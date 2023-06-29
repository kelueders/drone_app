from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .models import db as root_db, login_manager, ma
from .helpers import JSONEncoder

from flask_migrate import Migrate

# Flask CORS import - Cross Origin Resource Sharing 
# future proofing for our react app to be able to access our flask api
from flask_cors import CORS

app = Flask(__name__)

# temporary route to show how this works
# @app.route("/") # simple route on the homepage
# def hello_world():
#     return "<p>Hello, World!</p>"

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app)
migrate = Migrate(app, root_db)

ma.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'    # if user is not logged in and they try to go to a certain page, they will get redirected to auth.signin

app.json_encoder = JSONEncoder           # we aren't instantiated an object with specific attributes, we're just pointing one encoder to another

CORS(app)