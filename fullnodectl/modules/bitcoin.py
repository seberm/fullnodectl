"""
Module description TODO
"""
from logging import debug

from fullnodectl import mod

__license__ = "MIT"

MODULE_NAME = "bitcoin"
MODULE_AUTHOR = "Otto Sabart"
MODULE_AUTHOR_EMAIL = "seberm@seberm.com"
MODULE_DESCRIPTION = __doc__


def init_parsers(parser):
    debug("Initializing module parser")
    p_bitcoin = parser.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_bitcoin.add_parser("fees", help="Get current transaction fees")

    p_tx = p_bitcoin.add_parser("tx", help="Get information about specific transaction by its TXID")
    p_tx.add_argument("txid", help="Transaction ID (TXID)")

    p_block = p_bitcoin.add_parser("block", help="Get information about blocks")
    p_block.add_argument("id", help="Block number or a block hash. Without this argument program will return the information about the last block.", nargs="*")


def main(args):
    debug(f"Running module {MODULE_NAME}")

    ACTIONS = {
        "fees": action_fees,
        "tx": action_tx,
    }
    act = ACTIONS.get(args.action)
    act(args)

    return 0


MODULE_HOOKS = {
    mod.HOOK_INIT_PARSERS: init_parsers,
    # mod.HOOK_INIT: init,
    mod.HOOK_RUN: main,
}


def action_fees(args):
    print("Fees are ... TODO")


def action_tx(args):
    print(f"info about tx '{args.txid}' is ... TODO")
