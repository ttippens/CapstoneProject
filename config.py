import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Database connection string
DATABASE_URL = "postgres://postgres:Tr@v1st1p@localhost:5432/casting_agency"
#Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
