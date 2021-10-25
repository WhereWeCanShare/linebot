import logging
import os

from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__)

LOGFILE = os.getenv('LOGFILE') or "../logs/bot.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

@main.route('/')
def main_index():
    return render_template('index.html')
