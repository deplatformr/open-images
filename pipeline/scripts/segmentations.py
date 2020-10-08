
import os
import shutil
import sqlite3

def move_segmentations(image_id, filepath):

    try:
        abs_path = os.getcwd()
        segmentations_dir = os.path.join(abs_path, "source_data/segmentations/")
        split = os.path.split(filepath)
        dest_dir = os.path.join(abs_path, split[0])

        db_path = os.path.join(
            abs_path, "source_data/deplatformr_open_images_v6.sqlite")
        images_db = sqlite3.connect(db_path)
        cursor = images_db.cursor()

        cursor.execute(
            "SELECT MaskPath FROM train_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "train-masks-" + image_id[0])
            for result in results:
                shutil.move(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))

        cursor.execute(
            "SELECT MaskPath FROM validate_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "validation-masks-" + image_id[0])
            for result in results:
                shutil.move(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))

        cursor.execute(
            "SELECT MaskPath FROM test_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "test-masks-" + image_id[0])
            for result in results:
                shutil.move(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))

        cursor.close()
        images_db.close()

        # TODO: Update workflow dbase

    except Exception as e:
        print("Unable to move segmentation files for image " + image_id)
        print(e)

        # TODO: Update workflow dbase

    return()
