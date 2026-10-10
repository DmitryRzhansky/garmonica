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
    register_context_processors(app)
    return app


def register_blueprints(app):
    from app.blueprints.main import main_bp
    from app.blueprints.services import services_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp)


def register_context_processors(app):
    @app.context_processor
    def inject_clinic_contacts():
        from app.data.clinic_contacts import get_clinic_contacts

        return {"clinic_contacts": get_clinic_contacts()}

    @app.context_processor
    def inject_structured_data():
        from flask import current_app, has_request_context, request

        if not has_request_context():
            return {"json_ld": None}
        try:
            from app.services.structured_data import build_json_ld

            return {"json_ld": build_json_ld(request)}
        except Exception:
            if current_app.config.get("TESTING"):
                raise
            current_app.logger.exception("Failed to build JSON-LD structured data")
            return {"json_ld": None}
