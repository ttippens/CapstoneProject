import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 

from app import App
from models import setup_db, Actors, Movies



class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = App
        self.client = self.app.test_client
        self.database_name = 'casting_agency'
        self.username = 'postgres'
        self.password = 'Tr@v1st1p'
        self.url = 'localhost:5432'
        self.database_path = 'postgres://{}:{}@{}/{}'.format(self.username, self.password, self.url, self.database_name)
        setup_db(self.app, self.database_path)

        self.PRODUCER_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1UbXpWUldPMVVrSENIWVFMbEo3RCJ9.eyJpc3MiOiJodHRwczovL2Rldi1sM2staHVyeS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNTQwY2YxY2MxYWMwYzE0OTM1ZWI1IiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTA3NjM1MzAsImV4cCI6MTU5MDg0OTkzMCwiYXpwIjoiWjdkeU1ZTTg0YmZCMmNwNUNNN1Fyd2hTN1dBbTJibUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.jAmv5yYu3YcXW4Y38-MK7WRyLkraxDoW0P6K3W6Xqwf3u_nVZKotkvme1jh6lPMAkvHUSwdSX-aYh1qqLrv6R0CpnJSIfUMP3kCYjIN4XAnJTex3IbacP_82LuBQhVCQp7hEk7qnPOuIcV-fxhFsl_ds85rGZpFTvuOTQurwqADg7YNKEAUWVPisQBnyHyIxMq854hpxwbXjHiqO42Gt-yNIu0wsQpo96vyTY06MwtgmYxdd1A23KcMxIVEIT0rFoTU_TO-jUtPFU3FB9NkZB-wyje619rOzPdHSm2tFEPeN5WvO_rRYrPKqpSG3HUSSHpazU06EVmYRwJ90oSs8Jw'
        self.DIRECTOR_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1UbXpWUldPMVVrSENIWVFMbEo3RCJ9.eyJpc3MiOiJodHRwczovL2Rldi1sM2staHVyeS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNTQyOGQxY2MxYWMwYzE0OTM2MzllIiwiYXVkIjoiQ2FzdGluZyBBZ2VuY3kiLCJpYXQiOjE1OTA3NjM4MzAsImV4cCI6MTU5MDg1MDIzMCwiYXpwIjoiWjdkeU1ZTTg0YmZCMmNwNUNNN1Fyd2hTN1dBbTJibUsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.mRu9jNL_2hUBFwbZfLkuvvuBH13I6TabTRxYUCA7HTrJiTfeh6lRXMkVMxATF3xa3D3sYrz0mA4SsAPgm3cytq17_1lrkIXQjWgM5UfiQt3jHZxBj58Xv21Xjoy9HOCYZVsUW-SpF7cH1Ox48zSJW5kVAF53LSkhxW2YIu39MFMBmNTdTzBO5ZvmumjdJ_uymaXe3lOBlZjsaOKbCqzK2Qqib5wN0UQqdPKLV6ctWPIgjdAX_Z2oBTaH_AxiKonAkjGEiZdl3Z0iZHmd0Ok8qDN0zy6Jzm3ahk27sFf-wal6hdqB82c_tkk6SgfPH6QRl9MrG95OTYNrTiVVFgsF2g'

        self.post_movie={
            'title': 'The Dark Knight',
            'genre': 'Comedy'
        }

        self.post_movie_error={
            'title': 'The Dark Knight Rises'
        }

        self.post_actor={
            'name': 'Tom Hardy',
            'age': 42,
            'gender': 'female'
        }

        self.post_actor_error={
            'name': 'Cillian Murphy',
            'gender': 'male'
        }

        self.patch_movie={
            'title': 'The Dark Knight',
            'genre': 'Action'
        }

        self.patch_actor={
            'name': 'Tom Hardy',
            'age': 42,
            'gender': 'male'
        }

        self.executive_producer_header={
            'Content-Type': 'application/json',
            'Authorization': self.PRODUCER_TOKEN
        }

        self.casting_director_header={
            'Content-Type': 'application/json',
            'Authorization': self.DIRECTOR_TOKEN
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
        

    def tearDown(self):  
        pass
        

    '''
    Test
    This endpoint should post a new post
    '''

    def test_post_actor(self):
        res=self.client().post('/actors', json=self.post_actor, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_actor_error(self):
        res = self.client().post('/actors', json=self.post_actor_error, headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    '''
    Test
    This endpoint should post a new post
    '''

    def test_post_movie(self):
        res=self.client().post('/movies', json=self.post_movie, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_movie_error(self):
        res=self.client().post('/movies', json=self.post_movie_error, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')
   

    '''
    Test
    This endpoint should patch a post
    '''

    def test_patch_actor(self):
        res = self.client().patch('/actors/1', json=self.patch_actor, headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_patch_actor_error(self):
        res = self.client().patch('/actors/100', json=self.patch_actor, headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    '''
    Test
    This endpoint should patch a post
    '''

    def test_patch_movie(self):
        res = self.client().patch('/movies/1', json=self.patch_movie, headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_patch_movie_error(self):
        res = self.client().patch('/movies/100', json=self.patch_movie, headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    '''
    Test
    This endpoint should return a list of actors.
    '''

    def test_get_actors(self):
        res=self.client().get('/actors', headers=self.casting_director_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    '''
    Test
    This endpoint should return a list of actors.
    '''

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_director_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    '''
    Test 
    This endpoint should delete a actor using a actor id.
    '''

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'], 1)

    def test_delete_actor_error(self):
        res = self.client().delete('/actors/100', headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    '''
    Test 
    This endpoint should delete a movie using a movie id.
    '''

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie'], 1)

    def test_delete_movie_error(self):
        res = self.client().delete('/movies/100', headers=self.executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()