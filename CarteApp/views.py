from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_mail import Mail
import datetime

app = Flask(__name__)
mail = Mail(app)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

class Users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False)
    UserEmail = db.Column(db.String(200), nullable=False, unique=True)
    UserPassword = db.Column(db.String(200), nullable=False)
    UserDateAdd = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, UserName:str, UserEmail:str, UserPassword:str):
        self.UserName = UserName
        self.UserEmail = UserEmail
        self.UserPassword = UserPassword

class Votes(db.Model):
    UserID = db.Column(db.Integer, nullable=False)
    CSVFileVote = db.Column(db.String(200), nullable=False, unique=True)
    VoteDateAdd = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, UserID:int, CSVfileVote:str):
        self.UserID = UserID
        self.CSVFileVote = CSVfileVote

def init_db():
    db.drop_all()
    db.create_all()
    #db.session.add(Users("UserName:str", "UserEmail:str", "UserPassword:str"))
    db.session.commit()

@app.route('/')
def acceuil():
    pass