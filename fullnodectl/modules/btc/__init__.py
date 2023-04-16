"""
Common operations, actions and stats supported by a bitcoin service.

# Refs.:
# - https://github.com/petertodd/python-bitcoinlib/blob/master/bitcoin/rpc.py
"""
import logging
import json
from binascii import hexlify

from bitcoin import rpc

from fullnodectl import (
    mod,
    errors,
)

__license__ = "MIT"
log = logging.getLogger(__name__)

MODULE_NAME = "btc"
MODULE_AUTHOR = "Otto Sabart"
MODULE_AUTHOR_EMAIL = "seberm@seberm.com"
MODULE_DESCRIPTION = __doc__


def init_parsers(parser):
    log.debug("Initializing module parser")
    p_bitcoin = parser.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_bitcoin.add_parser("fees", help="Get current transaction fees")

    p_tx = p_bitcoin.add_parser("tx", help="Get information about specific transaction by its TXID")
    p_tx.add_argument("txid", help="Transaction ID (TXID)")

    p_block = p_bitcoin.add_parser("block", help="Get information about blocks")

    # TODO: Also support block hashes
    p_block.add_argument(
        "block_id",
        help="Block ID (number). Without this argument program will return the information about the last block.",
        nargs="*",
    )


def main(args, config):
    log.debug(f"Running module {MODULE_NAME}")

    ACTIONS = {
        "fees": action_fees,
        "tx": action_tx,
        "block": action_block,
    }
    act = ACTIONS.get(args.action)
    act(args, config)

    return 0


MODULE_HOOKS = {
    mod.HOOK_INIT: lambda *args: None,
    mod.HOOK_INIT_PARSERS: init_parsers,
    mod.HOOK_RUN: main,
}


def action_fees(args, config):
    print("Fees are ... TODO")


def action_block(args, config):
    proxy = rpc.Proxy(config["bitcoin"]["url"])

    try:
        if not args.block_id:
            log.debug("No block hash/number was provided, getting info about current best-block height.")
            args.block_id.append(proxy.getblockcount())

        #block_hash = bytes(args.hash[0], "UTF-8")
        block_id = int(args.block_id[0])
        block_hash = proxy.getblockhash(block_id)
        block = proxy.getblock(block_hash)
        header = block.get_header()

        out = {
            "id": block_id,
            # FIXME
            #"hash": hexlify(block_hash).decode("UTF-8"),
            #"hashPrevBlock": hexlify(header.hashPrevBlock).decode("UTF-8"),
            "nBits": header.nBits,
            "nNonce": header.nNonce,
            "nTime": header.nTime,
            "nVersion": header.nVersion,
            #"size": "",
            #"weight": "",

            #"vtx" :
            #"coinbase" : block.vtx[0],
            #coinbase_opreturn_data (coinbase data)
        }
        print(json.dumps(out, indent=2))
    except rpc.JSONRPCError as e:
        log.error(e)
        raise errors.FullNodeCTLError("There was a problem when connecting to bitcoin RPC.")


def action_tx(args, config):
    print(f"info about tx '{args.txid}' is ... TODO")
