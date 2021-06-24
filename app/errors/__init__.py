from flask import Blueprint, jsonify, render_template
from redis import RedisError
from werkzeug.exceptions import HTTPException

errors_blueprint = Blueprint("errors_blueprint", __name__)


@errors_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Not Found"), 404


@errors_blueprint.app_errorhandler(500)
@errors_blueprint.app_errorhandler(RedisError)
def internal_server_error(error):
    return (
        render_template("500.html", title="Internal Error", error_description=error),
        500,
    )


@errors_blueprint.app_errorhandler(HTTPException)
def handle_custom_http_error(error):
    return (
        jsonify(status="fail", name=error.name, message=error.description),
        error.code,
    )
