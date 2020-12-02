from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict
import os
import sqlite3
import csv
from datetime import datetime

api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')

powergate = PowerGateClient(api, is_secure=False)

jobs = powergate.admin.storage_jobs.executing(user_id=user, cids='')

jobs_dict = MessageToDict(jobs)

print(str(len(jobs_dict["storageJobs"])) + " jobs currently executing.")

today = datetime.today()
date_string = today.strftime("%b-%d-%Y")
filename = "storage-jobs-executing-" + user + "-" + date_string + ".csv"
print("Writing to " + filename)

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    # write column headers
    csvwriter.writerow(['Filename', 'CID', 'Job ID', 'Status', 'Created', 'Deal State', 'Deal Message', 'Piece CID', 'Miner']) 
    
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

        csvwriter.writerow([filename[0], cid, storage_job["id"], storage_job["status"], utc_date])

        try:
            for deal in storage_job["dealInfo"]:
                try:
                    msg = deal["message"]
                except:
                    msg = ''
                csvwriter.writerow(['','','','','',deal["stateName"], msg, deal["pieceCid"], deal["miner"]])
        except:
            pass