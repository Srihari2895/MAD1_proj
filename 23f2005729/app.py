from flask import Flask
from backend.models import *
from backend.api_controller import api
app = None

def init_app():
    myapp = Flask(__name__)
    myapp.debug = False
    myapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.sqlite3"
    db.init_app(myapp)
    api.init_app(myapp)
    myapp.app_context().push()
    db.create_all()
    return myapp

app = init_app()

from backend.login import *
from backend.influencer import *
from backend.sponsor import *

if __name__ == "__main__":
    app.run()
    