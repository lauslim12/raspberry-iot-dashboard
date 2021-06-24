from flask import Blueprint, render_template

from app.models import Link

views_blueprint = Blueprint("views_blueprint", __name__)


@views_blueprint.route("/", methods=["GET"])
def home():
    links = Link.get_links()
    return render_template("home.html", title="Homepage", links=links), 200


@views_blueprint.route("/new", methods=["GET"])
def new():
    return render_template("new.html", title="New"), 200


@views_blueprint.route("/edit/<id>", methods=["GET"])
def edit(id):
    link_to_edit = Link.get_one_link(id)
    return render_template("edit.html", title="Edit", link=link_to_edit), 200
