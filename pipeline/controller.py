import os
import sqlite3
import shutil
from natsort import natsorted
from scripts.download import download_images
from scripts.verify import verify_checksums

db_path = os.path.join(os.getcwd(), "deplatformr_open_images_workflow.sqlite")
workflow_db = sqlite3.connect(db_path)
db_path = os.path.join(os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)
images_path = ("source_data/images/")
if not os.path.exists(os.path.join(os.getcwd(), images_path + "/1")):
    os.makedirs(os.path.join(os.getcwd(), images_path + "/1"))


def download():
    cursor = workflow_db.cursor()
    cursor.execute(
        "SELECT image_id FROM images WHERE download IS NULL LIMIT 1",)
    result = cursor.fetchone()
    image_id = result[0]
    cursor.close()
    cursor = images_db.cursor()
    cursor.execute("SELECT OriginalURL FROM open_images WHERE ImageID = ?", (image_id,),)
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
    cursor = workflow_db.cursor()
    cursor.execute(
        "SELECT image_id, filepath FROM images WHERE download = 1 AND verify_checksum IS NULL LIMIT 1",)
    result = cursor.fetchone()
    image_id = result[0]
    filepath = result[1]
    cursor.close()
    cursor = images_db.cursor()
    cursor.execute("SELECT OriginalMD5 FROM open_images WHERE ImageID = ?", (image_id,),)
    result = cursor.fetchone()
    checksum = result[0]
    cursor.close
    verify_checksums(image_id, filepath, checksum)

    return()

if __name__ == "__main__":
    download()
    verify()



