import os
import shutil
import sqlite3
import tarfile
from datetime import datetime
import bagit


def create_package(images, batch_dir):

    abs_path = os.getcwd()
    package_threshold = 10485760  # 10MiB
    print("Package threshold: " + get_human_readable_file_size(package_threshold))

    try:
        package_size = 0
        for image in images:
            print("image " + image[0])  # debug
            print("image batch size " +
                  get_human_readable_file_size(image[1]))  # debug
            package_size += image[1]
        print("Total batch size: " + get_human_readable_file_size(package_size))
        if package_size < package_threshold:
            print("Not enough images yet to make a package from this batch.")
            return()
        else:
            try:
                # create new batch directory
                split = os.path.split(batch_dir)
                new_dir_number = int(split[1]) + 1
                new_batch_dir = os.path.join(split[0], str(new_dir_number))
                os.makedirs(new_batch_dir)
                # move all related files for the last image that's getting removed from batch to keep within threshold
                last_image = images[-1]
                path, dirs, files = next(os.walk(batch_dir))
                for file in files:
                    if file.find(last_image[0]) != -1:
                        filepath = os.path.join(path, file)
                        shutil.move(filepath, os.path.join(
                            new_batch_dir, file))
                # drop the last image from the list (convert tuple) to get the package size back under threshold
                images.pop(-1)
            except Exception as e:
                print("Unable to separate batch to make a package.")
                print(e)
                return()

            # Convert batch directory into a Bagit directory
            external_identifier = "deplatformr-open-images-" + split[1]
            bagit.make_bag(batch_dir,
                           {'Source-Organization': 'Deplatformr Project', 'Organization-Address': 'https://open-images.deplatformr.com', 'External-Description': 'This package contains a subset of the Google Open Images dataset used for machine learning training. The image files have been downloaded from their Flickr server source, verified for fixity, had EXIF metadata extracted, and are now bundled here with their annotation data, segmentation files and newly generated sha512 checksums. This content and context is described in a sidecar metadata files using schema.org/ImageObject and JSON-LD format.', 'External-Identifier': external_identifier, 'License': 'https://creativecommons.org/licenses/by/2.0/'}, checksums=["sha512"])
            print("Created a Bagit directory.")

            try:
                # Create the tar package
                packages_dir = os.path.join(
                    os.getcwd(), "source_data/packages/")
                tarball_name = external_identifier + ".tar"
                tarball = tarfile.open(os.path.join(
                    packages_dir, tarball_name), "w")
                tarball.add(batch_dir, arcname=external_identifier)
                tarball.close()
                print("Created tarball " + tarball_name + ".")
            except Exception as e:
                print("Unable to create a tarball package from batch.")
                print(e)
                return()

            try:
                shutil.rmtree(batch_dir)
                print("Deleted the batch source directory.")
            except OSError as e:
                print("Unable to delete the source directory.")
                print(e)

            # record the tarball package name for each image
            db_path = os.path.join(
                abs_path, "source_data/deplatformr_open_images_v6.sqlite")
            images_db = sqlite3.connect(db_path)
            cursor = images_db.cursor()

            for image in images:
                cursor.execute("UPDATE open_images SET package_name = ? WHERE ImageID = ?",
                               (tarball_name, image[0],),)
            images_db.commit()
            images_db.close()
            # add tarball name, size, and timestamp to the workflow dbase
            utctime = datetime.utcnow()
            tarball_size = os.path.getsize(
                os.path.join(packages_dir, tarball_name))
            print("Tarball size is: " + get_human_readable_file_size(tarball_size))
            db_path = os.path.join(
                abs_path, "deplatformr_open_images_workflow.sqlite")
            workflow_db = sqlite3.connect(db_path)
            cursor = workflow_db.cursor()
            for image in images:
                cursor.execute(
                    "UPDATE images SET package_name = ? WHERE image_id = ?", (tarball_name, image[0],),)
            cursor.execute("INSERT INTO packages (name, size, timestamp) VALUES (?,?,?)",
                           (tarball_name, tarball_size, utctime,),)
            workflow_db.commit()
            workflow_db.close()

    except Exception as e:
        print("Unable to create a package for batch directory " + batch_dir)
        print(e)


def get_human_readable_file_size(size, precision=2):
    suffixes = ["B", "KiB", "MiB", "GiB", "TiB"]
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division
    return "%.*f %s" % (precision, size, suffixes[suffixIndex])

    return()
