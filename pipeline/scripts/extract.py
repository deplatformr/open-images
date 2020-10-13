import exifread
import os
import mimetypes
import sqlite3
from datetime import datetime


def extract_metadata(image_id, filepath):
    abs_path = os.getcwd()
    db_path = os.path.join(abs_path, "deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)
    image_path = os.path.join(abs_path, filepath)

    try:

        try:
            get_mimetype = mimetypes.guess_type(image_path)
            mimetype = get_mimetype[0]
        except:
            mimetype = None

        # Return Exif tags
        f = open(image_path, 'rb')
        exif_tags = exifread.process_file(f)
        try:
            width = str(exif_tags.get("EXIF ExifImageWidth"))
        except IndexError:
            width = None
        try:
            height = str(exif_tags.get("EXIF ExifImageLength"))
        except IndexError:
            height = None
        try:
            xresolution = str(exif_tags.get("Image XResolution"))
            yresolution = str(exif_tags.get("Image YResolution"))
            resolution = xresolution + " x " + yresolution
        except IndexError:
            resolution = None
        try:
            if exif_tags.get("EXIF DateTimeOriginal") is None:
                created = str(exif_tags.get("Image DateTime"))
            else:
                created = str(exif_tags.get("EXIF DateTimeOriginal"))
        except IndexError:
            created = None
        try:
            description = str(exif_tags.get("Image ImageDescription"))
        except IndexError:
            description = None
        try:
            altitude = str(exif_tags.get("GPS GPSAltitude"))
        except IndexError:
            altitude = None
        try:
            latitude_string = str(exif_tags.get("GPS GPSLatitude"))
            clean_string = latitude_string[1:-1]
            split_list = clean_string.split(",")
            degrees = split_list[0]
            minutes = split_list[1][1:]
            seconds_fraction = split_list[2][1:]
            split_seconds = seconds_fraction.split("/")
            seconds = str(int(split_seconds[0]) / int(split_seconds[1]))
            direction = str(exif_tags.get("GPS GPSLatitudeRef"))
            latitude = gps_dms2dd(degrees, minutes, seconds, direction)
        except IndexError:
            latitude = None
        try:
            longitude_string = str(exif_tags.get("GPS GPSLongitude"))
            clean_string = longitude_string[1:-1]
            split_list = clean_string.split(",")
            degrees = split_list[0]
            minutes = split_list[1][1:]
            seconds_fraction = split_list[2][1:]
            split_seconds = seconds_fraction.split("/")
            seconds = str(int(split_seconds[0]) / int(split_seconds[1]))
            direction = str(exif_tags.get("GPS GPSLongitudeRef"))
            longitude = gps_dms2dd(degrees, minutes, seconds, direction)
        except IndexError:
            longitude = None

        db_path = os.path.join(
            abs_path, "source_data/deplatformr_open_images_v6.sqlite")
        images_db = sqlite3.connect(db_path)
        cursor = images_db.cursor()
        # Record the extracted values
        cursor.execute("UPDATE open_images SET mime_type = ?, created = ?, description = ?, width = ?, height = ?, resolution = ?, latitude = ?, longitude = ?, altitude = ? WHERE ImageID = ?",
                       (mimetype, created, description, width, height, resolution, latitude, longitude, altitude, image_id),)
        images_db.commit()
        images_db.close()
        cursor = workflow_db.cursor()
        utctime = datetime.utcnow()
        cursor.execute(
            "UPDATE images SET extract_metadata = ?, extract_metadata_timestamp = ? WHERE image_id = ?", (True, utctime, image_id,),)
        print("Extracted metadata from image " + image_id)
        workflow_db.commit()
        workflow_db.close()
        return("Success")

    except Exception as e:
        utctime = datetime.utcnow()
        cursor = workflow_db.cursor()
        cursor.execute(
            "UPDATE images SET extract_metadata = ?, extract_metadata_timestamp = ? WHERE image_id = ?", (False, utctime, image_id,),)
        workflow_db.commit()
        workflow_db.close()
        print("Failed to extract metadata for image " + image_id + ".")
        print(e)
        return("Failure")


def gps_dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return(dd)


if __name__ == "__main__":
    extract_metadata()
