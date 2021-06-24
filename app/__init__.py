from flask import Flask
from redis import StrictRedis

from app.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, Config

# Initialize global database object.
redis = StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True
)


def create_app(config_class=Config):
    # Initialize application.
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enter application context.
    with app.app_context():
        # Create components with our blueprints.
        from app.links import links_blueprint

        # Register our blueprints.
        app.register_blueprint(links_blueprint, url_prefix="/api/v1/links")

    return app
