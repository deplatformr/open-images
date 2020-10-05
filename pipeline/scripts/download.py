import os
import sqlite3
import requests
import shutil
from datetime import datetime

def download_images(url, image_id, directory):
    abs_path = os.getcwd()
    sqlite_path = ("deplatformr_open_images_workflow.sqlite")
    db_path = os.path.join(abs_path, sqlite_path)
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    images_path = ("source_data/images/")

    try:
        baseurl, file_extension = os.path.splitext(url)
        filepath = os.path.join(images_path + directory + "/", image_id + file_extension)
        response = requests.get(url, stream=True, timeout=(3, 10))
        utctime = datetime.utcnow()
        if response.status_code != 200:
            # Log download failure in database
            cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ? WHERE image_id = ?", (False, utctime, response.status_code, image_id,),)
            db.commit()
            db.close()
            return()
        file = open(filepath, "wb")
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ?, filepath = ? WHERE image_id = ?", (True, utctime, response.status_code, filepath, image_id,),)

    except Exception as e:
        print("Unable to download or save " + str(image_id))
        print(e)
        # Log failure in database
        utctime = datetime.utcnow()
        cursor.execute("UPDATE images SET download = ?, download_timestamp = ?, http_code = ? WHERE image_id = ?", (False, utctime, str(e), image_id,),)

    db.commit()
    db.close()

    return()