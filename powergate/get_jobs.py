import os
import sqlite3
from pygate_grpc.client import PowerGateClient


api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')


powergate = PowerGateClient(api, is_secure=True)


abs_path = os.getcwd()
split = os.path.split(abs_path)

workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")

workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

cursor.execute("SELECT name, cid FROM packages WHERE cid IS NOT NULL")
packages = cursor.fetchall()

for package in packages:
    try:
        cursor.execute("SELECT job_id FROM jobs WHERE cid=?", (package[1],),)
        jobs = cursor.fetchall()
        print(package[0] + "(CID: " + package[1] +
              ") has " + str(len(jobs)) + " jobs.")
        for job in jobs:
            print("Job ID: " + job[0])
            try:
                job = powergate.ffs.get_storage_job(jid=job[0], token=token)
                print(job)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
