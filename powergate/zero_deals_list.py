import os
import sqlite3
from datetime import datetime
from pygate_grpc.client import PowerGateClient
import time
import sys

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
cursor.execute("SELECT cid, name FROM packages WHERE cid IS NOT NULL")
cids = cursor.fetchall()

repush_count = 0
zero_count = 0

for cid in cids:
    cursor.execute(
        "SELECT COUNT(*) FROM deals WHERE payload_cid = ?", (cid[0], ), )
    count = cursor.fetchone()
    if count[0] == 0:
        zero_count += 1
        print(cid[1] + " - " + cid[0] + " has " +
              str(count[0]) + " active deals.")

    # TAKE SOME ACTION BASED ON NUMBER OF ACTIVE DEALS

    """
    # IF TOO MANY
    # SHOW CANCEL COMMAND
    if count[0] >= 7:
        cid = cid[0]

        cursor.execute(
            "SELECT job_id, status FROM jobs WHERE cid = ?", (cid,),)
        jobs = cursor.fetchall()
        if len(jobs) > 0:
            for job in jobs:
                # SHOW JOB STATUS
                print("Job ID: " + job[0])
                print(job[1])

                # SHOW CANCEL COMMAND
                if job[1] == "JOB_STATUS_EXECUTING" or job[1] == "JOB_STATUS_QUEUED":
                    print("POW_SERVERADDRESS=" + api +
                          " pow ffs cancel " + job[0] + " -t " + token)
    """

    # IF TOO FEW
    if count[0] == 0:
        package = cid[1]
        cid = cid[0]

        cursor.execute(
            "SELECT job_id, status FROM jobs WHERE cid = ?", (cid,),)
        jobs = cursor.fetchall()
        if len(jobs) > 0:
            for job in jobs:
                # SHOW JOB STATUS
                print("Job ID: " + job[0])
                print(job[1])
                """
                # SHOW CANCEL COMMAND
                if job[1] == "JOB_STATUS_EXECUTING" or job[1] == "JOB_STATUS_QUEUED":
                    print("POW_SERVERADDRESS=" + api +
                          " pow ffs cancel " + job[0] + " -t " + token)
                """
        """
        # REPUSH IF TOO FEW
        if job[1] != "JOB_STATUS_EXECUTING" and job[1] != "JOB_STATUS_QUEUED":
            try:
                interval = 10
                utctime = datetime.utcnow()
                job = powergate.ffs.push(cid, token, override=True)
                print("Repushed " + package + " - " + cid + " to Filecoin.")
                print("Job ID: " + job.job_id)
                utctime = datetime.utcnow()
                cursor = workflow_db.cursor()
                cursor.execute("INSERT INTO jobs (job_id, cid, ffs, timestamp, status) VALUES (?,?,?,?,?)",
                               (job.job_id, cid, ffs, utctime, "JOB_STATUS_EXECUTING",),)
                workflow_db.commit()
                print("Waiting " + str(interval) +
                      " seconds before next push.")
                time.sleep(interval)
                repush_count += 1
            except Exception as e:
                print("Repush of Job " + job[0] + " failed. Aborting queu.")
                print(e)
                workflow_db.close()
                sys.exit()
        else:
            print("Job " + job[1] + " is still executing or queued.")
        """

if repush_count > 0:
    print("Repushed " + str(repush_count) + " CIDs.")

if zero_count > 0:
    print(str(zero_count) + " CIDs without deals.")

workflow_db.close()
