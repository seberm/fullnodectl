"""
Various actions, oprations and stats provided by an electrum server.
"""
from logging import debug
import asyncio
import json

from connectrum.client import StratumClient
from connectrum.svr_info import ServerInfo
# from connectrum import ElectrumErrorResponse

from fullnodectl import mod

__license__ = "MIT"

MODULE_NAME = "electrum"
MODULE_AUTHOR = "Otto Sabart"
MODULE_AUTHOR_EMAIL = "seberm@seberm.com"
MODULE_DESCRIPTION = __doc__


def init_parsers(parser):
    p_electrum = parser.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_electrum.add_parser("banner", help="Get server banner")
    p_electrum.add_parser("donations", help="Get donation information")
    p_electrum.add_parser("monitor", help="Various monitoring actions")


def main(args, config):
    debug(f"Running module {MODULE_NAME}")

    server = "bitcoin.temi.seberm.com"
    protocol = "e"
    port = "50001"

    svr = ServerInfo(server, server, ports=((protocol+port)))
    loop = asyncio.get_event_loop()
    conn = StratumClient(loop=loop)
    connector = conn.connect(svr, protocol, use_tor=svr.is_onion, disable_cert_verify=True, short_term=True)

    try:
        loop.create_task(connector)
    except Exception as e:
        print("failed to connect: %s" % e)
        return -1

    ACTIONS = {
        "banner": action_banner,
        "donations": action_donations,
        "monitor": action_monitor,
    }
    act = ACTIONS.get(args.action)
    loop.run_until_complete(act(args, config, conn))
    loop.close()

    return 0


MODULE_HOOKS = {
    mod.HOOK_INIT: lambda *args: None,
    mod.HOOK_INIT_PARSERS: init_parsers,
    mod.HOOK_RUN: main,
}


async def action_banner(args, config, connection):
    action = "server.banner"
    motd = await connection.RPC(action)
    print(motd)


async def action_donations(args, config, connection):
    action = "server.donation_address"
    donation_info = await connection.RPC(action)
    print(donation_info)


async def action_monitor(args, config, connection):
    action = "blockchain.headers.subscribe"
    fut, q = connection.subscribe(action)
    print("Current block:")
    print(json.dumps(await fut, indent=1))

    print("Monitoring:")
    while 1:
        result = await q.get()
        print(json.dumps(result, indent=1))
