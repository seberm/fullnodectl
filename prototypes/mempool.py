#!/usr/bin/env python

import requests
import json


mempool_url = "https://mempool.space/api"

api_url = f"{mempool_url}/address/1wiz18xYmhRX6xStj2b9t1rwWX4GKUgpv"

session = requests.Session()

response = session.get(api_url, verify=True)
content = json.loads(response.content.decode("utf-8"))

print(content)
