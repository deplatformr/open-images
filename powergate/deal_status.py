import os
import sqlite3
from datetime import datetime
from pygate_grpc.client import PowerGateClient
import time

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
cursor.execute("SELECT cid, name FROM packages WHERE cid IS NOT NULL")
cids = cursor.fetchall()

for cid in cids:
    cursor.execute(
        "SELECT COUNT(*) FROM deals WHERE payload_cid = ?", (cid[0], ), )
    count = cursor.fetchone()
    print(cid[1] + " - " + cid[0] + " has " + str(count[0]) + " active deals.")

    # TAKE SOME ACTION BASED ON NUMBER OF ACTIVE DEALS
    # CANCEL IF TOO MANY
    """ All >= & jobs cancelled on Oct 17 21:00
    if count[0] >= 7:
        cursor.execute("SELECT job_id FROM jobs WHERE cid = ?", (cid[0],),)
        jobs = cursor.fetchall()
        for job in jobs:
            print("POW_SERVERADDRESS=" + api +
                  " pow ffs cancel " + job[0] + " -t " + token)
    """
    # CANCEL IF TOO LITTLE, THEN REPUSH
    if count[0] < 5:
        interval = 30
        package = cid[1]
        cid = cid[0]
        if cid != "QmPg9bg8DGMALcGAHET2pFyNPbJUznRJLaCMhyeM9Ncoxp" and cid != "Qmc57MM3wwGDCra8b35g4fAgvcSM3rcbhGizHm44ggLJVk":
            """
            cursor.execute("SELECT job_id FROM jobs WHERE cid = ?", (cid[0],),)
            jobs = cursor.fetchall()
            if len(jobs) > 0:
                for job in jobs:
                    print("POW_SERVERADDRESS=" + api +
                          " pow ffs cancel " + job[0] + " -t " + token)
            """
            utctime = datetime.utcnow()

            job = powergate.ffs.push(cid, token, override=True)
            print("Repushed " + package + " - " + cid + " to Filecoin.")
            print("Job ID: " + job.job_id)
            utctime = datetime.utcnow()
            cursor = workflow_db.cursor()
            cursor.execute("INSERT INTO jobs (job_id, cid, ffs, timestamp, status) VALUES (?,?,?,?,?)",
                           (job.job_id, cid, ffs, utctime, "Executing",),)
            workflow_db.commit()
            print("Waiting " + str(interval) + " seconds before next push.")
            time.sleep(interval)

workflow_db.close()
