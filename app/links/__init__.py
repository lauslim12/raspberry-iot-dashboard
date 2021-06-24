from operator import itemgetter

from flask import Blueprint, jsonify, request

from app.models import Link

links_blueprint = Blueprint("links_blueprint", __name__)


def request_valid(request_body):
    required_keys = {"name", "description", "url"}

    if all(key in request_body for key in required_keys):
        return True

    return False


@links_blueprint.route("/", methods=["GET"])
def get_all_links():
    pass


@links_blueprint.route("/", methods=["POST"])
def create_one_link():
    if not request_valid(request.json):
        return jsonify(message="Invalid input!"), 400

    # destructuring, python way
    name, description, url = itemgetter("name", "description", "url")(request.json)
    new_link = Link.create_link(Link(name, description, url))

    return jsonify(status="success", data=new_link), 200


@links_blueprint.route("/<id>", methods=["PATCH"])
def update_one_link():
    pass


@links_blueprint.route("/<id>", methods=["DELETE"])
def delete_one_link():
    pass
