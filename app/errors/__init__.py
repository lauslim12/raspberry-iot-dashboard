from flask import Blueprint, jsonify, render_template
from redis import RedisError
from werkzeug.exceptions import HTTPException

errors_blueprint = Blueprint("errors_blueprint", __name__)


@errors_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Not Found"), 404


@errors_blueprint.app_errorhandler(500)
def internal_server_error(error):
    pass


@errors_blueprint.app_errorhandler(HTTPException)
def handle_custom_http_error(error):
    return (
        jsonify(status="fail", name=error.name, message=error.description),
        error.code,
    )


@errors_blueprint.app_errorhandler(RedisError)
def handle_redis_exception(error):
    return (
        jsonify(
            status="fail",
            message="Our database has an internal error. Please try again later!",
        ),
        500,
    )
