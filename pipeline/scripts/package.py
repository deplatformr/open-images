import os
import sqlite3
import tarfile
from datetime import datetime


def create_package(images, batch_dir):
    print(type(images))  # debug
    print(images)  # debug

    package_threshold = 5242880  # 5MiB
    abs_path = os.getcwd()

    try:
        package_size = 0
        for image in images:
            package_size += image[2]
        if package_size < package_threshold:
            print("Not enough images yet to make a package from this batch.")
            return()
        else:
            try:
                # create new batch directory
                split = os.path.spit(batch_dir)
                new_dir_number = int(split[1]) + 1
                new_batch_dir = os.path.join(split[0], str(new_dir_number))
                os.makedirs(new_batch_dir)
                # find all related files for the last image that's getting removed from batch to keep within threshold
                last_image = images[-1]
                path, dirs, files = next(os.walk(batch_dir))
                for file in files:
                    if file.find(last_image[0]) != -1:
                        filepath = os.path.join(path, file)
                        shutil.move(filepath, os.path.join(
                            new_batch_dir, file))
                # drop the last image from the list (convert tuple) to get the package size back under threshold
                images_list = list(images)
                images_list.pop(-1)
            except Exception as e:
                print("Unable to separate batch to make a package.")
                print(e)
                return()

            # TO DO:
            # move image batches into OCFL structure
            # generate checksums
            # generate UUID for package name
            # shorten UUID for package name
            # create tarball

            try:
                # Create the tar package
                packages_dir = os.path.join(
                    os.getcwd(), "source_data/packages/")

                tarball_name = "deplatformr-open-images-" + split[1] + ".tar"
                tarball = tarfile.open(os.path.join(
                    packages_dir, tarball_name), "w:gz")

                for file in files:
                    filepath = os.path.join(path, file)
                    tarball.add(filepath, file)
                    # delete source copy of file to save space
                    os.remove(filepath)
                tarball.close()

            except Exception as e:
                print("Unable to create a tarball package from batch.")
                print(e)
                return()

            try:
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
                db_path = os.path.join(
                    abs_path, "deplatformr_open_images_workflow.sqlite")
                workflow_db = sqlite3.connect(db_path)
                cursor = worlflow_db.cursor()
                cursor.execute(
                    "UPDATE images SET package_name = ? WHERE image_id = ?", (tarball_name, image[0],),)
                cursor.execute("INSERT INTO packages (name, size, timestamp) VALUES (?,?,?",
                               (tarball_name, tarball_size, utctime,),)
                workflow_db.commit()
                workflow_db.close()

            except Exception as e:
                print("Unable to add tarball package name to database.")
                print(e)
                return()

    except Exception as e:
        print("Unable to create a package for batch directory " + batch_dir)
        print(e)

    return()
