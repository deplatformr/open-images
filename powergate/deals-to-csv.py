import os
import sqlite3
import csv

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
filename = "slingshot1-deals-deplatformr-21-Oct-2020" + ".csv"
print("Writing to " + filename + ".")

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # write column headers
    csvwriter.writerow(['Deal ID', 'Miner ID', 'Payload CID', 'Filename', 'File format', 'CID Size (bytes)', 'Date stored (UTC)',
                        'Curated Dataset'])

    for deal in deals:
        cursor.execute(
            "SELECT name, cid_timestamp from packages where cid = ?", (deal[1],),)
        package = cursor.fetchone()
        utc_date = package[1][:-10]
        csvwriter.writerow([deal[0], deal[3], deal[1], package[0],
                            ".tar containing .jpg, .png, and .jsonld", deal[2], utc_date, "Google Open Images"])
