from operator import itemgetter

from flask import Blueprint, jsonify, request
from regex import IGNORECASE, compile, match

from app.models import Link

links_blueprint = Blueprint("links_blueprint", __name__)


def request_valid(request_body):
    required_keys = {"name", "description", "url"}

    if all(key in request_body for key in required_keys):
        return True

    return False


def url_valid(url):
    regex = compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        IGNORECASE,
    )

    if not match(regex, url):
        return False

    return True


@links_blueprint.route("/", methods=["POST"])
def create_one_link():
    if not request_valid(request.json):
        return jsonify(message="Invalid input!"), 400

    if not url_valid(request.json.get("url")):
        return jsonify(message="Invalid URL!"), 400

    # instantly map dictionary keys to class attributes
    new_link = Link.create_link(Link(**request.json))

    return jsonify(status="success", data=vars(new_link)), 200


@links_blueprint.route("/<id>", methods=["PATCH"])
def update_one_link(id):
    previous_link = Link.get_one_link(id)

    if not request_valid(request.json):
        return jsonify(message="Invalid input!"), 400

    if not previous_link:
        return jsonify(message="No data with that ID!"), 400

    if not url_valid(request.json.get("url")):
        return jsonify(message="Invalid URL!"), 400

    # destructuring, python way
    name, description, url = itemgetter("name", "description", "url")(request.json)
    updated_link = Link.update_link(
        Link(name, description, url, previous_link.get("created_date"), id=id), id
    )

    return jsonify(status="success", data=vars(updated_link)), 200


@links_blueprint.route("/<id>", methods=["DELETE"])
def delete_one_link(id):
    if not Link.get_one_link(id):
        return jsonify(message="No data with that ID!"), 400

    Link.delete_link(id)

    return "", 204
