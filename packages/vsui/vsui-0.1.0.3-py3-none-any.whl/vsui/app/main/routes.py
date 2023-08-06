from flask import render_template, send_file
from pathlib import Path
from . import main
from .. import definitions

@main.route('/')
def index():
    return render_template('index.html')
