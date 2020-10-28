import os
import sqlite3
from pygate_grpc.client import PowerGateClient
from google.protobuf.json_format import MessageToDict


api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')


powergate = PowerGateClient(api, is_secure=False)


abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")

workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

cursor.execute("SELECT name, cid FROM packages WHERE cid IS NOT NULL")
packages = cursor.fetchall()

for package in packages:
    cursor.execute("SELECT job_id FROM jobs WHERE cid=?", (package[1],),)
    jobs = cursor.fetchall()
    print(package[0] + "(CID: " + package[1] +
          ") has " + str(len(jobs)) + " jobs.")
    for job in jobs:
        job_id = job[0]
        print("Job ID: " + job_id)
        try:
            response = powergate.ffs.get_storage_job(
                jid=job_id, token=token)
            job = MessageToDict(response)
            status = job["job"]["status"]
        except Exception as e:
            status = "JOB_STATUS_NOT_FOUND"
        print("Status: " + status)
        cursor.execute(
            "UPDATE jobs SET status=? WHERE job_id=?", (status, job_id, ), )
        workflow_db.commit()
