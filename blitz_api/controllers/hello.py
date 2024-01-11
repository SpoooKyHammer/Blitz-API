from flask import Blueprint

hi = Blueprint("hi", __name__)

@hi.route("/hello")
def hello():
    return { "text": "hello world" }

