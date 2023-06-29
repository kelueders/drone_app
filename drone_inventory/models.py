from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid                                 # using this to create unique primary key numbers
from datetime import datetime

# Adding Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets     # using this to generate a user token

# Import for LoginManager & UserMixin
# help us login our users and store their credentials
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

# help us log in a user
@login_manager.user_loader      # object login_manager has access to the attribute user_loader
def load_user(user_id):
    return User.query.get(user_id)     # quering the database for the user and then returning the dictionary for that user


# helps us find the user
class User(db.Model, UserMixin):
    # creating our table and all the columns and setting them to their particular types
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True)    # you can create a user without needing to have this relationship

    # need to still create relationship between User table and Drone table

    def __init__(self, email, username, password, first_name = '', last_name = ''):     # defaults always go last
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self):       # everything has to be returned if it is set in the init
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database! Wahoo!"
    

class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    camera_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_production = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(150))
    random_joke = db.Column(db.String, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)     # using this as the foreign key
    # relationship is: One User to Many Drones, which is why the foreign key is on the Drone Class

    def __init__(self, name, description, price, camera_quality, flight_time, max_speed, dimensions, weight,
                 cost_of_production, series, random_joke, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.series = series
        self.random_joke = random_joke
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Drone {self.name} has been added to the database! Woohoo!"
    
class DroneSchema(ma.Schema):
    class Meta:
        # these fields will come back from the API call
        fields = ['id', 'name', 'description', 'price', 'camera_quality', 'flight_time', 'max_speed',
                  'dimensions', 'weight', 'cost_of_production', 'series', 'random_joke']
        
drone_schema = DroneSchema()
drones_schema = DroneSchema(many = True)   # will bring back a list of objects


