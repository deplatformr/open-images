from cid_status import deal_status
import os
import sqlite3

abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

for i in range(432, 442):
    package_name = "deplatformr-open-images-" + str(i) + ".tar"
    cursor.execute("SELECT name, cid FROM packages WHERE name=?", (package_name,))
    package = cursor.fetchone()
    deal_status(package[1])