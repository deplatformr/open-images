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
        table+=[(deal["stateName"], deal["miner"], deal["pricePerEpoch"])]
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

"""
CidInfo
    (cid='QmRpALcLgVYvyurJqNR59WEyyA4wS1hDQYK4SQ48MaCqQR', 
    latestPushedStorageConfig={'hot': {'allowUnfreeze': True, 'unfreezeMaxPrice': '50000000', 'ipfs': {'addTimeout': '30'}}, 'cold': {'enabled': True, 'filecoin': {'replicationFactor': '4', 'dealMinDuration': '518400', 'renew': {}, 'address': 'f3qne2hc6e6hoki2o47urwodci3546z2govz6zjachm3yeogj6rfqyoh2xticeuwwt7rk6yfbit7xvdiukt4tq', 'maxPrice': '10000000000', 'fastRetrieval': True, 'dealStartOffset': '8640'}}, 'repairable': True}, executingStorageJob=
        {'id': '30afaab2-82ae-478d-b081-27bcd32d5f04', 'apiId': '7bcc30a1-fecc-4892-a99a-ab6c54d59360', 'cid': 'QmRpALcLgVYvyurJqNR59WEyyA4wS1hDQYK4SQ48MaCqQR', 'status': 'JOB_STATUS_EXECUTING',          
            'dealInfo': 
                [{'proposalCid': 'bafyreiadikthr23a3tvszap7deeswixqivkkthpgvpkqz5tflkf5vcvlwa', 'stateId': '13', 
                'stateName': 'StorageDealCheckForAcceptance', 
                'miner': 'f080480', 
                'pieceCid': 'baga6ea4seaqpabshwzcrmt2fcumeii22kfg4crpsh4wwyaqps5mycociexhkija', 
                'size': '1065353216', 
                'pricePerEpoch': '10000000000', 
                'duration': '521721'}, 
                {'proposalCid': 'bafyreibl4xfcdkzt5kv6ymdchpn7rx7tafxoahmuikphezsic4lnseews4', 'stateId': '13', 'stateName': 'StorageDealCheckForAcceptance', 'miner': 'f014768', 'pieceCid': 'baga6ea4seaqpabshwzcrmt2fcumeii22kfg4crpsh4wwyaqps5mycociexhkija', 'size': '1065353216', 'pricePerEpoch': '5000000000', 'duration': '523159'}, 
                {'proposalCid': 'bafyreibragoucbw62wpqhiui23w6567lo6m2xly3uzz5br7lnzwz3ureh4', 'stateId': '13', 'stateName': 'StorageDealCheckForAcceptance', 'miner': 'f079817', 'pieceCid': 'baga6ea4seaqpabshwzcrmt2fcumeii22kfg4crpsh4wwyaqps5mycociexhkija', 'size': '1065353216', 'pricePerEpoch': '10000000000', 'duration': '523805'}, 
                {'proposalCid': 'bafyreidqfte5vmf2emvufnzcvlveal4s67atybn7b2uyvmcytrmqowiejm', 'stateId': '16', 'stateName': 'StorageDealStartDataTransfer', 'miner': 'f065280', 'pieceCid': 'baga6ea4seaqpabshwzcrmt2fcumeii22kfg4crpsh4wwyaqps5mycociexhkija', 'size': '1065353216', 'pricePerEpoch': '500000000', 'duration': '522933'}], 'createdAt': '1606955873'}, queuedStorageJobs=None)
"""