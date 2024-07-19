from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, Float
from sqlalchemy.orm import relationship
from flask import Flask
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
os.environ.get('FLASK_KEY')


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)

# CONFIGURE TABLES






class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    coordinate1 = db.Column(Float, nullable=False)
    coordinate2 = db.Column(Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    distance = db.Column(db.Enum('close', 'so so', 'far', name='distance_enum'), nullable=False)
    type = db.Column(db.Enum('indoor', 'outdoor', name='type_enum'), nullable=False)
    photo_address = db.Column(db.String(100), nullable=True)




    #attributes
    att_food = db.Column(db.Boolean, default=False, nullable=False)
    att_my_food = db.Column(db.Boolean, default=False, nullable=False)
    att_table = db.Column(db.Boolean, default=False, nullable=False)
    att_socket = db.Column(db.Boolean, default=False, nullable=False)
    att_cultural = db.Column(db.Boolean, default=False, nullable=False)
    att_outdoor_activity = db.Column(db.Boolean, default=False, nullable=False)
    att_work_study = db.Column(db.Boolean, default=False, nullable=False)

    # Foreign key to the User table
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates='places')




class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    places = relationship('Place', back_populates='author')











