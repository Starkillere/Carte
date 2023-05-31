from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from flask_mail import Mail
from . import MyStat
import secrets
import hashlib
import enum
import csv
import os

app = Flask(__name__, static_url_path='/static')
mail = Mail(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

class Activate(enum.Enum):
    off = 0
    on = 1

class Users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False, unique=True)
    UserEmail = db.Column(db.String(200), nullable=False, unique=True)
    UserPassword = db.Column(db.String(200), nullable=False)
    UserDateAdd = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, UserName:str, UserEmail:str, UserPassword:str):
        self.UserName = UserName
        self.UserEmail = UserEmail
        self.UserPassword = UserPassword

class Votes(db.Model):
    VotesID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    VoteTitle = db.Column(db.String(200), nullable=False)
    VoteCastique = db.Column(db.String(3000), nullable=False)
    MultipleChoice = db.Column(db.String(3000), nullable=False)
    VoteStatue = db.Column(db.Enum(Activate), nullable=False)
    CSVFileVote = db.Column(db.String(200), nullable=False, unique=True)
    Access = db.Column(db.String(200), nullable=False, unique=True)
    VoteDateAdd = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, UserID:int, VoteTitle:str, CSVfileVote:str, VoteCastique:str, MultipleChoice:str, VoteStatue:str, Access:str):
        self.UserID = UserID
        self.VoteTitle = VoteTitle
        self.VoteCastique = VoteCastique
        self.MultipleChoice = MultipleChoice
        self.VoteStatue = VoteStatue
        self.CSVFileVote = CSVfileVote
        self.Access =  Access

def t_init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Users(app.config["ADMINISTRATEUR_USERNAME"], app.config["MAIL_USERNAME"], hashlib.sha384( app.config["ADMINISTRATEUR_PASSWORD"].encode()).hexdigest()))
    db.session.commit()

@app.route('/', methods=['GET'])
def acceuil():
    if "CONNECT" in session:
        return render_template('acceuil.html', connect=session['CONNECT'])
    else:
        return render_template('acceuil.html', connect=False)
    
@app.route('/login',  methods=['POST'])
def login():
    if not "CONNECT" in session:
        if request.method == 'POST':
            username = request.form['username']
            useremail = request.form['useremail']
            userpassword = hashlib.sha384(request.form['userpassword'].encode()).hexdigest()

            ok_user = Users.query.filter_by(UserName=username, UserEmail=useremail, UserPassword=userpassword).first()

            if ok_user != None:
                session["CONNECT"] = True
                session["UserID"] = ok_user.UserID
                session["UserName"] = username
                session["UserEmail"] = useremail

                flash("Bisou Bisou <5", "message")
            else:
                flash("Y'a un problème avec toi mon pote", "error")
        
    return redirect(url_for('acceuil'))

@app.route('/sigin', methods=['POST'])
def sigin():
    if not "CONNECT" in session:
        if request.method == 'POST':
            username = request.form['username']
            useremail = request.form['useremail']
            userpassword = hashlib.sha384(request.form['userpassword'].encode()).hexdigest()

            ok_username = Users.query.filter_by(UserName=username).first()
            ok_useremail = Users.query.filter_by(UserEmail=useremail).first()

            if ok_username != None and ok_useremail != None:
                user = Users(username, useremail, userpassword)
                db.session.add(user)
                db.session.commit()

                ok_user = Users.query.filter_by(UserName=username, UserEmail=useremail, UserPassword=userpassword).first()
                session["CONNECT"] = True
                session["UserID"] = ok_user.UserID
                session["UserName"] = username
                session["UserEmail"] = useremail

                flash("Bienvenue bienvenue. Tu as amené de la pizza, j'espère !", "message")
            flash("Vous ne pouvait pas être deux trouve toit ton identité", "message")
    return redirect(url_for('acceuil'))

@app.route('/mot-de-passe-oublie', methods=['GET', 'POST'])
def mot_de_passe_oublie():
    pass

