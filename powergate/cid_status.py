from pygate_grpc.client import PowerGateClient
import os
import sys
from tabulate import tabulate

def deal_status(cid):
    api = os.getenv('POWERGATE_API')
    token = os.getenv('POWERGATE_TOKEN')
    powergate = PowerGateClient(api, is_secure=False)

    status = powergate.data.cid_info(cids=[cid], token=token)

    print("CID: " + status[0][0])
    print("Job ID: " + status[0][2]["id"])
    print("Status: " + status[0][2]["status"])
    table = []
    for deal in status[0][2]["dealInfo"]:
        if deal["stateName"]=="StorageDealError":
            message = deal["message"]
        else:
            message = ""
        table+=[(deal["stateName"], deal["miner"], deal["pricePerEpoch"], message)]
    print(tabulate(table))


if __name__ == "__main__":

    try:
        if sys.argv[1] is None:
            print("Please provide a CID.")
            sys.exit(0)
        else:
            deal_status(str(sys.argv[1]))
    except Exception as e:
        print("Unable to get status for " + str(sys.argv[1]) + ".")
        print(e)