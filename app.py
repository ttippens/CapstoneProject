import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json


from models import setup_db, db_drop_and_create_all, Movies, Actors
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #db_drop_and_create_all()

    return app

App = create_app()

'''
POST /actors
    endpoint accesible by casting director and executive producer
    return status code 200 and json {'success' True, 'actor': actor}
    where actor is the actor that has been added to the db
    or appropriate status code indicating the reason for failure
'''
@App.route('/')
def index():
    return jsonify({'message': 'Casting Agent API'})


@App.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def post_actor(payload):

    form = request.get_json()

    name = form.get('name')
    age = form.get('age')
    gender = form.get('gender')

    if name is None or age is None or gender is None:
        abort(422)
    
    try:
        actor = Actors(
            name=name,
            age=age,
            gender=gender
        ).insert()
        
        all_actors = Actors.query.all()
        actors = [actor.format() for actor in all_actors]

        return jsonify({
            'success': True,
            'actors': actors
        })
    except Exception:
        abort(422)

'''
POST /movies
    endpoint accesible by the casting director and executive producer
    return status code 200 and the json {'success': True, 'movie': movie}
    where movie is the movie that has been added to the db
    or appropriate status code indicating the reason for failure
'''

@App.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def post_movie(payload):

    form = request.get_json()

    title = form.get('title')
    genre = form.get('genre')

    if title is None or genre is None:
        abort(422)

    try:
        movie = Movies(
            title=title,
            genre=genre
        ).insert()

        all_movies = Movies.query.all()
        movies = [movie.format() for movie in all_movies]

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception:
        abort(422)

'''
PATCH /actors
    endpoint is accesible by casting director and executive producer
    return status code 200 and json {'success': True, 'actor': actor}
    where actor is the actor who's details have been edited
    or appropriate status code indicating the reason for failure
'''

@App.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def patch_actor(payload, actor_id):

    form = request.get_json()

    name=form.get('name')
    age=form.get('age')
    gender=form.get('gender')

    if name is None or age is None or gender is None:
        abort(422)

    actor = Actors.query.filter_by(id=actor_id).one_or_none()

    if actor is None:
        abort(404)
    
    try:
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.update()

        all_actors = Actors.query.all()
        actors = [actor.format() for actor in all_actors]

        return jsonify({
            'success': True,
            'actors': actors
        })
    except Exception:
        abort(422)

'''
PATCH /movies
    endpoint is accesible by the casting director and executive producer
    return status code 200 and json {'success': True, 'movie': movie}
    where movie the movie who's details have been edited
    or appropriate status code indicatinf reason for failure
'''

@App.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def patch_movie(payload, movie_id):

    form = request.get_json()

    title=form.get('title')
    genre=form.get('genre')

    if title is None or genre is None:
        abort(422)

    movie = Movies.query.filter_by(id=movie_id).one_or_none()

    if movie is None:
        abort(404)

    try:
        movie.title = title
        movie.genre = genre
        movie.update()
        
        all_movies = Movies.query.all()
        movies = [movie.format() for movie in all_movies]

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception:
        abort(422)

'''
GET /actors
    endpoint accesible by casting assistant, casting director and executive producer
    return status code 200 and json {'success': True, 'actors': actors}
    where actors is the list of actors
    or appropriate status code indicating reason for failure
'''

@App.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):

    all_actors = Actors.query.all()

    try:
        actors = [actor.format() for actor in all_actors]
        return jsonify({
            'success': True,
            'actors': actors
        })
    except Exception:
        abort(404)

'''
GET /movies
    endpoint accesible by casting assistant, casting director and exectuive producer
    return status code 200 and json {'success': True, 'movies': movies}
    where movies is the list of movies
    or appropriate status code indicating reason for failure
'''

@App.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):

    all_movies = Movies.query.all()
    try:
        movies = [movie.format() for movie in all_movies]
        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception:
        abort(404)


'''
DELETE /actors
    endpoint accesible by casting director and executive producer
    return status code 200 and json {'succes': True, 'deleted_actor': actor_id}
    where actor_id is the id of the actor deleted
    or appropriate status code indicating the reason for failure
'''

@App.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload, actor_id):

    actor = Actors.query.filter_by(id=actor_id).one_or_none()

    if actor is None:
        abort(404)

    try:
        actor.delete()

        return jsonify({
            'success': True,
            'deleted_actor': actor_id
        })
    except Exception:
        abort(422)

'''
DELETE /movies
    endpoint accesible by executive producer
    return status code 200 and json {'success': True, 'deleted_movie': movie_id}
    where movie_id is the id of the movie deleted
    or appropriate status code indicating the reason for failure
'''

@App.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):

    movie = Movies.query.filter_by(id=movie_id).one_or_none()

    if movie is None:
        abort(404)

    try:
        movie.delete()

        return jsonify({
            'success': True,
            'deleted_movie': movie_id
        })
    except Exception:
        abort(422)

'''
Error 422
'''

@App.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    'success': False,
                    'error': 422,
                    'message': 'unprocessable entity'
                    }), 422

'''
Error 404
'''

@App.errorhandler(404)
def resouce_not_found(error):
    return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'resource not found'                
                    }), 404

'''
Error AuthError
'''

@App.errorhandler(AuthError)
def authorization_error(error):
    return jsonify({
                    'success': False,
                    'error': AuthError,
                    'message': 'Error with authorization.'
                    }), AuthError

'''
Error 401
'''

@App.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    'success': False,
                    'error': 401,
                    'message': 'Unauthorized.'
                    }), 401

'''
Error 400
'''


@App.errorhandler(400)
def bad_request(error):
    return jsonify({
                    'success': False,
                    'error': 400,
                    'message': 'Bad request.'
                    }), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    App.run(host='0.0.0.0', port=port, debug=True)
