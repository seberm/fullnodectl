import json
import requests


class API:
    def __init__(self, api_url):
        self.api_url = api_url
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()

        return self._session

    def _get(self, endpoint):
        response = self.session.get(f"{self.api_url}/{endpoint}", verify=True)
        return json.loads(response.content.decode("UTF-8"))

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
