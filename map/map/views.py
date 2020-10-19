import os
import sqlite3
from flask import Flask, render_template, redirect, flash, url_for, safe_join, send_file
from datetime import datetime
from pygate_grpc.client import PowerGateClient
from map import app

images_db = "map/deplatformr-open-images.sqlite"

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')
powergate = PowerGateClient(api, is_secure=True)

@app.route('/')
@app.route('/<id>')
def index(id):

    db = sqlite3.connect(images_db)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT DisplayName FROM annotations")
    tags = cursor.fetchall()

    cursor.execute("SELECT * FROM open_images WHERE ImageID=?", (id,),)
    photo = cursor.fetchone()

    if photo[12] is not None:
        # TODO convert to more readable format
        created = photo[12]
    else:
        created = "None"

    split = os.path.splitext(photo[21])
    jsonld = split[0] + ".jsonld"

    cursor.execute("SELECT * FROM annotations WHERE ImageID=?", (id,),)
    annotations = cursor.fetchall()

    cursor.execute(
        "SELECT cid, size FROM packages WHERE name=?", (photo[22],),)
    cid = cursor.fetchone()

    return render_template("index.html", tags=tags, photo=photo, created=created, jsonld=jsonld, annotations=annotations, cid=cid)


@app.route("/filecoin-download/<id>/<package>/<cid>", methods=["GET"])
def filecoin_download(id, cid, package):
    """
    Retrieve a file from Filecoin via IPFS using Powergate and offer the user
    the option to save it to their machine.
    """

    try:
        # Use the user data directory configured for the app
        downloads = app.config["FILECOIN_DOWNLOADS"]
        if not os.path.exists(downloads):
            os.makedirs(downloads)

        """
        # Retrieve data from Filecoin
        data_ = powergate.ffs.get(cid, token)

        # Save the downloaded data as a file
        with open(os.path.join(downloads, package), "wb") as out_file:
            # Iterate over the data byte chunks and save them to an output file
            for data in data_:
                out_file.write(data)
        """

        # FOR TESTING
        package = "deplatformr-open-images-71.tar"

        # Create path to download file
        safe_path = safe_join("../" + downloads, package)

        # Offer the file for download to local machine
        return send_file(safe_path, as_attachment=True)

        # TODO: CLEAR CACHED FILES IN DOWNLOAD DIRECTORY

    except Exception as e:
        # Output error message if download from Filecoin fails
        flash("failed to download '{}' from Filecoin. {}".format(
            package, e), "alert-danger")
        return (redirect(url_for('index', id=id)))
