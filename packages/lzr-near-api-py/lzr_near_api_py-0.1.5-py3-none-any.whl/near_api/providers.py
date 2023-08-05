import base64
import json
import time
from typing import Union, Optional
import logging
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

import requests

logger = logging.getLogger(__name__)


def _default_retry_strategy() -> Retry:
    retry_backoff_factor = 0.7
    connection_timeout = 5
    read_timeout = 8
    method_whitelist = ["GET", "POST"]

    retry_strategy = Retry(
        backoff_factor=retry_backoff_factor,
        connect=connection_timeout,
        read=read_timeout,
        status_forcelist=[502, 503],
        allowed_methods=method_whitelist)
    return retry_strategy


class FinalityTypes:
    FINAL = "final"
    OPTIMISTIC = "optimistic"


class JsonProviderError(Exception):
    def get_type(self) -> Optional[str]:
        try:
            return self.args[0]["name"]
        except (IndexError, KeyError):
            return None

    def get_cause(self) -> Optional[str]:
        try:
            return self.args[0]["cause"]["name"]
        except (IndexError, KeyError):
            return None

    def is_invalid_nonce_tx_error(self) -> bool:
        try:
            return (
                self.get_type() == "HANDLER_ERROR"
                and self.get_cause() == "INVALID_TRANSACTION"
                and "InvalidNonce" in self.args[0]["data"]["TxExecutionError"]["InvalidTxError"]
            )
        except (IndexError, KeyError):
            return False

    def is_request_timeout_error(self) -> bool:
        return (
            self.get_type() == "HANDLER_ERROR"
            and self.get_cause() == "TIMEOUT_ERROR"
        )

    def is_expired_tx_error(self) -> bool:
        try:
            return (
                self.get_type() == "HANDLER_ERROR"
                and self.get_cause() == "INVALID_TRANSACTION"
                and self.args[0]["data"]["TxExecutionError"]["InvalidTxError"] == "Expired"
            )
        except (IndexError, KeyError):
            return False


class JsonProvider(object):
    def __init__(self, rpc_addr, proxies=None,
                 retry_strategy: Retry = _default_retry_strategy(),
                 tx_timeout_retry_number: int = 12,
                 tx_timeout_retry_backoff_factor: float = 1.5,):
        if isinstance(rpc_addr, tuple):
            self._rpc_addr = "http://%s:%s" % rpc_addr
        else:
            self._rpc_addr = rpc_addr

        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        self.proxies = proxies
        self._http = http

        self._tx_timeout_retry_number = tx_timeout_retry_number
        self._tx_timeout_retry_backoff_factor = tx_timeout_retry_backoff_factor

    def rpc_addr(self) -> str:
        return self._rpc_addr

    def json_rpc(self, method: str, params: Union[dict, list, str], timeout: 'TimeoutType' = 2.0) -> dict:
        attempt = 0
        while True:
            try:
                return self._json_rpc_once(method, params, timeout)
            except JsonProviderError as e:
                if attempt >= self._tx_timeout_retry_number:
                    raise
                if e.is_request_timeout_error():
                    logger.warning(
                        "Retrying request to %s as it has timed out: %s", method, e)
                else:
                    raise
            attempt += 1
            time.sleep(self._tx_timeout_retry_backoff_factor ** attempt * 0.5)

    def _json_rpc_once(self, method: str, params: Union[dict, list, str], timeout: 'TimeoutType' = 2.0) -> dict:
        j = {
            'method': method,
            'params': params,
            'id': "dontcare",
            'jsonrpc': "2.0"
        }
        r = self._http.post(self.rpc_addr(), json=j,
                            proxies=self.proxies)
        r.raise_for_status()
        content = json.loads(r.content)
        if "error" in content:
            raise JsonProviderError(content['error'])
        return content['result']

    def send_tx(self, signed_tx: bytes) -> dict:
        return self.json_rpc("broadcast_tx_async",
                             [base64.b64encode(signed_tx).decode('utf8')])

    def send_tx_and_wait(self, signed_tx: bytes) -> dict:
        return self.json_rpc("broadcast_tx_commit",
                             [base64.b64encode(signed_tx).decode('utf8')])

    def get_status(self) -> dict:
        r = self._http.get("%s/status" % self.rpc_addr())
        r.raise_for_status()
        return json.loads(r.content)

    def get_validators(self) -> dict:
        return self.json_rpc("validators", [None])

    def query(self, query_object: str) -> dict:
        return self.json_rpc("query", query_object)

    def get_account(
            self,
            account_id: str,
            finality: str = FinalityTypes.OPTIMISTIC
    ) -> dict:
        return self.json_rpc(
            "query", {
                'request_type': "view_account",
                'account_id': account_id,
                'finality': finality
            })

    def get_access_key_list(
            self,
            account_id: str,
            finality: str = FinalityTypes.OPTIMISTIC
    ) -> dict:
        return self.json_rpc(
            "query", {
                'request_type': "view_access_key_list",
                'account_id': account_id,
                'finality': finality
            })

    def get_access_key(
            self,
            account_id: str,
            public_key: str,
            finality: str = FinalityTypes.OPTIMISTIC
    ) -> dict:
        return self.json_rpc(
            "query", {
                'request_type': "view_access_key",
                'account_id': account_id,
                'public_key': public_key,
                'finality': finality
            })

    def view_call(
            self,
            account_id: str,
            method_name: str,
            args: bytes,
            finality: str = FinalityTypes.OPTIMISTIC
    ) -> dict:
        return self.json_rpc(
            "query", {
                'request_type': "call_function",
                'account_id': account_id,
                'method_name': method_name,
                'args_base64': base64.b64encode(args).decode('utf8'),
                'finality': finality
            })

    def get_block(self, block_id: str) -> dict:
        return self.json_rpc("block", [block_id])

    def get_chunk(self, chunk_id: str) -> dict:
        return self.json_rpc("chunk", [chunk_id])

    def get_tx(self, tx_hash: str, tx_recipient_id: str) -> dict:
        return self.json_rpc("tx", [tx_hash, tx_recipient_id])

    def get_changes_in_block(
            self,
            block_id: Union[str] = None,
            finality: str = None
    ) -> dict:
        """Use either block_id or finality. Choose finality from "finality_types" class."""
        params = {}
        if block_id:
            params['block_id'] = block_id
        if finality:
            params['finality'] = finality
        return self.json_rpc("EXPERIMENTAL_changes_in_block", params)

    def get_validators_ordered(self, block_hash: bytes) -> dict:
        return self.json_rpc("EXPERIMENTAL_validators_ordered", [block_hash])

    def get_light_client_proof(
            self,
            outcome_type: str,
            tx_or_receipt_id: str,
            sender_or_receiver_id: str,
            light_client_head: str
    ) -> dict:
        if outcome_type == "receipt":
            params = {
                'type': "receipt",
                'receipt_id': tx_or_receipt_id,
                'receiver_id': sender_or_receiver_id,
                'light_client_head': light_client_head
            }
        else:
            params = {
                'type': "transaction",
                'transaction_hash': tx_or_receipt_id,
                'sender_id': sender_or_receiver_id,
                'light_client_head': light_client_head
            }
        return self.json_rpc("light_client_proof", params)

    def get_next_light_client_block(self, last_block_hash) -> dict:
        return self.json_rpc("next_light_client_block", [last_block_hash])

    def get_receipt(self, receipt_hash) -> dict:
        return self.json_rpc("EXPERIMENTAL_receipt", [receipt_hash])
