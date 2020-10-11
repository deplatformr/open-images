import os
import sqlite3
from flask import Flask, render_template
from map import app


@app.route('/')
def index():
    return render_template("index.html")
