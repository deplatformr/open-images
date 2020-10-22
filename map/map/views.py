import os
import sqlite3
from flask import Flask, render_template, redirect, flash, url_for, safe_join, send_file, jsonify
from datetime import datetime
from pygate_grpc.client import PowerGateClient
from map import app
import requests

images_db = "map/deplatformr-open-images.sqlite"

api = os.getenv('POWERGATE_API')
ffs = os.getenv('POWERGATE_FFS')
token = os.getenv('POWERGATE_TOKEN')
powergate = PowerGateClient(api, is_secure=True)


@app.route('/')
def index():

    return (redirect(url_for('image', id='14a2df364ad5f854')))


@app.route('/image/<id>')
def image(id):

    db = sqlite3.connect(images_db)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM open_images WHERE ImageID=?", (id,),)
    result = cursor.fetchone()
    photo = list(result)

    # See if city or country needs to be retrieved
    if photo[24] is None or photo[25] is None:
        map_key = os.getenv('GOOGLE_MAP_API_KEY')
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" +
                                photo[18] + "," + photo[19] + "&result_type=locality&result_type=country&key=" + map_key)
        geo_dict = dict(response.json())
        for component in geo_dict["results"][0]["address_components"]:
            if "locality" in component["types"]:
                city = component["long_name"]
            if "country" in component["types"]:
                country = component["long_name"]
        if photo[24] is None and city is not None:
            cursor.execute(
                "UPDATE open_images set city=? where ImageID=?", (city, photo[0],),)
            db.commit()
            photo[24] = city
        if photo[25] is None and country is not None:
            cursor.execute(
                "UPDATE open_images set country=? where ImageID=?", (country, photo[0],),)
            db.commit()
            photo[25] = country

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

    marker = float(photo[19]) - 50

    return render_template("index.html", photo=photo, marker=marker, created=created, jsonld=jsonld, annotations=annotations, cid=cid)


@app.route("/labels", methods=["GET"])
def labels():

    db = sqlite3.connect(images_db)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT DisplayName FROM annotations ORDER BY DisplayName")
    labels = cursor.fetchall()

    labels_list = []
    for label in labels:
        labels_list += label

    return jsonify(labels_list)


@app.route("/filecoin-download/<package>/<cid>", methods=["GET"])
def filecoin_download(package, cid):
    """
    Retrieve a file from Filecoin via IPFS using Powergate and offer the user
    the option to save it to their machine.
    """

    try:
        # Use the user data directory configured for the app
        downloads = app.config["FILECOIN_DOWNLOADS"]
        if not os.path.exists(downloads):
            os.makedirs(downloads)

        # Retrieve data from Filecoin
        # NOTE: CID config must have "hot: enabled" in Powergate for retrieval to work
        data_ = powergate.ffs.get(cid, token)

        # Save the downloaded data as a file
        with open(os.path.join(downloads, package), "wb") as out_file:
            # Iterate over the data byte chunks and save them to an output file
            for data in data_:
                out_file.write(data)

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
