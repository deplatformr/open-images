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

    print(filename[0])
    print(cid)
    print(utc_date)

    table = []

    try:
        for deal in storage_job["dealInfo"]:
            try:
                message = deal["message"]
            except:
                message = ''
            table+=[(deal["stateName"], deal["miner"], deal["pricePerEpoch"], message)]
        print(tabulate(table))
    except Exception as e:
        print(e)
    
    print("")

print(str(len(jobs_dict["storageJobs"])) + " jobs currently executing.")