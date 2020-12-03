from cid_status import deal_status
import os
import sqlite3

abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

timestamp = "2020-12-02 00:00:00.00000"
cursor.execute("SELECT name, cid FROM packages WHERE cid_timestamp > ?", (timestamp,),)
packages = cursor.fetchall()

package_count = 0

for package in packages:
    package_count+= 1
    print("Filename: " + package[0])
    deal_status(package[1])

print(str(package_count) + " packages uploaded after " + timestamp)