import exifread
import os
import sqlite3

img_dir = os.path.join(os.getcwd(), "source_data/images/1/")
images = os.listdir(img_dir)

for image in images:
    # Open image file for reading (binary mode)
    f = open(img_dir + image, 'rb')

    disk_size = os.path.getsize(img_dir + image)
    split = os.path.split(img_dir + image)
    image_id, extension = os.path.splitext(split[1])

    db_path = os.path.join(
        os.getcwd(), "source_data/deplatformr_open_images_v6.sqlite")
    images_db = sqlite3.connect(db_path)
    cursor = images_db.cursor()
    cursor.execute(
        "SELECT OriginalSize FROM open_images WHERE ImageID = ?", (image_id,),)
    open_image_size = cursor.fetchone()

    print(image_id)
    print(open_image_size[0])
    print(disk_size)
    print("-----")
