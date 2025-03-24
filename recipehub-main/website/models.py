import datetime
from .database import db
from flask_login import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import TSVECTOR

favorites = db.Table('favorites',
    db.Column('user_id', db.String(36), db.ForeignKey('users.id')),
    db.Column('recipe_id', db.String(36), db.ForeignKey('recipes.id'))
)
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.String(36), db.ForeignKey('recipes.id')),
    db.Column('tag_id', db.String(36), db.ForeignKey('tags.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    recipes = db.relationship('Recipe', back_populates='user') 
    favorites = db.relationship('Recipe', secondary=favorites, backref=db.backref('favorited_by', lazy='dynamic'), lazy='dynamic')

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    title = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(250))
    cooking_time = db.Column(db.String(150))
    difficulty = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #search_vector = db.Column(TSVECTOR)

    user = db.relationship('User', back_populates='recipes')
    tags = db.relationship('Tag', secondary=recipe_tags, back_populates='recipes')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    recipes = db.relationship('Recipe', secondary=recipe_tags, back_populates='tags')