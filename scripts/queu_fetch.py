import os
import sqlite3
import requests
import shutil

current_path = os.getcwd()
sqlite_path = ("source_data/deplatformr_open_images_v6.sqlite")
db_path = os.path.join(current_path, sqlite_path)
db = sqlite3.connect(db_path)


def main():
    cursor = db.cursor()
    # Get current offset for walking the labels table
    cursor.execute(
        "SELECT value FROM configuration WHERE key = ?;", ("download_offset",),)
    offset = cursor.fetchone()

    # Retrieve the next label, alphabetically
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

    # Download each picture that uses this label
    for i in range(0, 3):
        # Check that this image and its info has not already been downloaded
        cursor.execute("SELECT status FROM workflow_status WHERE image_id = ? AND task =?;",
                       (labeled_images[i][0], "download"),)
        download_status = cursor.fetchone()
        if download_status is None:
            # Create a download directory per label
            label_dir = os.path.join(
                current_path, "/source_data/images/" + label[1] + "/")
            if not os.path.exists(label_dir):
                os.makedirs(label_dir)
            file_extentsion = os.path.split(labeled_images[i][1])
            filename = os.path.join(
                label_dir, labeled_images[i][0] + file_extension[1])
            response = requests.get(
                labeled_images[i][1], headers=user_agent, stream=True, timeout=(3, 10))
            file = open(filename, "wb")
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        else:
            continue

    return()


if __name__ == "__main__":
    main()
