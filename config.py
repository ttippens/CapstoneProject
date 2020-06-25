import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Database connection string
DATABASE_URL = "postgres://rgtkgtbnphmdae:9e38766e18b328da6d4be1ad4d2eb155dcff236e7d46aad6b148fef38498692d@ec2-34-232-147-86.compute-1.amazonaws.com:5432/d5o0brthggfn9i"
#Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False