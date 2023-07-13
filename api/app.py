from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)

from DB.models import Groups

with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!"
