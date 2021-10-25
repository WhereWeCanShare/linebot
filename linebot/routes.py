import logging
import os

from flask import Blueprint, render_template, url_for
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)


@main.route('/')
def main_index():
    return render_template('index.html')
