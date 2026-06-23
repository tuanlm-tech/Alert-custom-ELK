from flask import Blueprint, Flask, jsonify, render_template


from services.elastic_service import (
    get_users,
    get_roles,
    get_current_user
)
app = Flask(
    __name__,
    template_folder="views"
)

api = Blueprint("api", __name__)

@api.route("/")
def home():

    return render_template(
        "index.html",
        current_user=get_current_user()
    )


@api.route("/users")
def users():

    return render_template(
        "users.html",
        users=get_users()
    )


@api.route("/roles")
def roles():

    return render_template(
        "roles.html",
        roles=get_roles()
    )