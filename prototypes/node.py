import subprocess
import sys
import json
from collections import OrderedDict


def success(*args):
    return subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def is_active(unit):
    return success("systemctl", "is-active", "--quiet", unit)


def is_enabled(unit):
    return success("systemctl", "is-enabled", "--quiet", unit)


def cmd(*args):
    return subprocess.run(args, stdout=subprocess.PIPE).stdout.decode("utf-8")


def shell(*args):
    return cmd("bash", "-c", *args).strip()


infos = OrderedDict()
operator = "operator"


def set_onion_address(info, name, port):
    path = f"/var/lib/onion-addresses/{operator}/{name}"
    try:
        with open(path, "r") as f:
            onion_address = f.read().strip()
    except OSError:
        print(f"error reading file {path}", file=sys.stderr)
        return
    info["onion_address"] = f"{onion_address}:{port}"


def add_service(service, make_info):
    if not is_active(service):
        infos[service] = "service is not running"
    else:
        info = OrderedDict()
        exec(make_info, globals(), locals())
        infos[service] = info


def action_info(args):
    if is_enabled("onion-adresses") and not is_active("onion-adresses"):
        print("error: service 'onion-adresses' is not running")
        exit(1)

    add_service("bitcoind", """
info["local_address"] = "127.0.0.1:8333"
set_onion_address(info, "bitcoind", 8333)
""")

    add_service("btcpayserver", """
info["local_address"] = "127.0.0.1:23000"
""")

    add_service("clightning", """
info["local_address"] = "127.0.0.1:9735"
info["nodeid"] = shell("lightning-cli getinfo | jq -r '.id'")
if 'onion_address' in info:
    info["id"] = f"{info['nodeid']}@{info['onion_address']}"
""")

    add_service("clightning-rest", """
info["local_address"] = "127.0.0.1:3001"
set_onion_address(info, "clightning-rest", 3001)
""")

    add_service("electrs", """
info["local_address"] = "127.0.0.1:50001"
set_onion_address(info, "electrs", 50001)
""")

    add_service("rtl", """
info["local_address"] = "127.0.0.1:3000"
set_onion_address(info, "rtl", 80)
""")

    add_service("sshd", """set_onion_address(info, "sshd", 22)""")

    print(json.dumps(infos, indent=2))


ACTIONS = {
    "info": action_info,
}


# Subparser TODO
#    subp_node = p_node.add_subparsers(
#        dest="action",
#        help="Action name",
#        required=True,
#    )
#    subp_node.add_parser("info", help="Print node information")
