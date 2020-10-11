import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Flask settings
# TODO: change to os.getenv('FLASK-MAP-APP-SECRET-KEY')
SECRET_KEY = "22eefe0f-67fa-443c-af76-39855adb8b7d"

# Database location
OPEN_IMAGES_MAP_DB = os.path.join(BASEDIR + "map", "open-images-map.sqlite")
