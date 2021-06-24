from flask import Flask


def create_app():
    # Initialize application
    app = Flask(__name__)

    # Enter application context.
    with app.app_context():

        @app.route("/", methods=["GET"])
        def hello():
            return "Hello World!", 200

    return app
