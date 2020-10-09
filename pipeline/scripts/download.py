import os
import sqlite3
import requests
import shutil
from datetime import datetime


def download_images(url, image_id, directory):
    abs_path = os.getcwd()
    images_path = ("source_data/images/")

    try:
        baseurl, file_extension = os.path.splitext(url)
        filepath = os.path.join(
            images_path + directory + "/", image_id + file_extension)
        response = requests.get(url, stream=True, timeout=(3, 10))
        utctime = datetime.utcnow()
        if response.status_code != 200:
            # Log download failure in database
            sqlite_path = ("deplatformr_open_images_workflow.sqlite")
            db_path = os.path.join(abs_path, sqlite_path)
            workflow_db = sqlite3.connect(db_path)
            cursor = workflow_db.cursor()
            cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ? WHERE image_id = ?",
                           (False, utctime, response.status_code, image_id,),)
            workflow_db.commit()
            workflow_db.close()
            print("Unable to download image " + image_id +
                  ". Received " + response.status_code + " code.")

            return()
        file = open(filepath, "wb")
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        # Record the updated filename that uses Open Images ID as filename
        db_path = os.path.join(
            abs_path, "source_data/deplatformr_open_images_v6.sqlite")
        images_db = sqlite3.connect(db_path)
        cursor = images_db.cursor()
        filepath_split = os.path.split(filepath)
        filename = filepath_split[1]
        cursor.execute(
            "UPDATE open_images SET filename = ? WHERE ImageID = ?", (filename, image_id,),)
        images_db.commit()
        images_db.close()
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ?, filepath = ? WHERE image_id = ?",
                       (True, utctime, response.status_code, filepath, image_id,),)
        workflow_db.commit()
        workflow_db.close()
        print("Downloaded image " + image_id)

    except Exception as e:
        utctime = datetime.utcnow()
        print("Unable to download or save " + image_id)
        print(e)
        # Log failure in database
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ? WHERE image_id = ?",
                       (False, utctime, str(e), image_id,),)
        workflow_db.commit()
        workflow_db.close()

    return()


def get_directory():
    images_dir = os.path.join(os.getcwd(), images_path)
    dirs = os.listdir(images_dir)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    latest_dir = natsorted(dirs)[-1]
    count_dir = os.path.join(images_dir, latest_dir)
    path, dirs, files = next(os.walk(count_dir))
    file_count = len(files)
    if file_count > 999:
        new_dir = str(int(latest_dir) + 1)
        os.makedirs(os.path.join(images_dir, new_dir))
        return(new_dir)
    else:
        return(latest_dir)
