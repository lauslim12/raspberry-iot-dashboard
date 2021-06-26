from flask import Blueprint, jsonify

utils_blueprint = Blueprint("utils_blueprint", __name__)


@utils_blueprint.route("/", methods=["GET"])
def connection_test():
    return jsonify(status="success", message="Connected successfully!"), 200


@utils_blueprint.route("/developer", methods=["GET"])
def developer_details():
    developer = {
        "name": "@lauslim12",
        "email": "nicholasdwiarto@yahoo.com",
        "github": "https://github.com/lauslim12",
        "linkedin": "https://www.linkedin.com/in/nicholasdwiarto/",
        "stackoverflow": "https://stackoverflow.com/users/13980107/nicholas-d",
        "website": "https://wwww.nicholasdw.com/",
    }

    return jsonify(status="success", data=developer), 200
