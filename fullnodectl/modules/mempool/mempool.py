import json
import logging
import requests

from fullnodectl import errors


log = logging.getLogger(__name__)


class API:
    def __init__(self, api_url, ssl_verify=True):
        self.api_url = api_url
        self.ssl_verify = ssl_verify
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()

        return self._session

    def _get(self, endpoint):
        response = self.session.get(f"{self.api_url}/{endpoint}", verify=self.ssl_verify)
        content = response.content.decode("UTF-8")

        if response.status_code != 200:
            log.error(content)
            raise errors.FullNodeCTLError(f"Mempool responded with HTTP code: {response.status_code}")

        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError:
            return content

    @property
    def recommended_fees(self):
        return self._get("v1/fees/recommended")

    @property
    def difficulty_adjustment(self):
        return self._get("v1/difficulty-adjustment")

    def get_transaction(self, txid):
        return self._get(f"tx/{txid}")

    def get_block_by_hash(self, hash_id):
        return self._get(f"block/{hash_id}")

    def get_block_by_height(self, height):
        return self._get(f"block-height/{height}")

    @property
    def block_tip_hash(self):
        return self._get("blocks/tip/hash")
