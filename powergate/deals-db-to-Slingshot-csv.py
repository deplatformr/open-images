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
cursor.execute(
    "SELECT deal_id, payload_cid, piece_size, miner_id from deals ORDER BY payload_cid;")
deals = cursor.fetchall()


print(str(len(deals)) + " storage deals found.")

today = date.today()
date_string = today.strftime("%b-%d-%Y")

filename = "slingshot2-deals-deplatformer-" + date_string + ".csv"
print("Writing to " + filename + ".")

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # write column headers
    csvwriter.writerow(['Deal ID', 'Miner ID', 'Payload CID', 'Filename', 'File format', 'Deal Size (in bytes)', 'Deal Date (UTC)', 'Curated Dataset', '10+ Deals?'])

    cid_count = 0
    previous_cid = ""
    for deal in deals:
        cursor.execute(
            "SELECT name, cid_timestamp from packages where cid = ?", (deal[1],),)
        package = cursor.fetchone()
        utc_date = package[1][:-10]
        if deal[1] == previous_cid:
            cid_count += 1
        else:
            cid_count = 1
        previous_cid = deal[1]
        if cid_count > 10:
            size = 0
            ten = "10+ deals"
        else:
            size = deal[2]
            ten = ""
        csvwriter.writerow([deal[0], deal[3], deal[1], package[0],
                            ".tar containing .jpg, .png, and .jsonld", size, utc_date, "Google Open Images", ten])
