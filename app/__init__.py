from flask import Flask

from app.config import Config
from app.errors import register_error_handlers


def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/assets",
    )
    app.config.from_object(config_class)

    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_blueprints(app):
    from app.blueprints.main import main_bp
    from app.blueprints.services import services_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp)
