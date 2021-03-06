import os
import shutil
import sqlite3


def batch_size(image_id, img_dir, batch_dir):
    abs_path = os.getcwd()
    db_path = os.path.join(abs_path, "deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)

    try:
        path, dirs, files = next(os.walk(os.path.join(abs_path, img_dir)))
        batch_size = 0
        batch_dir = os.path.join(abs_path, batch_dir)

        geo = False
        db_path = os.path.join(
            abs_path, "source_data/deplatformr_open_images_v6.sqlite")
        images_db = sqlite3.connect(db_path)
        cursor = images_db.cursor()
        cursor.execute(
            "SELECT latitude from open_images where ImageID = ?", (image_id,),)
        latitude = cursor.fetchone()
        images_db.close()
        if latitude[0] is not None:
            geo = True
            print("Found geodata in image " + image_id + ". Making copy.")

        # Loop over files in the directory
        for file in files:
            if file.find(image_id) != -1:
                filepath = os.path.join(path, file)
                batch_size += os.path.getsize(filepath)
                if geo:
                    shutil.copy(filepath, os.path.join(
                        os.getcwd(), "source_data/geodata"))
                shutil.move(filepath, os.path.join(batch_dir, file))

        cursor = workflow_db.cursor()
        cursor.execute("UPDATE images SET batch_size = ? WHERE image_id = ?",
                       (batch_size, image_id,),)
        print("Calculated batch size for image " + image_id)
        workflow_db.commit()
        workflow_db.close()

        return("Success")

    except Exception as e:
        print("Unable to get batch size for image " + image_id)
        print(e)
        cursor = workflow_db.cursor()
        cursor.execute(
            "UPDATE images SET batch_size = ? WHERE image_id = ?", (None, image_id,),)
        workflow_db.commit()
        workflow_db.close()

        return("Failure")
