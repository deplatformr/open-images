import os
import csv
from datetime import datetime
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, False)

# get final storage deals info
storage_deals = powergate.deals.storage_deal_records(
    include_pending=True, include_final=False, token=token
)

total_deals = len(storage_deals)
print(str(total_deals) + " pending storage deals found.")

if total_deals > 0:
    today = datetime.today()
    date_string = today.strftime("%b-%d-%Y")
    wallet_alias = storage_deals[1]["address"][-6:]
    filename = "pending-deals-" + wallet_alias + "-" + date_string + ".csv"
    print("Writing to " + filename)

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        # write column headers
        csvwriter.writerow(['Deal ID', 'CID', 'Miner ID', 'Filename', 'Size (bytes)', 'Date stored (UTC)',
                            'Piece CID', 'Price per epoch', 'Start epoch', 'Activation Epoch', 'Duration', 'Wallet', 'Deal state'])

        for deal in storage_deals:

            try:
                price = deal["dealInfo"]["pricePerEpoch"]
            except:
                price = 0

            utc_date = datetime.utcfromtimestamp(int(deal["time"]))
            cid = deal["rootCid"]
            cursor.execute("SELECT name from packages where cid = ?", (cid,),)
            filename = cursor.fetchone()
            csvwriter.writerow([deal["dealInfo"]["dealId"], deal["rootCid"], deal["dealInfo"]["miner"], filename[0], deal["dealInfo"]["size"], utc_date, deal["dealInfo"]["pieceCid"], price, deal["dealInfo"]["startEpoch"], deal["dealInfo"]["activationEpoch"], deal["dealInfo"]["duration"], deal["address"], deal["dealInfo"]["stateName"]])
