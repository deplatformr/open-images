import os
import sqlite3
import requests
import shutil
from datetime import datetime

current_path = os.getcwd()
sqlite_path = ("source_data/deplatformr_open_images_v6.sqlite")
db_path = os.path.join(current_path, sqlite_path)
db = sqlite3.connect(db_path)


def get_download_list(offset):
    cursor = db.cursor()
    # Going alphabetically by label, get list of next set of photographs to download
    cursor.execute(
        "SELECT * FROM labels ORDER BY DisplayName ASC LIMIT ? OFFSET ?;", (1, offset[0],),)
    label = cursor.fetchone()

    # Retrieve pictures per label
    labeled_images = []

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN test_labels_human ON test_labels_human.ImageID = open_images.ImageID WHERE test_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    labeled_images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN validate_labels_human ON validate_labels_human.ImageID = open_images.ImageID WHERE validate_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    labeled_images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN train_labels_human ON train_labels_human.ImageID = open_images.ImageID WHERE train_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    labeled_images += results

    cursor.close()

    return(label, labeled_images)

def download_images(label, list):

    cursor = db.cursor()
    # Download each picture that uses the same label
    # for i in range(0, len(list)):
    for i in range(0, 20):
        # Check that this image and its info has not already been downloaded
        cursor.execute("SELECT status FROM workflow_status WHERE image_id = ? AND task =?;",
                       (list[i][0], "download"),)
        download_status = cursor.fetchone()
        if download_status is None:
            try:
                # Create a download directory per label
                label_dir = os.path.join(
                    os.getcwd(), "source_data/images/" + label + "/")
                if not os.path.exists(label_dir):
                    os.makedirs(label_dir)
                url, file_extension = os.path.splitext(list[i][1])
                filename = os.path.join(
                    label_dir, list[i][0] + file_extension)
                response = requests.get(
                    list[i][1], stream=True, timeout=(3, 10))
                utctime = datetime.utcnow()
                if response.status_code != 200:
                    cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                        list[i][0], "download", "failure", utctime, response.status_code,),)
                    continue
                file = open(filename, "wb")
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                    list[i][0], "download", "success", utctime, response.status_code,),)
            except Exception as e:
                print("Unable to download or save" + list[i][1])
                print(e)
                cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                    list[i][0], "download", "failure", utctime, response.status_code,),)
        else:
            continue

    db.commit()
    cursor.close()

    return(label_dir)


def main():
    cursor = db.cursor()
    # Get current offset for walking the labels table
    cursor.execute(
        "SELECT value FROM configuration WHERE key = ?;", ("download_offset",),)
    offset = cursor.fetchone()

    try:
        # Generate the download list for the next label
        label, images = get_download_list(offset)

    except Exception as e:
        print("Creating download list for '" + label[1] + "' failed.")
        print(e)

    try:
        # Download each picture that uses this label
        download_dir = download_images(label[1], images)

        # Update the download offset
        update = int(offset[0]) + 1
        cursor.execute("UPDATE configuration SET value = ? WHERE key = ?",
                       (update, "download_offset",),)
        db.commit()
    except Exception as e:
        print("Unable to download the images.")
        print(e)

    cursor.close()

    return()


if __name__ == "__main__":
    main()
