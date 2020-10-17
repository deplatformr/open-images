import os
import sqlite3
from datetime import datetime


abs_path = os.getcwd()
split = os.path.split(abs_path)

workflow_db_path = os.path.join(
    split[0], "pipeline/deplatformr_open_images_workflow.sqlite")

workflow_db = sqlite3.connect(workflow_db_path)
cursor = workflow_db.cursor()

utctime = datetime.utcnow()

with open("updated_jobs.txt", "r") as jobs_list:
    jobs = jobs_list.readlines()
    for job in jobs:
        split = job.split(",")
        cursor.execute("UPDATE jobs set job_id=?, timestamp=?, status=? WHERE cid=?",
                       (split[1], utctime, "Executing", split[0],),)
        workflow_db.commit()
workflow_db.close()
