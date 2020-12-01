import os
import sqlite3
import csv
from datetime import datetime
from pygate_grpc.client import PowerGateClient

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, False)

# get final storage deals info
storage_deals = powergate.deals.storage_deal_records(
    include_pending=False, include_final=True, token=token
)

total_deals = len(storage_deals)
print(str(total_deals) + " finalized storage deals found.")

if total_deals > 0:

    today = datetime.today()
    date_string = today.strftime("%b-%d-%Y")
    wallet_alias = storage_deals[1]["address"][-6:]
    filename = "finalized-deals-" + wallet_alias + "-" + date_string + ".csv"
    print("Writing to " + filename)

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        # write column headers
        csvwriter.writerow(['Deal ID', 'CID', 'Miner ID', 'Filename', 'Size (bytes)', 'Date stored (UTC)',
                            'Piece CID', 'Price per epoch', 'Start epoch', 'Activation Epoch', 'Duration', 'Wallet', 'Deal state'])

        abs_path = os.getcwd()
        split = os.path.split(abs_path)
        db_path = os.path.join(
            split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()

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
            cursor.execute("INSERT OR IGNORE INTO deals (deal_id, payload_cid, piece_cid, timestamp, piece_size, miner_id, start_epoch, activation_epoch, duration, price, wallet, state) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                deal["dealInfo"]["dealId"], deal["rootCid"], deal["dealInfo"]["pieceCid"], utc_date, deal["dealInfo"]["size"], deal["dealInfo"]["miner"], deal["dealInfo"]["startEpoch"], deal["dealInfo"]["activationEpoch"], deal["dealInfo"]["duration"], price, deal["address"], deal["dealInfo"]["stateName"]),)
            workflow_db.commit()

    workflow_db.close()
