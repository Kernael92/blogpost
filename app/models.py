import datetime 

import quart.flask_patch
# The flask_patch module allows the extensions 
# to find modules and objects in the flask namespace
from quart import Quart 
import flask_admin as admin 
from flask_mongoengine import MongoEngine 
from flask_admin.form import rules 
from flask_admin.contrib.mongoengine import ModelView

# create application
app = Quart(__name__)

# Create dummy secret key so we can use sessions 
app.config['SECRET_KEY'] = 'my secret key'
app.config['MONGODB_SETTINGS'] ={'DB': 'testing'}

# create models
db = MongoEngine()
db.init_app(app)