import os
import shutil
import sqlite3


def batch_size(image_id, img_dir, batch_dir):
    abs_path = os.getcwd()
    db_path = os.path.join(abs_path, "deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)

    try:
        path, dirs, files = next(os.walk(os.path.join(abs_path, img_dir)))
        print(path)

        batch_size = 0

        # Loop over files in the directory
        for file in files:
            if file.find(image_id) != -1:
                filepath = os.path.join(path, file)
                batch_size += os.path.getsize(filepath)
                # TODO make a seperate copy for images with GeoData
                shutil.move(filepath, os.path.join(batch_dir, file))

        cursor = workflow_db.cursor()
        cursor.execute("UPDATE images SET batch_size = ? WHERE image_id = ?",
                       (batch_size, image_id,),)
        print("Calculated batch size for image " + image_id)

    except Exception as e:
        print("Unable to get batch size for image " + image_id)
        print(e)
        cursor.execute(
            "UPDATE images SET batch_size = ? WHERE image_id = ?", (None, image_id,),)

    workflow_db.commit()
    workflow_db.close()

    return()
