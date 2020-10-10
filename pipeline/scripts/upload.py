from pygate_grpc.client import PowerGateClient
from pygate_grpc.ffs import get_file_bytes, bytes_to_chunks
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
        ffs = os.getenv('POWERGATE_FFS')
        token = os.getenv('POWERGATE_TOKEN')
        powergate = PowerGateClient(api, False)

        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)

        iter = get_file_bytes(upload_file)
        stage = powergate.ffs.stage(bytes_to_chunks(iter), token)

        job = powergate.ffs.push(stage.cid, token)
        print("Uploaded package " + package + " to Filecoin.")
        print("CID: " + stage.cid)
        print("Job ID: " + job.job_id)
        utctime = datetime.utcnow()
        cursor = workflow_db.cursor()
        cursor.execute("UPDATE packages SET cid = ?, cid_timestamp = ? WHERE name = ?",
                       (stage.cid, utctime, package,),)
        cursor.execute("INSERT INTO jobs (job_id, cid, timestamp, status) VALUES (?,?,?,?)",
                       (job.job_id, stage.cid, utctime, "initiated",),)
        workflow_db.commit()
        workflow_db.close()

    except Exception as e:
        print("Unable to push package " + package + " to Filecoin.")
        print(e)

    return()


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
