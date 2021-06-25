from flask import Flask
from redis import StrictRedis

from app.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, Config
from app.extensions import compress, cors, limiter, talisman

# Initialize global database object.
redis = StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True
)


def create_app(config_class=Config):
    # Initialize application.
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup Content Security Policy.
    csp = {
        "default-src": "'self'",
        "font-src": ["'self'", "fonts.googleapis.com", "fonts.gstatic.com"],
        "style-src-elem": ["'self'", "fonts.googleapis.com"],
    }

    # Setup global third-party middlewares with application factories.
    compress.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    with app.app_context():
        # Create components with our blueprints.
        from app.errors import errors_blueprint
        from app.links import links_blueprint
        from app.views import views_blueprint

        # Register our blueprints.
        app.register_blueprint(links_blueprint, url_prefix="/api/v1/links")
        app.register_blueprint(views_blueprint)

        # Register our global error handling blueprint.
        app.register_blueprint(errors_blueprint)

    return app
