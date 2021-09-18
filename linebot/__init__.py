from flask import Flask, Blueprint

from .routes import main
from .line2telegram.routes import l2tg

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    # db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(l2tg, url_prefix='/l2tg')

    return app
