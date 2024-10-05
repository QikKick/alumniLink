import os

class Config:
    username = 'postgres'
    password = ''
    database = 'postgres'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://{username}:{password}@localhost:5432/{database}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask db init
    # flask db migrate -m "Initial migration."
    # flask db upgrade