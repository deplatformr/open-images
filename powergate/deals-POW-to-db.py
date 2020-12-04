import os
import sqlite3
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
        cursor.execute("INSERT OR IGNORE INTO deals (deal_id, payload_cid, piece_cid, timestamp, piece_size, miner_id, start_epoch, activation_epoch, duration, price, wallet, state) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            deal["dealInfo"]["dealId"], deal["rootCid"], deal["dealInfo"]["pieceCid"], utc_date, deal["dealInfo"]["size"], deal["dealInfo"]["miner"], deal["dealInfo"]["startEpoch"], deal["dealInfo"]["activationEpoch"], deal["dealInfo"]["duration"], price, deal["address"], deal["dealInfo"]["stateName"]),)
        workflow_db.commit()
    workflow_db.close()

print("Database updated.")
