import os
import sqlite3
from flask import Flask, render_template, redirect, flash, url_for, safe_join, send_file, jsonify, request
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

    return (redirect(url_for('label', name='Swimming')))


@app.route('/about')
def about():

    return (render_template("about.html"))


@app.route('/image/<id>')
def image(id):

    db = sqlite3.connect(images_db)
    cursor = db.cursor()

    cursor.execute("SELECT * FROM open_images WHERE ImageID=?", (id,),)
    result = cursor.fetchone()
    photo = list(result)

    # See if city or country needs to be retrieved
    if photo[24] is None or photo[25] is None:
        city = None
        country = None
        map_key = os.getenv('GOOGLE_MAP_API_KEY')
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" +
                                photo[18] + "," + photo[19] + "&result_type=street_address&key=" + map_key)
        geo_dict = dict(response.json())
        try:
            for component in geo_dict["results"][0]["address_components"]:
                if "postal_town" in component["types"]:
                    city = component["long_name"]
                if "country" in component["types"]:
                    country = component["long_name"]
                if "locality" in component["types"]:
                    city = component["long_name"]
                if "country" in component["types"]:
                    country = component["long_name"]
        except:
            pass
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

    # Gather and sort annotations related to this image
    cursor.execute("SELECT * FROM annotations WHERE ImageID=?", (id,),)
    annotations = cursor.fetchall()
    tags = []
    boxes = []
    relationships = []
    segmentations = []
    for annotation in annotations:
        if annotation[3] == "tag":
            tags += [[annotation[4], annotation[5], annotation[2]]]
        if annotation[3] == "relationship":
            relationships += [[annotation[4], annotation[2], annotation[10], annotation[11], annotation[6], annotation[7],
                               annotation[8], annotation[9], annotation[12], annotation[13], annotation[14], annotation[15]]]
        if annotation[3] == "box":
            boxes += [[annotation[4], annotation[2], annotation[6], annotation[7],
                       annotation[8], annotation[9], annotation[16], annotation[17], annotation[18], annotation[19], annotation[20]]]
        if annotation[3] == "segmentation":
            segmentations += [[annotation[4], annotation[2], annotation[6], annotation[7],
                               annotation[8], annotation[9], annotation[21], annotation[23]]]

    training_relationships = [
        relationship for relationship in relationships if relationship[0] == "training"]
    validation_relationships = [
        relationship for relationship in relationships if relationship[0] == "validation"]
    testing_relationships = [
        relationship for relationship in relationships if relationship[0] == "testing"]

    training_boxes = [
        box for box in boxes if box[0] == "training"]
    validation_boxes = [
        box for box in boxes if box[0] == "validation"]
    testing_boxes = [
        box for box in boxes if box[0] == "testing"]

    training_tags = [tag for tag in tags if tag[0] == "training"]
    confident_training_tags = [tag for tag in training_tags if tag[1] == 1]
    not_confident_training_tags = [tag for tag in training_tags if tag[1] == 0]

    validation_tags = [tag for tag in tags if tag[0] == "validation"]
    confident_validation_tags = [tag for tag in validation_tags if tag[1] == 1]
    not_confident_validation_tags = [
        tag for tag in validation_tags if tag[1] == 0]

    testing_tags = [tag for tag in tags if tag[0] == "testing"]
    confident_testing_tags = [tag for tag in testing_tags if tag[1] == 1]
    not_confident_testing_tags = [tag for tag in testing_tags if tag[1] == 0]

    training_segmentations = [
        segmentation for segmentation in segmentations if segmentation[0] == "training"]
    validation_segmentations = [
        segmentation for segmentation in segmentations if segmentation[0] == "validation"]
    testing_segmentations = [
        segmentation for segmentation in segmentations if segmentation[0] == "confident_testing_tags"]

    cursor.execute(
        "SELECT cid, size FROM packages WHERE name=?", (photo[22],),)
    cid = cursor.fetchone()

    marker = float(photo[19]) - 50

    return render_template("image.html", photo=photo, marker=marker, created=created, jsonld=jsonld, cid=cid, training_boxes=training_boxes, validation_boxes=validation_boxes, testing_boxes=testing_boxes, confident_training_tags=confident_training_tags, not_confident_training_tags=not_confident_training_tags, confident_validation_tags=confident_validation_tags, not_confident_validation_tags=not_confident_validation_tags, confident_testing_tags=confident_testing_tags, not_confident_testing_tags=not_confident_testing_tags, training_segmentations=training_segmentations, validation_segmentations=validation_segmentations, testing_segmentations=testing_segmentations, training_relationships=training_relationships, validation_relationships=validation_relationships, testing_relationships=testing_relationships)


@app.route("/label/<name>", methods=["GET"])
def label(name):

    db = sqlite3.connect(images_db)
    cursor = db.cursor()
    cursor.execute(
        "SELECT ImageID FROM annotations WHERE DisplayName = ?", (name,),)
    labels = cursor.fetchall()

    images_list = []
    for label in labels:
        cursor.execute(
            "SELECT latitude, longitude FROM open_images WHERE ImageID=?", (label[0],),)
        image = cursor.fetchone()
        if image is not None:
            images_list += [(label[0], image[0], image[1])]

    count = len(images_list)

    return render_template("label.html", images=images_list, label=name, count=count)


@app.route('/image-info')
def image_info():
    id = request.args.get("id")
    db = sqlite3.connect(images_db)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM open_images WHERE ImageID=?", (id,),)
    result = cursor.fetchone()
    photo = list(result)

    # See if city or country needs to be retrieved
    if photo[24] is None or photo[25] is None:
        city = None
        country = None
        map_key = os.getenv('GOOGLE_MAP_API_KEY')
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" +
                                photo[18] + "," + photo[19] + "&result_type=street_address&key=" + map_key)
        geo_dict = dict(response.json())
        try:
            for component in geo_dict["results"][0]["address_components"]:
                if "postal_town" in component["types"]:
                    city = component["long_name"]
                if "country" in component["types"]:
                    country = component["long_name"]
                if "locality" in component["types"]:
                    city = component["long_name"]
                if "country" in component["types"]:
                    country = component["long_name"]
        except:
            pass
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

    return jsonify({"filename": photo[21], "city": photo[24], "country": photo[25]})


@app.route("/labels", methods=["GET"])
def labels():

    db = sqlite3.connect(images_db)
    cursor = db.cursor()
    cursor.execute(
        "SELECT DISTINCT DisplayName FROM annotations ORDER BY DisplayName")
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

        """
        # Retrieve data from Filecoin
        # NOTE: CID config must have "hot: enabled" in Powergate for retrieval to work
        data_ = powergate.ffs.get(cid, token)

        # Save the downloaded data as a file
        with open(os.path.join(downloads, package), "wb") as out_file:
            # Iterate over the data byte chunks and save them to an output file
            for data in data_:
                out_file.write(data)
        """

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
