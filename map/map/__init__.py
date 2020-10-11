from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static")
app.config.from_object("config")

# These imports need to come after the app is instantiated
from map import views
