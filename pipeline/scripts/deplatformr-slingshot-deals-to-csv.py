import os
import sqlite3
import csv
from datetime import datetime
from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, is_secure=True)

# get final storage deals info
storage_deals = powergate.ffs.list_storage_deal_records(
    include_pending=False, include_final=True, token=token)

print(str(len(storage_deals.records)) +
      " storage deals found for ffs " + ffs + ".")
csv_file = "slingshot-deals-deplatformr.csv"
print("Writing to " + csv_file + ".")

with open(csv_file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # write column headers
    csvwriter.writerow(['CID', 'Miner ID', 'Filename', 'File format', 'Size (bytes)', 'Date stored (UTC)',
                        'Piece CID', 'Wallet ID', 'Deal ID', 'Price per epoch', 'Start epoch', 'Duration'])

    for record in storage_deals.records:
        deal = MessageToDict(record)
        utc_date = datetime.utcfromtimestamp(int(deal["time"]))
        cid = deal["rootCid"]
        abs_path = os.getcwd()
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute("SELECT name from packages where cid = ?", (cid,),)
        filename = cursor.fetchone()
        csvwriter.writerow([deal["rootCid"], deal["dealInfo"]["miner"], filename[0], '.tar containing .jpg, .png, .json-ld', deal["dealInfo"]["size"], utc_date, deal["dealInfo"]
                            ["pieceCid"], deal["addr"], deal["dealInfo"]["dealId"], deal["dealInfo"]["pricePerEpoch"], deal["dealInfo"]["startEpoch"], deal["dealInfo"]["duration"]])

# Combine output from the two FFSes used in Slingshot into one CSV
api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')

powergate = PowerGateClient(api, False)

# get final storage deals info
storage_deals = powergate.ffs.list_storage_deal_records(
    include_pending=False, include_final=True, token=token)

print(str(len(storage_deals.records)) +
      " storage deals found for ffs " + ffs + ".")
print("Writing to " + csv_file + ".")

with open(csv_file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    for record in storage_deals.records:
        deal = MessageToDict(record)
        utc_date = datetime.utcfromtimestamp(int(deal["time"]))
        cid = deal["rootCid"]
        abs_path = os.getcwd()
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute("SELECT name from packages where cid = ?", (cid,),)
        filename = cursor.fetchone()
        csvwriter.writerow([deal["rootCid"], deal["dealInfo"]["miner"], filename[0], '.tar containing .jpg, .png, .json-ld', deal["dealInfo"]["size"], utc_date, deal["dealInfo"]
                            ["pieceCid"], deal["addr"], deal["dealInfo"]["dealId"], deal["dealInfo"]["pricePerEpoch"], deal["dealInfo"]["startEpoch"], deal["dealInfo"]["duration"]])
