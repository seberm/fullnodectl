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
        return json.loads(response.content.decode("utf-8"))

    @property
    def recommended_fees(self):
        return self._get("v1/fees/recommended")
