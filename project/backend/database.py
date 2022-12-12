from enum import unique
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/MovieFinder'



db = SQLAlchemy(app)


class movies(db.Model):
    __tablename__ = "MovieFinder"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=False)
    genre = db.Column(db.Text, unique=False)
    director = db.Column(db.Text, unique=False)
    actor = db.Column(db.Text, unique=False)
    poster = db.Column(db.Text, unique=False)
    description = db.Column(db.Text, unique=False)
    rating = db.Column(db.REAL, unique=False)
    year = db.Column(db.Integer, unique=False)

    def __init__(self, id, name, genre, director, actor, poster, description, rating, year):
        self.id = id
        self.name = name
        self.genre = genre
        self.director = director
        self.actor = actor
        self.poster = poster
        self.description = description
        self.rating = rating
        self.year = year

    def __repr__(self):
        return '<Movie %r>' % self.name


class users(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    pass_hash = db.Column(db.String(64), unique=False)
    otc = db.Column(db.String(6), unique=False)
    tmp = db.Column(db.Integer, unique=False)
    username = db.Column(db.String(), unique=False)
    token = db.Column(db.String(), unique=False)
    review = db.Column(db.JSON, unique=False)
    wishlist = db.Column(db.Text, unique=False)
    banlist = db.Column(db.Text, unique=False)

    def __init__(self, uid, email, pass_hash, otc, tmp, username, token, wishlist, banlist):
        self.uid = uid
        self.email = email
        self.pass_hash = pass_hash
        self.otc = otc
        self.tmp = tmp
        self.username = username
        self.token = token
        self.wishlist = wishlist
        self.banlist = banlist
        self.review = {}

    def getEmail(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % self.username
