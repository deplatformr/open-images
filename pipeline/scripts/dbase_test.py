import sqlite3
import os

db_path = os.path.join(os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)

cursor = workflow_db.cursor()
cursor.execute(
    "SELECT name FROM packages WHERE cid IS NOT NULL LIMIT ?", (1,),)
    result = cursor.fetchone()
    if result is None:
        print("nothing found")
        return()
    else:
        print("Uploading package " + result[0] + " to Filecoin.")
