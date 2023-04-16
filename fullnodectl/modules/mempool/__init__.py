"""
Various actions, oprations and stats provided by a mempool.
"""
from logging import debug
import json

from fullnodectl import mod
from fullnodectl.modules.mempool import mempool

__license__ = "MIT"

MODULE_NAME = "mempool"
MODULE_AUTHOR = "Otto Sabart"
MODULE_AUTHOR_EMAIL = "seberm@seberm.com"
MODULE_DESCRIPTION = __doc__


def init_parsers(parser):
    p_mempool = parser.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_mempool.add_parser("fees", help="Get current transaction fees")

    p_tx = p_mempool.add_parser("tx", help="Get information about specific transaction by its TXID")
    p_tx.add_argument("txid", help="Transaction ID (TXID)")

    p_block = p_mempool.add_parser("block", help="Get information about blocks")
    p_block.add_argument(
        "block_id",
        help="Block number of a hash. Without this argument program will return the information about the last block.",
        nargs="*",
    )


def main(args, config):
    debug(f"Running module {MODULE_NAME}")

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
    m = mempool.API(config["mempool"]["api_url"])
    print(json.dumps(m.recommended_fees, indent=2))


def action_tx(args, config):
    print("args")


def action_block(args, config):
    print("args")
