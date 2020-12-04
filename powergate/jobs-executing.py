from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict
import os
import sqlite3
import csv
from datetime import datetime
from tabulate import tabulate

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')

powergate = PowerGateClient(api, is_secure=False)

jobs = powergate.admin.storage_jobs.executing(user_id=user, cids='')

jobs_dict = MessageToDict(jobs)

jobs = []

for storage_job in jobs_dict["storageJobs"]:

    utc_date = datetime.utcfromtimestamp(int(storage_job["createdAt"]))
    cid = storage_job["cid"]

    abs_path = os.getcwd()
    split = os.path.split(abs_path)
    db_path = os.path.join(
        split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)
    cursor = workflow_db.cursor()
    cursor.execute("SELECT name from packages where cid = ?", (cid,),)
    filename = cursor.fetchone()

    table = []

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
            table+=[(id, deal["stateName"], deal["miner"], price, message)]
    except Exception as e:
        print(e)

    jobs.append({"filename": filename[0], "job_id": storage_job["id"], "CID": cid, "Date": str(utc_date), "Deals": table})
    
# sort by package name
jobs.sort(key=lambda x: x['filename'], reverse=False)

for job in jobs:
    print(job["filename"])
    print("Job: " + job["job_id"])
    print("CID: " + job["CID"])
    print(job["Date"])
    print(tabulate(job["Deals"]))
    print("")

print(str(len(jobs_dict["storageJobs"])) + " jobs currently executing.")