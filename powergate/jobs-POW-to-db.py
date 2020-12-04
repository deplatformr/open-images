from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict
import os
import sqlite3
import csv
from datetime import datetime
from tabulate import tabulate

# Connect to Powergate
api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')
powergate = PowerGateClient(api, is_secure=False)

# Connect to db
abs_path = os.getcwd()
split = os.path.split(abs_path)
db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
cursor = workflow_db.cursor()

# Flush stale Jobs & Deal state info
cursor.execute("DROP TABLE jobs")
cursor.execute('CREATE TABLE "jobs" ("job_id" TEXT, "cid" TEXT, "timestamp"	TEXT, "status" TEXT, PRIMARY KEY("job_id"))')
cursor.execute("DROP TABLE jobs_deals")
cursor.execute('CREATE TABLE "jobs_deals" ("proposalCID" TEXT, "job_id" TEXT, "state" TEXT, "deal_id" INTEGER, "miner_id" TEXT, "price" INTEGER, "message" TEXT, PRIMARY KEY("proposalCID"))')
workflow_db.commit()

jobs = powergate.admin.storage_jobs.executing(user_id=user, cids='')
jobs_dict = MessageToDict(jobs)
print(str(len(jobs_dict["storageJobs"])) + " jobs currently executing.")

for storage_job in jobs_dict["storageJobs"]:

    utc_date = datetime.utcfromtimestamp(int(storage_job["createdAt"]))
    cursor.execute('INSERT INTO jobs(job_id, cid, timestamp, status) VALUES(?,?,?,?)', (storage_job["id"], storage_job["cid"], utc_date, storage_job["status"],))
    workflow_db.commit()

    try:
        for deal in storage_job["dealInfo"]:
            try:
                message = deal["message"]
            except:
                message = ""
            try:
                price = deal["pricePerEpoch"]
            except:
                price = 0
            try:
                id = deal["dealId"]
            except:
                id = "n/a"
            cursor.execute('INSERT INTO jobs_deals(proposalCID, job_id, state, deal_id, miner_id, price, message) VALUES (?,?,?,?,?,?,?)', (deal["proposalCid"], storage_job["id"], deal["stateName"], id, deal["miner"], price, message,))
            workflow_db.commit()  
    except:
        pass

jobs = powergate.admin.storage_jobs.queued(user_id=user, cids='')
jobs_dict = MessageToDict(jobs)
print(str(len(jobs_dict["storageJobs"])) + " jobs currently queued.")

for storage_job in jobs_dict["storageJobs"]:

    utc_date = datetime.utcfromtimestamp(int(storage_job["createdAt"]))
    cursor.execute('INSERT INTO jobs(job_id, cid, timestamp, status) VALUES(?,?,?,?)', (storage_job["id"], storage_job["cid"], utc_date, storage_job["status"],))
    workflow_db.commit()

print("Database updated.")