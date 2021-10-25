import logging
import os

from flask import Blueprint, render_template, url_for
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

# LOGFILE = os.environ.get("LOGFILE")
# logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

@main.route('/')
def main_index():
    return render_template('index.html')
