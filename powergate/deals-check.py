import os
import sqlite3
import csv
from tabulate import tabulate
from datetime import date
from pygate_grpc.client import PowerGateClient

# Connect to Powergate
api = os.getenv('POWERGATE_API')
token = os.getenv('POWERGATE_TOKEN')
user = os.getenv('POWERGATE_USER')
powergate = PowerGateClient(api, is_secure=False)

abs_path = os.getcwd()
split = os.path.split(abs_path)
workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

plus_ten_count = 0
less_count = 0
no_jobs_count = 0

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
            if deal_count < 1:
                less_count += 1
                print(package[0] + ": " + str(deal_count) + " deals.")
                print("CID: " + package[1])
                cursor.execute("SELECT * FROM jobs WHERE cid=?", (package[1],))
                jobs = cursor.fetchall()
                if len(jobs) > 0:
                    for job in jobs:
                        if job[3]=="JOB_STATUS_QUEUED":
                            print("Queued job: " + job[0] + "  " + job[2])
                        else:
                            print("Executing job: " + job[0] + "  " + job[2])
                            cursor.execute("SELECT * FROM jobs_deals WHERE job_id=?", (job[0],))
                            deals = cursor.fetchall()
                            table = []
                            for deal in deals:
                                try:
                                    message = deal[6]
                                except:
                                    message = ""
                                try:
                                    price = deal[5]
                                except:
                                    price = 0
                                try:
                                    id = deal[3]
                                except:
                                    id = "n/a"
                                table+=[(id, deal[2], deal[4], price, message)]
                            print(tabulate(table))
                else:
                    no_jobs_count += 1                    
                    powergate.config.apply(package[1], override=True, token=token)
                    print("Configuration push applied.")
                print("")

print("Number of CIDs with over 10 deals: " + str(plus_ten_count))
print("Number of CIDs with 0 deals: " + str(less_count))
print("Number of CIDs with 0 jobs: " + str(no_jobs_count))
