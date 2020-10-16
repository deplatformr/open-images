import os
import sqlite3
from datetime import date
import shutil

workflow_db_path = os.path.join(
    os.getcwd(), "deplatformr_open_images_workflow.sqlite")
images_db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(images_db_path)
images_path = ("source_data/images/")
if not os.path.exists(os.path.join(os.getcwd(), images_path + "/1")):
    os.makedirs(os.path.join(os.getcwd(), images_path + "/1"))
batches_path = ("source_data/batches/")
if not os.path.exists(os.path.join(os.getcwd(), batches_path + "/1")):
    os.makedirs(os.path.join(os.getcwd(), batches_path + "/1"))
if not os.path.exists(os.path.join(os.getcwd(), "source_data/packages/")):
    os.makedirs(os.path.join(os.getcwd(), "source_data/packages/"))
if not os.path.exists(os.path.join(os.getcwd(), "source_data/geodata/")):
    os.makedirs(os.path.join(os.getcwd(), "source_data/geodata/"))


print("Backing up Workflow database...")
today = date.today()
date_string = today.strftime("%d-%m-%Y")
shutil.copyfile(workflow_db_path, workflow_db_path + "." + date_string)
print("Backing up Images database...")
shutil.copyfile(images_db_path, workflow_db_path + "." + date_string)
