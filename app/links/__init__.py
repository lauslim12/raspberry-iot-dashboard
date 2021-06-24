from flask import Blueprint

links_blueprint = Blueprint("links_blueprint", __name__)


@links_blueprint.route("/", methods=["GET"])
def get_all_links():
    pass


@links_blueprint.route("/", methods=["POST"])
def create_one_link():
    pass


@links_blueprint.route("/<id>", methods=["PATCH"])
def update_one_link():
    pass


@links_blueprint.route("/<id>", methods=["DELETE"])
def delete_one_link():
    pass
