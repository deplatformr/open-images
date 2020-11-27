from pygate_grpc.client import PowerGateClient
import os
import sys
import sqlite3
from datetime import datetime


def filecoin_upload(package):

    try:
        abs_path = os.getcwd()
        package_dir = os.path.join(abs_path, "source_data/packages")
        upload_file = os.path.join(package_dir, package)

        api = os.getenv('POWERGATE_API')
        token = os.getenv('POWERGATE_TOKEN')
        powergate = PowerGateClient(api, is_secure=False)

        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)

        staged_file = powergate.data.stage_file(upload_file, token)
        job = powergate.config.apply(staged_file.cid, override=False, token=token)

        print("Uploaded package " + package + " to Filecoin.")
        print("CID: " + staged_file.cid)
        print("Job ID: " + job.jobId)
        utctime = datetime.utcnow()
        cursor = workflow_db.cursor()
        cursor.execute("UPDATE packages SET cid = ?, cid_timestamp = ? WHERE name = ?",
                       (staged_file.cid, utctime, package,),)
        cursor.execute("INSERT INTO jobs (job_id, cid, ffs, timestamp, status) VALUES (?,?,?,?,?)",
                       (job.jobId, staged_file.cid, None, utctime, "JOB_STATUS_EXECUTING",),)
        workflow_db.commit()
        workflow_db.close()
        return("Success")

    except Exception as e:
        print("Unable to push package " + package + " to Filecoin.")
        print(e)
        return("Failure")


if __name__ == "__main__":

    try:
        if sys.argv[1] is None:
            print("Please provide a package name.")
            sys.exit(0)
        else:
            filecoin_upload(str(sys.argv[1]))
    except Exception as e:
        print("Unable to push package " + str(sys.argv[1]) + " to Filecoin.")
        print(e)
