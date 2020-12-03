import os
import sqlite3
import csv
from datetime import date

abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

plus_ten_count = 0
less_count = 0

for i in range(127, 748):
    package_name = "deplatformr-open-images-" + str(i) + ".tar"
    cursor.execute("SELECT name, cid FROM packages WHERE name=?", (package_name,))
    package = cursor.fetchone()
    if package[1] is not None:
        cursor.execute("SELECT deal_id, miner_id FROM deals WHERE payload_cid=?", (package[1],))
        deals = cursor.fetchall()
        deal_count = len(deals)
        if deal_count > 10:
            plus_ten_count += 1
        else:
            if deal_count < 3:
                less_count += 1
                print(package[0] + ": " + str(deal_count) + " deals. CID: " + package[1])

print("Number of CIDs with over 10 deals: " + str(plus_ten_count))
print("Number of CIDs with less than 3 deals: " + str(less_count))
