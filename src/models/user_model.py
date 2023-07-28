
from src import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    firstname = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))
