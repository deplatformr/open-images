import os
import sqlite3
import time
import sys
from scripts.upload import filecoin_upload

workflow_db_path = os.path.join(
    os.getcwd(), "deplatformr_open_images_workflow.sqlite")
interval = 60


def upload():
    try:
        workflow_db = sqlite3.connect(workflow_db_path)
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT name FROM packages WHERE cid IS NULL LIMIT ?", (1,),)
        result = cursor.fetchone()
        if len(result) == 0:
            print("No packages ready for Filecoin upload yet.")
            return()
        else:
            print("Uploading package " + result[0] + " to Filecoin.")
            status = filecoin_upload(result[0])
            if status == "Failure":
                print("Upload unsuccessful. Aborting job.")
                sys.exit()

    except Exception as e:
        print("Unable to find package for Filecoin upload.")
        print(e)
        sys.exit()

    return()

def upload_all():
    try:
        workflow_db = sqlite3.connect(workflow_db_path)
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT name FROM packages WHERE cid IS NULL")
        results = cursor.fetchall()
        if len(results) == 0:
            print("No packages ready for Filecoin upload yet.")
            return()
        else:
            count = 0
            for result in results:
                count += 1
                print("Uploading package # " + str(count) +
                      " of " + str(len(results)) + " to Filecoin.")
                status = filecoin_upload(result[0])
                if status == "Success":
                    print("Waiting " + str(interval) +
                          " seconds before next upload.")
                    time.sleep(interval)
                else:
                    print("Upload unsuccessful. Aborting queu.")
                    sys.exit()

    except Exception as e:
        print("Unable to find package for Filecoin upload.")
        print(e)
        sys.exit()

    return()

if __name__ == "__main__":
    job_limit = 10

    for i in range(1, job_limit):
        upload()