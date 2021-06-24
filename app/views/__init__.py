from flask import Blueprint, render_template

views_blueprint = Blueprint("views_blueprint", __name__)


@views_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html", title="Homepage"), 200


@views_blueprint.route("/new", methods=["GET"])
def new():
    return render_template("new.html", title="New"), 200
