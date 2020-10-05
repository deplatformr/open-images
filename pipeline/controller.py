import os
import sqlite3
import shutil
from natsort import natsorted
from scripts.download import download_images

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
        "SELECT ImageID FROM images LIMIT 1 WHERE download = ?", (None,),)
    image_id = cursor.fetchone()
    cursor.close()
    cursor = images_db.cursor()
    cursor.execute("SELECT OriginalURL FROM open_images WHERE ImageID = ?", (image_id,),)
    directory = get_directory()

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

def main():

    download()

if __name__ == "__main__":
    get_directory()


