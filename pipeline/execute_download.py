import os
import sqlite3
from natsort import natsorted
from scripts.download import download_images


db_path = os.path.join(os.getcwd(), "deplatformr_open_images_downloads.sqlite")
downloads_db = sqlite3.connect(db_path)
db_path = os.path.join(
    os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
images_db = sqlite3.connect(db_path)
images_path = ("source_data/images/")
if not os.path.exists(os.path.join(os.getcwd(), images_path + "/1")):
    os.makedirs(os.path.join(os.getcwd(), images_path + "/1"))


def download():
    cursor = downloads_db.cursor()
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
    directory = get_download_directory()
    download_images(url, image_id, directory)


def get_download_directory():
    images_dir = os.path.join(os.getcwd(), images_path)
    dirs = os.listdir(images_dir)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    latest_dir = natsorted(dirs)[-1]
    count_dir = os.path.join(images_dir, latest_dir)
    path, dirs, files = next(os.walk(count_dir))
    file_count = len(files)
    if file_count > 99:
        new_dir = str(int(latest_dir) + 1)
        os.makedirs(os.path.join(images_dir, new_dir))
        return(new_dir)
    else:
        return(latest_dir)


if __name__ == "__main__":

    limit = 5
    for i in range(1, limit):
        print("Job # " + str(i) + " of " + str(limit) + ".")
        download()
