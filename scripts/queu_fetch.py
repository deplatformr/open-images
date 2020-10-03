import os
import sqlite3

current_path = os.getcwd()
sqlite_path = ("source_data/deplatformr_open_images.sqlite")
db_path = os.path.join(current_path, sqlite_path)
db = sqlite3.connect(db_path)
offset = 2
limit = 1


def main():
    cursor = db.cursor()
    # Retrieve labels alphabetically
    cursor.execute(
        "SELECT * FROM labels ORDER BY DisplayName ASC LIMIT ? OFFSET ?;", (limit, offset,),)
    label = cursor.fetchone()

    # Retrieve pictures per label
    images = []

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN test_labels_human ON test_labels_human.ImageID = open_images.ImageID WHERE test_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN validate_labels_human ON validate_labels_human.ImageID = open_images.ImageID WHERE validate_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    images += results

    cursor.execute(
        "SELECT open_images.ImageID, OriginalURL, OriginalSize FROM open_images INNER JOIN train_labels_human ON train_labels_human.ImageID = open_images.ImageID WHERE train_labels_human.LabelName = ?;", (label[0],),)
    results = cursor.fetchall()
    images += results

    for i in range(0, len(images)):
        print(i, images[i][0])
    print(len(images))
    print(i)
    return()


if __name__ == "__main__":
    main()
