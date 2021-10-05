from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return render_template('index.html')
