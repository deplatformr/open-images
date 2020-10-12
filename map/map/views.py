import os
import sqlite3
from flask import Flask, render_template
from datetime import datetime
from map import app

images_db = "map/deplatformr-open-images.sqlite"


@app.route('/')
@app.route('/<id>')
def index(id="14a2df364ad5f854"):

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

    return render_template("index.html", tags=tags, photo=photo, created=created, jsonld=jsonld, annotations=annotations)
