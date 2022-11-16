#!/usr/bin/env python

from bitcoin import rpc

username = "public"
password = "somepwd"
hostname = "localhost"
port = 8332

proxy = rpc.Proxy(f"http://{username}:{password}@{hostname}:{port}")

block_count = proxy.getblockcount()
print(f"Current block: {block_count}")
