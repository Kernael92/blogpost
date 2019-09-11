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

# Define mongoengine documents
class User(db.Document):
    name = db.StringField(max_length=40)
    tags = db.ListField(db.ReferenceField('Tag'))
    password = db.StringField(max_length=40)

    def __unicode__(self):
        return self.name


class Tag(db.Document):
    name = db.StringField(max_length=10)

    def __unicode__(self):
        return self.name 


class comment(db.EmbeddeDocument):
    name = db.StringField(max_length=20, required=True)
    value = db.StringField(max_length=20)
    tag = db.ReferenceField(Tag)

class Post(db.Document):
    name = db.StringField(max_length=20, required=True)
    body = db.TextAreaField()
    pub_date = db.DateTime(default=datetime.datetime.now)
    inner = db.ListField(db.EmbeddedDocumentField(Comment))
    lols = db.ListField(db.StringField(max_length=20))
    user = db.ReferenceField(User, required=True)

    # Required for administrative interface
    def __unicode__(self):
        return self.name


class File(db.Document):
    name = db.StringField(max_length=20)
    data = db.FileField()


class Image(db.Document):
    name = db.StringField(max_length=20)
    image = db.ImageField(thumbnail_size=(100, 100, True))


# Customize admin views
class UserView(ModelView):
    column_filters = ['name']

    column_searchable_list = ('name', 'password')

    form_ajax_refs = {
        'tags': {
            'fields': ('name')
        }
    }


class PostView(ModelView):
    column_filters = ['name']

    form_ajax_refs =  {
        'user': {
            'fields': ['name']
        }
    }

    form_subdocuments = {
        'inner': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the of the form 
                    'form_rules': ('name', 'tag', 'value', rules.HTML('<hr>')),
                    'form_widget_args': {
                        'name': {
                            'style': 'color: red'
                        }
                    }
                }
            }
        }
    }