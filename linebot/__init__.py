from flask import Flask, Blueprint

from .settings import Setting
from .routes import main
from .line2telegram.routes import l2tg


def create_app():
    app = Flask(__name__)
    app.config.from_object(Setting)

    app.register_blueprint(main)
    app.register_blueprint(l2tg, url_prefix='/l2tg')

    return app
