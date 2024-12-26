# FullNodeCTL - Your Bitcoin/Lightning Ultimate Tool

** This project is a draft and it's still under design **



## Overview

FullNodeCTL is a comprehensive tool designed to manage and interact with your Bitcoin and Lightning nodes. It provides a wide range of features and functionalities to help you monitor, manage, and optimize your nodes.

## Electrum
------------

### Commands

* `fullnodectl electrum banner`: Displays the server banner
* `fullnodectl electrum donations`: Displays the donation address
* `fullnodectl electrum peers`: Displays the list of current peers
* `fullnodectl electrum fees`: Displays the current fees according to the Electrs/Fulcrum server
* `fullnodectl electrum monitor --address`: Monitors the specified address and displays any incoming transactions or changes
* `fullnodectl electrum monitor --block`: Monitors new blocks and block headers
* `fullnodectl electrum address`: Displays information about the specified address, including UTXOs
* `fullnodectl electrum address-history`: Displays the transaction history of the specified address
* `fullnodectl electrum block <hash/id>`: Displays information about the specified block based on its hash or ID
* `fullnodectl electrum tx/transaction '<txid>'`: Displays information about the specified transaction

## Bitcoind
------------

### Commands

* `fullnodectl btc block '<id>/<hash>'`: Displays information about the specified block, including its height and other details (default: returns the current block and its height)
* `fullnodectl btc diff/difficulty`: Displays the current difficulty
* `fullnodectl btc ?peers/netinfo?`: Displays information about the node's peers and network

## LND/CLN
------------

### Commands

* `fullnodectl ln peers`: Displays the number of peers and their IP addresses
* `fullnodectl ln balance`: Displays the current balance (on-chain and off-chain)
* `fullnodectl ln ?status/netinfo?`: Displays information about the node's status and network
* `fullnodectl ln channels`: Displays information about the channels, including their size and balance

## Mempool.space (or custom instance)
--------------------------------------

### Commands

* `fullnodectl mempool`: Integrates with the API of the specified Mempool.space instance (or custom instance)
* `fullnodectl mempool fees`: Displays the current fees
* `fullnodectl mempool block id/hash`: Displays information about the specified block based on its ID or hash
* `fullnodectl mempool address`: Displays information about the specified address
* `fullnodectl mempool pool`: Displays information about the mining pools and statistics
* `fullnodectl mempool hashrate`: Displays information about the hashrate
* `fullnodectl mempool stats`: Displays information about the mempool, including the number of transactions, size, and total fees
* `fullnodectl mempool ln stats`: Displays statistics about the Lightning Network
* `fullnodectl mempool ln node <pubkey>`: Displays information about the specified node, or searches for a node based on the provided query
* `fullnodectl mempool ln channel <channel_id>`: Displays information about the specified channel

## Node
------

### Commands

* `fullnodectl node info`: Displays information about the node, including its software version, clearnet addresses, and onion addresses
* `fullnodectl node status`: Displays information about the services running on the node, including their status
* `fullnodectl node ps`: Displays a filtered list of processes running on the node, including their resource usage and blockchain size
* `fullnodectl node [start | stop | status ] [bitcoin | ln | ...]`: Starts, stops, or displays the status of the specified service

### Serve

* `fullnodectl serve`: Exposes public information through an API, using a framework like FastAPI, or integrates a simple web-based dashboard
