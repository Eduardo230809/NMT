from flask import Flask

from src.routes import AuthRoutes, IndexRoutes, LanguageRoutes

app = Flask(__name__)

def init_app(config):
    app.config.from_object(config)

    app.register_blueprint(IndexRoutes.main, url_prefix = '/')

    return app