@app.route('/creat-new-vote', methods=['GET', 'POST'])
def creat_new_vote():
    if "CONNECT" in session:
        if request.method == 'POST':
            form_content = dict(request.form)
            if 'option0' in form_content:

                vote_title = form_content['title']

                if 'multiple-choice' in form_content:
                    type_of_choice = form_content['multiple-choice']
                else:
                    type_of_choice = "off"
                
                
                options = ''.join([value+',' for key,value in form_content.items() if key.startswith('option')])[:-1]

                access = secrets.token_urlsafe(35)+''.join(chr(ord(let)) for let in session['UserName'])+''.join(chr(ord(let)) for let in str(datetime.now()).replace(" ", "-").replace(".", "-").replace(":", "-"))

                urlforcsvfile = os.path.join((f"CarteApp/static/{app.config['CSVFOLDER']}"), access+'.csv') #url_for('static', filename=app.config['CSVFOLDER']+access+'.csv')
                urlforvote = url_for('print_vote', access=access)

                vote = Votes(session["UserID"], vote_title, urlforcsvfile, options, type_of_choice, Activate.on, access)
                db.session.add(vote)
                db.session.commit()

                with open(urlforcsvfile, 'w', newline='') as file:
                    dw = csv.DictWriter(file, delimiter=',', fieldnames=options.split(","))
                    dw.writeheader()
                
                flash(f'Votre a été initialiser ! Et est disponible ici : {urlforvote}', 'message')
                return redirect(request.url)

            else:
                flash('Vous avez oubliè de renseigner les options de réponse !', 'error')
                return redirect(request.url)
        else:
            return render_template('creat.html', connect=session['CONNECT'])
    return redirect(url_for('acceuil'))

@app.route('/vote/<access>', methods=['GET', "POST"])
def print_vote(access):
    if request.method == "POST":
        form_content = list(dict(request.form).values())
        keys = Votes.query.filter_by(Access=access).first().VoteCastique.split(',')
        values = [0 for i in range(len(keys))]
        content = { k:v for (k,v) in zip(keys, values)}

        for option in form_content:
            content[option] = 1
        
        with open(Votes.query.filter_by(Access=access).first().CSVFileVote, 'a', newline='') as file:
            dw = csv.DictWriter(file, fieldnames=keys)
            dw.writerow(content)
        
        flash('Votre vote à bien était pris en compte', 'warning')
        return redirect(url_for('acceuil'))

    else:
        voteselect = Votes.query.filter_by(Access=access).first()
        if voteselect != None:
            if voteselect.VoteStatue == Activate.on:
                return render_template('vote.html', Access=access, options=voteselect.VoteCastique.split(','), type_of_choice=voteselect.MultipleChoice, titre=voteselect.VoteTitle)
            else:
                flash('Ce vote est out', 'message')
                return redirect(url_for('acceuil'))
        else:
            flash('Vote inexistant', 'message')
            return redirect(url_for('acceuil'))
        
@app.route("/tableau-de-bord", methods=['GET', 'POST'])
def tableau_de_bord():
    if "CONNECT" in session:
        voteselect = Votes.query.filter_by(UserID=session["UserID"]).all()
        return render_template("tableau_de_bord.html", votes=voteselect, connect=session['CONNECT'], session=session)
    return redirect(request.url)

@app.route('/my-statistique-for/<UserName>/<Access>', methods=['GET', 'POST'])
def my_statistique(UserName, Access):
    if "CONNECT" in session:
        if session["UserName"] == UserName:
            if request.method == 'POST':
               return send_file(os.path.join((f"CarteApp/static/{app.config['CSVFOLDER']}"), Access+'.csv'))
            mystat = MyStat.MyStat(os.path.join((f"CarteApp/static/{app.config['CSVFOLDER']}"), Access+'.csv'))
            return render_template('my-statistique.html', stat=mystat.dict_smoll_stat(), head=mystat.head, connect=session['CONNECT'], session=session, access=Access)
    return redirect(request.url)