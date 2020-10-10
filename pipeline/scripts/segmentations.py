
import os
import shutil
import sqlite3
from datetime import datetime


def move_segmentations(image_id, filepath):
    try:
        abs_path = os.getcwd()
        segmentations_dir = os.path.join(
            abs_path, "source_data/segmentations/")
        split = os.path.split(filepath)
        dest_dir = os.path.join(abs_path, split[0])

        db_path = os.path.join(
            abs_path, "source_data/deplatformr_open_images_v6.sqlite")
        images_db = sqlite3.connect(db_path)
        cursor = images_db.cursor()

        move = False

        cursor.execute(
            "SELECT MaskPath FROM train_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "train-masks-" + image_id[0])
            for result in results:
                shutil.copyfile(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))
            move = True

        cursor.execute(
            "SELECT MaskPath FROM validate_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "validation-masks-" + image_id[0])
            for result in results:
                shutil.copyfile(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))
            move = True

        cursor.execute(
            "SELECT MaskPath FROM test_segmentations where ImageID = ?", (image_id,),)
        results = cursor.fetchall()

        if len(results) > 0:
            source_dir = os.path.join(
                segmentations_dir, "test-masks-" + image_id[0])
            for result in results:
                shutil.copyfile(os.path.join(
                    source_dir, result[0]), os.path.join(dest_dir, result[0]))
            move = True

        cursor.close()
        images_db.close()

        # Log successful move or non-move (if no segmentation files were found)
        utctime = datetime.utcnow()
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute(
            "UPDATE images SET move_segmentations = ?, move_segmentations_timestamp = ? WHERE image_id = ?", (True, utctime, image_id,),)
        if move:
            print("Moved segmentation files for image " + image_id)
        else:
            print("No segmentation files to move for image " + image_id)

    except Exception as e:
        print("Unable to move segmentation files for image " + image_id)
        print(e)
        utctime = datetime.utcnow()
        # Log failure in database
        abs_path = os.getcwd()
        db_path = os.path.join(
            abs_path, "deplatformr_open_images_workflow.sqlite")
        workflow_db = sqlite3.connect(db_path)
        cursor = workflow_db.cursor()
        cursor.execute(
            "UPDATE images SET move_segmentations = ?, move_segmentations_timestamp = ? WHERE image_id = ?", (False, utctime, image_id,),)

    workflow_db.commit()
    workflow_db.close()

    return()
