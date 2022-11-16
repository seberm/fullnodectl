
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="TODO",
        allow_abbrev=False,
    )

    module_subparsers = parser.add_subparsers(
        dest="module",
        help="Module name",
        required=True,
    )

    p_module = module_subparsers.add_parser("node", help="Current fullnode actions")
    node_action_subparsers = p_module.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_info = node_action_subparsers.add_parser("info", help="Print node information")

    #b_parser = p_bitcoin.add_subparsers(
    #    dest="action",
    #    help="Action name",
    #    required=True,
    #)
    #b_parser.add_argument("fees", help="Get current transaction fees")
    #b_parser.add_argument("tx", "transaction", help="Get current transaction fees")

    args = parser.parse_args()
    #print(vars(args))

    from fullnodectl.modules import node
    act = node.ACTIONS.get(args.action)

    act(args)
