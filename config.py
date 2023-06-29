import os
from dotenv import load_dotenv    

basedir = os.path.abspath(os.path.dirname(__file__))

# give access to the project in ANY os we find ourselves in
# allow outside files/folders to be added to the project from the base directory

load_dotenv(os.path.join(basedir, '.env'))    # telling it to load our variables from the env file

class Config():
    """
        Set Config variables for the flask app
        Using Environment variables where available otherwise
        create the config variables if not already done.
    """

    FLASK_APP = os.environ.get('FLASK_APP')      # refers to variables created in .env... adding the env to a separate file makes it more secure since we will put .env into gitignore
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess this, haha'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Turn off database updates from sqlalchemy

    # URI = Uniform resource indentifier