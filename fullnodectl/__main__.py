import argparse
import importlib
import logging

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="TODO",
        allow_abbrev=False,
    )

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        help="Path to configuration file",
    )

    module_subparsers = parser.add_subparsers(
        dest="module",
        help="Module name",
        required=True,
    )

    p_node = module_subparsers.add_parser("node", help="Current fullnode actions")
    subp_node = p_node.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    subp_node.add_parser("info", help="Print node information")

    p_bitcoin = module_subparsers.add_parser("bitcoin", help="Bitcoin related operations")
    subp_bitcoin = p_bitcoin.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    subp_bitcoin.add_parser("fees", help="Get current transaction fees")
    p_tx = subp_bitcoin.add_parser("tx", help="Get information about specific transaction by its TXID")
    p_tx.add_argument("txid", help="Transaction ID (TXID)")

    args = parser.parse_args()

    module_str = f"fullnodectl.modules.{args.module}"

    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError as e:
        print(dir(e))
        log.error(f"Module '{args.module}' was not found in '{e.name}'")
        # FIXME: raise FullNodeCTLError
        raise

    action = module.ACTIONS.get(args.action)
    action(args)
