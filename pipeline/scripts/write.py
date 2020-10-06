import os
import sqlite3
import json


def write_metadata(image_id="cdc83f5d4569422d", image_directory="source_data/images/1"):
    abs_path = os.getcwd()
    filepath = (os.path.join(
        abs_path, image_directory + "/" + image_id + ".jsonld"))
    db_path = os.path.join(
        abs_path, "source_data/deplatformr_open_images_v6.sqlite")
    images_db = sqlite3.connect(db_path)
    cursor = images_db.cursor()
    cursor.execute("SELECT * from open_images WHERE ImageID = ?", (image_id,),)
    image = cursor.fetchone()

    imageid = "openimages:" + image[0]

    if image[6] is None or image[6] == "None":
        if image[5] is not None or image[5] != "None":
            creator = image[5]
        else:
            creator = None
    else:
        if image[5] is not None and image[5] != "None":
            creator = image[6] + " (" + image[5] + ")"
        else:
            creator = image[6]

    if image[8] is not None and image[8] != "None":
        size = GetHumanReadableFilesize(image[8])
    else:
        size = None

    img_dict = {"@context": "https://schema.org/",
                "@type": "ImageObject", "@id": imageid, "contentUrl": image[2]}

    if image[10] is not None and image[10] != "None":
        img_dict["thumbnailUrl"] = image[10]
    if image[7] is not None and image[7] != "None":
        img_dict["name"] = image[7]
    if image[21] is not None and image[21] != "None":
        img_dict["image"] = image[21]
    if creator is not None:
        img_dict["creator"] = creator
    if image[12] is not None and image[12] != "None":
        img_dict["dateCreated"] = image[12]
    if image[13] is not None and image[13] != "None":
        img_dict["description"] = image[13]
    if image[4] is not None and image[4] != "None":
        img_dict["license"] = image[4]
    if size is not None:
        img_dict["contentSize"] = size
    if image[14] is not None and image[14] != "None":
        img_dict["encodingFormat"] = image[14]
    if image[15] is not None and image[15] != "None":
        img_dict["width"] = image[15]
    if image[16] is not None and image[16] != "None":
        img_dict["height"] = image[16]
    if image[17] is not None and image[17] != "None":
        img_dict["resolution"] = image[17]
    if image[9] is not None and image[9] != "None":
        img_dict["disambiguatingDescription"] = image[9]

    exif_dict = []
    if image[11] is not None and image[11] != "None":
        exif_dict.append({"@type": "PropertyValue",
                          "name": "Orientation", "value": image[11]})
    if image[18] is not None and image[18] != "None":
        exif_dict.append({"@type": "PropertyValue",
                          "name": "GPSLatitude", "value": image[18]})
    if image[19] is not None and image[19] != "None":
        exif_dict.append({"@type": "PropertyValue",
                          "name": "GPSLongitude", "value": image[19]})
    if image[20] is not None and image[20] != "None":
        exif_dict.append({"@type": "PropertyValue",
                          "name": "GPSAltitude", "value": image[20]})
    if exif_dict is not None:
        img_dict["exifData"] = exif_dict

    with open(filepath, "w", encoding="utf-8") as outfile:
        json.dump(img_dict, outfile, indent=4, ensure_ascii=False)

    return()


def GetHumanReadableFilesize(size, precision=2):
    suffixes = ["B", "KiB", "MiB", "GiB", "TiB"]
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])


if __name__ == "__main__":
    write_metadata()
