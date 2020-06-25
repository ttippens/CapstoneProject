import os
from sqlalchemy import Column, String, ForeignKey, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)

    migrate = Migrate(app, db)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize and clean a database
    the database_filename variable can be changed to have multiple versions of a database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
'''

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    
    def __init__(self, title, release_date):
        self.title = title
        self.genre = genre
        
    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id 
        EXAMPLE
            movie = Movies(title=req_title, release_date=req_release_date)
            movie.insert
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movies.query.filter_by(id=req_id)
            movie.title = 'Batman Begins'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movies.query.filter_by(id=req_id)
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        representation of the Movie model
    '''

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre
        }

'''
Actors
'''

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actors(name=re_name, age=req_age, gender=req_gender)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actors.query.filter_by(id=req_id)
            actor.name = 'Christian Bale'
            actor.update()
    '''

    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter_by(id=req_id)
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        representation of the Actor model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    