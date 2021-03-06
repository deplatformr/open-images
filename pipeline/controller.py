import os
import sqlite3
from natsort import natsorted
from scripts.verify import verify_checksums
from scripts.extract import extract_metadata
from scripts.sidecar import write_metadata
from scripts.segmentations import move_segmentations
from scripts.batch import batch_size
from scripts.package import create_package
from scripts.upload import filecoin_upload

downloads_db_path = os.path.join(
    os.getcwd(), "deplatformr_open_images_downloads.sqlite")
workflow_db_path = os.path.join(
    os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
images_db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)
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


def verify():
    try:
        downloads_db = sqlite3.connect(downloads_db_path)
        cursor = downloads_db.cursor()
        cursor.execute(
            "SELECT image_id, filepath FROM images WHERE download = ? AND verify_checksum IS NULL LIMIT ?", (1, 1,),)
        result = cursor.fetchone()
        image_id = result[0]
        filepath = result[1]
        cursor.close()
        cursor = images_db.cursor()
        cursor.execute(
            "SELECT OriginalMD5 FROM open_images WHERE ImageID = ?", (image_id,),)
        result = cursor.fetchone()
        checksum = result[0]
        cursor.close
        verify_checksums(image_id, filepath, checksum)
    except Exception as e:
        print("Unable to find image for verification")
        print(e)

    return()


def extract():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT image_id, filepath FROM images WHERE verify_checksum = ? AND extract_metadata IS NULL LIMIT ?", (1, 1,),)
        result = cursor.fetchone()
        image_id = result[0]
        filepath = result[1]
        cursor.close()
        extract_metadata(image_id, filepath)
    except Exception as e:
        print("Unable to find image for metadata extraction.")
        print(e)

    return()


def sidecar():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT image_id, filepath FROM images WHERE extract_metadata = ? AND write_sidecar IS NULL LIMIT ?", (1, 1,),)
        result = cursor.fetchone()
        image_id = result[0]
        split = os.path.split(result[1])
        directory = split[0]
        cursor.close()
        write_metadata(image_id, directory)
    except Exception as e:
        print("Unable to find image for metadata writing.")
        print(e)

    return()


def segmentations():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT image_id, filepath FROM images WHERE write_sidecar = ? AND move_segmentations IS NULL LIMIT ?", (1, 1,),)
        result = cursor.fetchone()
        image_id = result[0]
        filepath = result[1]
        cursor.close()
        move_segmentations(image_id, filepath)
    except Exception as e:
        print("Unable to find segmentation files to move.")
        print(e)

    return()


def batch():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT image_id, filepath FROM images WHERE move_segmentations = ? AND batch_size IS NULL LIMIT ?", (1, 1,),)
        result = cursor.fetchone()
        cursor.close()
        image_id = result[0]
        split = os.path.split(result[1])
        directory = split[0]
        batch_dir = get_batch_directory()
        batch_size(image_id, directory, batch_dir)
    except Exception as e:
        print("Unable to find image for batch sizing.")
        print(e)

    return()


def get_batch_directory():
    batches_dir = os.path.join(os.getcwd(), batches_path)
    dirs = os.listdir(batches_dir)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    latest_dir = natsorted(dirs)[-1]
    batch_dir = os.path.join(batches_path, latest_dir)

    return(batch_dir)


def package():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT image_id, batch_size FROM images WHERE batch_size > 0 AND package_name IS NULL")
        results = cursor.fetchall()
        images = list(results)
        batch_dir = get_batch_directory()
        create_package(images, batch_dir)

    except Exception as e:
        print("Unable to find image for batching.")
        print(e)

    return()


def upload():
    try:
        cursor = workflow_db.cursor()
        cursor.execute(
            "SELECT name FROM packages WHERE cid IS NULL LIMIT ?", (1,),)
        result = cursor.fetchone()
        if result is None:
            return()
        else:
            filecoin_upload(result[0])

    except Exception as e:
        print("Unable to find package for Filecoin upload.")
        print(e)

    return()


if __name__ == "__main__":

    limit = 5
    for i in range(1, limit):
        print("Job # " + str(i) + " of " + str(limit) + ".")
        verify()
        extract()
        sidecar()
        segmentations()
        batch()
        package()
        upload()
