

def action_fees(args):
    print("Fees are ... TODO")


def action_tx(args):
    print(f"info about tx '{args.txid}' is ... TODO")


ACTIONS = {
    "fees": action_fees,
    "tx": action_tx,
}
