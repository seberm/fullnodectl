#!/usr/bin/env python

import socket
import json

# Ref.: https://electrum.readthedocs.io/en/latest/protocol.html#blockchain-estimatefee
# echo '{ "id": 17, "method": "blockchain.estimatefee", "params": [ 6 ] }' | nc <host> 50001

host = 'localhost'
port = 50001

sock = socket.socket()
sock.connect((host, port, ))

sock.sendall(b'{ "id": 17, "method": "blockchain.estimatefee", "params": [ 6 ] }\n')

data = sock.recv(1024)
json_data = json.loads(data)

sock.close()

fee_rate_kb = float(json_data['result'])
fee = (fee_rate_kb * 100_000_000) / 1000  # to sats per B

print(f"Current fee: {fee} sat/B")
