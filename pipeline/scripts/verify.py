import os
import sqlite3
from datetime import datetime
import base64
import hashlib


def verify_checksums(image_id, filepath, checksum):
    abs_path = os.getcwd()
    db_path = os.path.join(abs_path, "deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)
    cursor = workflow_db.cursor()
    image_path = os.path.join(abs_path, filepath)

    try:
        # Generate MD5 checksum for downloaded file
        with open(image_path, 'rb') as filehash:
            m = hashlib.md5()
            while True:
                data = filehash.read(8192)
                if not data:
                    break
                m.update(data)

        # Decode Open Images checksum from Base64
        open_images_md5 = base64.b64decode(checksum)

        # Compare values
        utctime = datetime.utcnow()
        if m.hexdigest() == open_images_md5.hex():
            cursor.execute(
                "UPDATE images SET verify_checksum = ?, verify_checksum_timestamp = ? WHERE image_id = ?", (True, utctime, image_id,),)
            workflow_db.commit()
            workflow_db.close()
            print("Verified MD5 checksum for image " + image_id)
            return("Success")
        else:
            cursor.execute(
                "UPDATE images SET verify_checksum = ?, verify_checksum_timestamp = ? WHERE image_id = ?", (False, utctime, image_id,),)
            workflow_db.commit()
            workflow_db.close()
            print("Failed to match checksum " +
                  m.hexdigest() + " for image " + image_id + ".")
            return("Failure")

    except Exception as e:
        utctime = datetime.utcnow()
        cursor.execute(
            "UPDATE images SET verify_checksum = ?, verify_checksum_timestamp = ? WHERE image_id = ?", (False, utctime, image_id,),)
        workflow_db.commit()
        workflow_db.close()
        print("Failed to match checksum " +
              m.hexdigest() + " for image " + image_id + ".")
        print(e)
        return("Failure")
