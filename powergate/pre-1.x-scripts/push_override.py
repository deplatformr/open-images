import os
import sys
import sqlite3
from datetime import datetime
from pygate_grpc.client import PowerGateClient


def push(cid):

    try:
        abs_path = os.getcwd()
        split = os.path.split(abs_path)
        workflow_db_path = os.path.join(
            split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(workflow_db_path)

        api = os.getenv('POWERGATE_API')
        ffs = os.getenv('POWERGATE_FFS')
        token = os.getenv('POWERGATE_TOKEN')
        powergate = PowerGateClient(api, is_secure=False)

        utctime = datetime.utcnow()

        job = powergate.ffs.push(cid, token, override=False)
        print("Repushed CID " + cid + " to Filecoin.")
        print("Job ID: " + job.job_id)
        utctime = datetime.utcnow()
        cursor = workflow_db.cursor()
        cursor.execute("INSERT INTO jobs (job_id, cid, ffs, timestamp, status) VALUES (?,?,?,?,?)",
                       (job.job_id, cid, ffs, utctime, "JOB_STATUS_EXECUTING",),)
        workflow_db.commit()
        workflow_db.close()

    except Exception as e:
        print("Repush of CID " + cid + " failed.")
        print(e)

    return()


if __name__ == "__main__":

    try:
        if sys.argv[1] is None:
            print("Please provide a CID.")
            sys.exit(0)
        else:
            push(str(sys.argv[1]))
    except Exception as e:
        print("Unable to repush CID " + str(sys.argv[1]) + " to Filecoin.")
        print(e)
