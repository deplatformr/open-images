import os
import sqlite3
import requests
import shutil
from datetime import datetime
import hashlib
import base64

current_path = os.getcwd()
sqlite_path = ("source_data/deplatformr_open_images_v6.sqlite")
db_path = os.path.join(current_path, sqlite_path)
db = sqlite3.connect(db_path)


def get_download_offset():
    cursor = db.cursor()
    cursor.execute(
        "SELECT value FROM configuration WHERE key = ?;", ("download_offset",),)
    offset = cursor.fetchone()
    cursor.close()

    return(offset)


def increment_download_offset(offset):
    cursor = db.cursor()
    update = int(offset[0]) + 1
    cursor.execute("UPDATE configuration SET value = ? WHERE key = ?",
                   (update, "download_offset",),)
    db.commit()

    return()


def get_download_list(offset):
    cursor = db.cursor()
    # Going alphabetically by label, get list of next set of photographs to download
    cursor.execute(
        "SELECT * FROM labels ORDER BY DisplayName ASC LIMIT ? OFFSET ?;", (1, offset[0],),)
    label = cursor.fetchone()

    # Retrieve pictures per label
    labeled_images = []

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalMD5 FROM open_images INNER JOIN test_labels_human ON test_labels_human.ImageID = open_images.ImageID WHERE test_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    labeled_images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalMD5 FROM open_images INNER JOIN validate_labels_human ON validate_labels_human.ImageID = open_images.ImageID WHERE validate_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    labeled_images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalMD5 FROM open_images INNER JOIN train_labels_human ON train_labels_human.ImageID = open_images.ImageID WHERE train_labels_human.LabelName = ?;", (label[0],),)
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
                    # Log failure in database
                    cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                        list[i][0], "download", "failure", utctime, response.status_code,),)
                    # Remove this image from fetch list
                    list[i].pop()
                    continue
                file = open(filename, "wb")
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)
                cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                    list[i][0], "download", "success", utctime, response.status_code,),)
                list[i][3] = filename
            except Exception as e:
                print("Unable to download or save " + list[i][1])
                print(e)
                # Log failure in database
                cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp, output) VALUES (?,?,?,?,?)", (
                    list[i][0], "download", "failure", utctime, e,),)
                # Remove this image from fetch list
                list[i].pop()
        else:
            continue

    db.commit()
    cursor.close()

    return(label_dir, list)


def verify_checksums(download_dir, images):
    cursor = db.cursor()

    # for i in range(0, len(images)):
    print(images)
    for i in range(0, 10):
        try:
            # Decode Open Images MD5 checksum
            open_images_md5 = base64.b64decode(images[i][2])

            # Calculate MD5 checksum for downloaded file
            with open(images[i][3], 'rb') as filehash:
                m = hashlib.md5()
                while True:
                    data = filehash.read(8192)
                    if not data:
                        break
                    m.update(data)

            # Verify checksum match
            if m.hexdigest() != open_images_md5.hex():
                utctime = datetime.utcnow()
                print("Unable to verify checksum for " + images[i][0])
                cursor.execute("INSERT INTO workflow_status (image_id, task, status, timestamp) VALUES (?,?,?,?)", (
                    list[i][0], "checksum verification", "failure", utctime,),)
                os.remove(list[i][3])
        except Exception as e:
            print(e)

        db.commit()
        cursor.close()

    return()


def main():

    # Get current offset for walking the labels table
    try:
        offset = get_download_offset()
    except Exception as e:
        print("Unable to get download offset.")
        print(e)
        return()

    # Generate a download list per label
    try:
        label, image_list = get_download_list(offset)
        print(str(len(image_list)) + " images using label '" +
              label[1] + "' are queued for download.")
    except Exception as e:
        print("Creating download list for '" + label[1] + "' failed.")
        print(e)
        return()

    # Download each picture that uses this label
    try:
        print("Downloading...")
        download_dir, images = download_images(label[1], image_list)
        # Increment the download offset
        increment_download_offset(offset)
    except Exception as e:
        print("Unable to download the images.")
        print(e)
        return()

    # Verify the MD5 checksum of the downloaded files
    try:
        print("Verifying checksums...")
        verified_images = verify_checksums(download_dir, images)
        print(len(verified_images) + " images successfully downloaded.")
    except Exception as e:
        print("Unable to verify download checksums")
        print(e)
        return()

    return(verified_images)


if __name__ == "__main__":
    main()
