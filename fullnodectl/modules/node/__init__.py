"""
<module description>
"""
from fullnodectl import mod

__license__ = "MIT"

MODULE_NAME = "node"
MODULE_AUTHOR = "Otto Sabart"
MODULE_AUTHOR_EMAIL = "seberm@seberm.com"
MODULE_DESCRIPTION = __doc__


def init_parsers(parser):
    p_node = parser.add_subparsers(
        dest="action",
        help="Action name",
        required=True,
    )
    p_node.add_parser("status", help="Show current status of services")
    p_node.add_parser("ps", help="Show services and its resources")

    actions = ["start", "stop", "enable", "disable"]
    service_parser = p_node.add_parser("service", help="Control services")
    service_subparser = service_parser.add_subparsers(
        dest="service_action",
        help="/".join(actions) + " full node services",
        required=True,
    )

    for action in actions:
        p_action = service_subparser.add_parser(action, help=f"{action.capitalize()} node service")
        p_action.add_argument(
            "name",
            choices=["bitcoin", "ln", "electrum"],
        )


def main(args):
    return 0


MODULE_HOOKS = {
    mod.HOOK_INIT: lambda *args: None,
    mod.HOOK_INIT_PARSERS: init_parsers,
    mod.HOOK_RUN: main,
}
