import os
import sqlite3
import shutil
from natsort import natsorted
from scripts.download import download_images
from scripts.verify import verify_checksums
from scripts.extract import extract_metadata

db_path = os.path.join(os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)
images_path = ("source_data/images/")
if not os.path.exists(os.path.join(os.getcwd(), images_path + "/1")):
    os.makedirs(os.path.join(os.getcwd(), images_path + "/1"))


def download():
    cursor = workflow_db.cursor()
    cursor.execute(
        "SELECT image_id FROM images WHERE download IS NULL LIMIT ?", (1,),)
    result = cursor.fetchone()
    image_id = result[0]
    cursor.close()
    cursor = images_db.cursor()
    cursor.execute(
        "SELECT OriginalURL FROM open_images WHERE ImageID = ?", (image_id,),)
    result = cursor.fetchone()
    url = result[0]
    cursor.close
    directory = get_directory()
    download_images(url, image_id, directory)


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


def verify():
    try:
        cursor = workflow_db.cursor()
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


if __name__ == "__main__":

    for i in range(1, 10):
        print("verify " + str(i))  # debug
        verify()
    for i in range(1, 10):
        print("extract " + str(i))  # debug
        extract()
