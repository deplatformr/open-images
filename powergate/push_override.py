import os
import sqlite3
from datetime import datetime
from pygate_grpc.client import PowerGateClient

abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(workflow_db_path)

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')
powergate = PowerGateClient(api, is_secure=True)

cid = "QmaQtN37VfCWfmmQTtNFZVA85K911He7rF5JochkD5iGsK"
utctime = datetime.utcnow()

job = powergate.ffs.push(cid, token, override=True)
print("Repushed CID " + cid + " to Filecoin.")
print("Job ID: " + job.job_id)
utctime = datetime.utcnow()
cursor = workflow_db.cursor()
cursor.execute("INSERT INTO jobs (job_id, cid, ffs, timestamp, status) VALUES (?,?,?,?,?)",
               (job.job_id, cid, ffs, utctime, "Executing",),)
workflow_db.commit()
workflow_db.close()
