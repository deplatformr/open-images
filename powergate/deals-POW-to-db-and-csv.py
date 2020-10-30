import os
import sqlite3
import csv
from datetime import datetime
from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, False)

# get final storage deals info
storage_deals = powergate.ffs.list_storage_deal_records(
    include_pending=False, include_final=True, token=token)

print(str(len(storage_deals.records)) + " storage deals found.")
filename = "deals-ffs-" + ffs + ".csv"
print("Writing to " + filename + ".")

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # write column headers
    csvwriter.writerow(['CID', 'Miner ID', 'Filename', 'File format', 'Size (bytes)', 'Date stored (UTC)',
                        'Piece CID', 'Wallet ID', 'Deal ID', 'Price per epoch', 'Start epoch', 'Duration'])

    abs_path = os.getcwd()
    split = os.path.split(abs_path)
    db_path = os.path.join(
        split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)
    cursor = workflow_db.cursor()

    for record in storage_deals.records:
        deal = MessageToDict(record)

        try:
            price = deal["dealInfo"]["pricePerEpoch"]
        except:
            price = 0

        utc_date = datetime.utcfromtimestamp(int(deal["time"]))
        cid = deal["rootCid"]
        cursor.execute("SELECT name from packages where cid = ?", (cid,),)
        filename = cursor.fetchone()
        csvwriter.writerow([deal["rootCid"], deal["dealInfo"]["miner"], filename[0], '.tar containing .jpg, .png, .json-ld', deal["dealInfo"]["size"], utc_date, deal["dealInfo"]
                            ["pieceCid"], deal["addr"], deal["dealInfo"]["dealId"], price, deal["dealInfo"]["startEpoch"], deal["dealInfo"]["duration"]])
        cursor.execute("INSERT OR IGNORE INTO deals (deal_id, payload_cid, piece_cid, timestamp, piece_size, miner_id, start_epoch, duration, price) VALUES (?,?,?,?,?,?,?,?,?)", (
            deal["dealInfo"]["dealId"], deal["rootCid"], deal["dealInfo"]["pieceCid"], utc_date, deal["dealInfo"]["size"], deal["dealInfo"]["miner"], deal["dealInfo"]["startEpoch"], deal["dealInfo"]["duration"], price),)

workflow_db.close()
