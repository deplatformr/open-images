import os
import sqlite3
from scripts.upload import filecoin_upload

workflow_db_path = os.path.join(
    os.getcwd(), "deplatformr_open_images_workflow.sqlite")


def upload():
    try:
        workflow_db = sqlite3.connect(workflow_db_path)
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT name FROM packages WHERE cid IS NULL")
        results = cursor.fetchall()
        if results is None:
            print("No packages ready for Filecoin upload yet.")
            return()
        else:
            count = 0
            for result in results:
                count += 1
                print("Uploading package # " + count + " of " +
                      str(len(results)) + " to Filecoin.")
                filecoin_upload(result[0])

    except Exception as e:
        print("Unable to find package for Filecoin upload.")
        print(e)

    return()


if __name__ == "__main__":
    upload()
