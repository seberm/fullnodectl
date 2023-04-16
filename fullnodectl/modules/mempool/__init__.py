"""
Various actions, oprations and stats provided by a mempool.
"""
import requests
import json
from logging import debug

from fullnodectl import mod

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


def main(args, config):
    debug(f"Running module {MODULE_NAME}")

    ACTIONS = {
        "fees": action_fees,
        "tx": action_tx,
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
    mempool_url = config["mempool"]["api_url"]
    api_url = f"{mempool_url}/v1/fees/recommended"

    session = requests.Session()

    response = session.get(api_url, verify=True)
    content = json.loads(response.content.decode("utf-8"))

    print(content)


def action_tx(args, config):
    print("args")
