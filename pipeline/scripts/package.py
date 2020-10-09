import os
import sqlite3
import tarfile

def create_package(images)

    abs_path = os.getcwd()
    db_path = os.path.join(abs_path, "deplatformr_open_images_workflow.sqlite")
    workflow_db = sqlite3.connect(db_path)

    try:
        package_threshhold = 5242880  # 5MiB
        package_size = 0
        for image in images:
            package_size += result[1]
        if package_size > package_threshold:
            # create new batch directory
            # find all related files for image getting moved from batch
            # move them into the new batch directory
            split = os.split(batch_dir)
            new_dir = int(split[1]) + 1
            os.makedirs(os.path.join(split[0], str(new_dir)))
            # drop the last image from the list (convert tuple) to get the package size back under threshold
            results_list = list(results)
            results_list.pop(-1)

            # move image batches into OCFL structure
            # generate checksums
            # generate UUID for package name
            # shorten UUID for package name
            # create tarball

            # Create the tar package
            if not os.path.exists(os.path.join(os.getcwd(), "source_data/packages/")):
                os.makedirs(os.path.join(os.getcwd(), "source_data/packages/"))
            packages_dir = os.path.join(os.getcwd(), "source_data/packages/")

            tarball_name = "deplatformr-open-images-" + first_dir + ".tar"
            tarball = tarfile.open(os.path.join(
                packages_dir, tarball_name), "w:gz")

            filepath = os.path.join(path, file)
            tarball.add(filepath, file)
            tarball.close()

            # add tarball_size to dbase
            tarball_size = os.path.getsize(
                os.path.join(packages_dir, tarball_name))
            # add tarball name to dbase
            cursor = workflow_db.cursor()
            cursor.execute("UPDATE ___ SET  WHERE ___ = ?",
                           (__, ___,),)

        else:
            print("Not enough images yet to make a package from this batch.")
            return()

    except Exception as e:
        print("Unable to create a package for batch directory " + batch_dir)
        print(e)
        cursor.execute(
            "UPDATE ___ SET ___  WHERE __ = ?", (__, __,),)

    workflow_db.commit()
    workflow_db.close()

    return()
