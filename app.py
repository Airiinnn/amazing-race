# Python standard libraries
import json
import os
import sqlite3
import csv
import random
import subprocess
import datetime

# Third-party libraries
from flask import Flask, render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from user import User
from config import Config

# Configuration
GOOGLE_CLIENT_ID = "685992959593-701prlcssas6vu8h87srulmbr6t40hg2.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "zKHCQ2IYsBdn50r7Umyy2ZUM"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    player = Player.query.filter_by(id=user_id).first()
    return User(player.id, player.name, player.email)

# Redirect unauthorized users to login
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')

# Models
class Bonusstage(db.Model):
    stageid = db.Column(db.Integer, index=True, primary_key=True)
    stagename = db.Column(db.Text, index=True)
    requirement = db.Column(db.Text, index=True)

class Mainstage(db.Model):
    stageid = db.Column(db.Integer, index=True, primary_key=True)
    stagename = db.Column(db.Text, index=True)
    psw = db.Column(db.Text, index=True)

class Player(db.Model):
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, index=True, unique=True)
    email = db.Column(db.Text, index=True, unique=True)

class Progress(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    mainstage = db.Column(db.Integer, index=True, default=0)
    bonus0 = db.Column(db.Text, index=True)
    bonus1 = db.Column(db.Text, index=True)
    bonus2 = db.Column(db.Text, index=True)
    bonus3 = db.Column(db.Text, index=True)
    main0 = db.Column(db.Text, index=True)
    main1 = db.Column(db.Text, index=True)
    main2 = db.Column(db.Text, index=True)
    main3 = db.Column(db.Text, index=True)
    main4 = db.Column(db.Text, index=True)
    main5 = db.Column(db.Text, index=True)
    main6 = db.Column(db.Text, index=True)
    main7 = db.Column(db.Text, index=True)
    end = db.Column(db.Text, index=True)
    psw = db.Column(db.Text, index=True, default="goodmorning")
    group = db.Column(db.Integer, index=True, default=0)

class Stage0(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    q1 = db.Column(db.Integer, index=True, default=0)
    q2 = db.Column(db.Integer, index=True, default=0)
    q3 = db.Column(db.Integer, index=True, default=0)
    q4 = db.Column(db.Integer, index=True, default=0)
    q5 = db.Column(db.Integer, index=True, default=0)
    q6 = db.Column(db.Integer, index=True, default=0)
    q7 = db.Column(db.Integer, index=True, default=0)
    q8 = db.Column(db.Integer, index=True, default=0)
    q9 = db.Column(db.Integer, index=True, default=0)
    q10 = db.Column(db.Integer, index=True, default=0)

class Stage1(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    q1 = db.Column(db.Integer, index=True, default=0)
    q2 = db.Column(db.Integer, index=True, default=0)
    q3 = db.Column(db.Integer, index=True, default=0)
    q4 = db.Column(db.Integer, index=True, default=0)

class Stage2(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    q1 = db.Column(db.Integer, index=True, default=0)
    q2 = db.Column(db.Integer, index=True, default=0)
    q3 = db.Column(db.Integer, index=True, default=0)
    q4 = db.Column(db.Integer, index=True, default=0)
    q5 = db.Column(db.Integer, index=True, default=0)
    q6 = db.Column(db.Integer, index=True, default=0)
    q7 = db.Column(db.Integer, index=True, default=0)
    q8 = db.Column(db.Integer, index=True, default=0)

class Stage3(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    q1 = db.Column(db.Integer, index=True, default=0)
    q2 = db.Column(db.Integer, index=True, default=0)
    q3 = db.Column(db.Integer, index=True, default=0)

class Stage7(db.Model):
    email = db.Column(db.Text, index=True, primary_key=True)
    q1 = db.Column(db.Integer, index=True, default=0)
    q2 = db.Column(db.Integer, index=True, default=0)
    q3 = db.Column(db.Integer, index=True, default=0)
    q4 = db.Column(db.Integer, index=True, default=0)
    q5 = db.Column(db.Integer, index=True, default=0)
    q6 = db.Column(db.Integer, index=True, default=0)




with app.app_context():
    db.create_all()

bonus0 = Bonusstage(stageid=0, stagename="Bonus 0: Computational Thinking", requirement=2)
bonus1 = Bonusstage(stageid=1, stagename="Bonus 1: SQL", requirement=3)
bonus2 = Bonusstage(stageid=2, stagename="Bonus 2: Competitive Programming", requirement=5)
bonus3 = Bonusstage(stageid=3, stagename="Bonus 3: HTML & CSS", requirement=7)
main0 = Mainstage(stageid=0, stagename="Stage 0: Cyber Security, Ethics & Practices", psw="protecc")
main1 = Mainstage(stageid=1, stagename="Stage 1: Python Basics", psw="nextdoor")
main2 = Mainstage(stageid=2, stagename="Stage 2: Computational Thinking", psw="bigbraintime")
main3 = Mainstage(stageid=3, stagename="Stage 3: SQL", psw="bbcsland")
main4 = Mainstage(stageid=4, stagename="Stage 4: NoSQL", psw="3213b5")
main5 = Mainstage(stageid=5, stagename="Stage 5: Competitive Programming", psw="fastgame")
main6 = Mainstage(stageid=6, stagename="Stage 6: Socket Programming", psw="z cfmv jftbvkzf")
main7 = Mainstage(stageid=7, stagename="Stage 7: HTML & CSS", psw="-")
main8 = Mainstage(stageid=8, stagename="Portal", psw="goodmorning")
db.session.add_all([bonus0, bonus1, bonus2, bonus3, main0, main1, main2, main3, main4, main5, main6, main7, main8])
db.session.commit()

players = []

with open("group_psw.csv", 'r') as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)
    for line in reader:
        players.append(line)

for player in player:
    p = Progress(email=player[2], psw=player[3], group=int(player[0]))
    db.session.add(p)
    db.session.commit()




@app.route("/")
def index():
    if current_user.is_authenticated:
        main_stages = Mainstage.query.all()
        bonus_stages = Bonusstage.query.all()

        q = Progress.query.filter_by(email=current_user.email).first()
        progress = [q.mainstage, q.bonus0, q.bonus1, q.bonus2, q.bonus3]

        finished = Stage7.query.filter_by(email=current_user.email).first().q6

        return render_template("index.html", name=current_user.name, progress=progress, main_stages=main_stages, bonus_stages=bonus_stages, finished=finished)
    else:
        return render_template("login.html")



#Stage -1: Demostration, KEY: testrun
@app.route("/stage-1", methods=["GET", "POST"])
@login_required
def stage_demo():
    if request.method == "GET":
        return render_template("stage-1.html")
    else:
        ans = request.form.get("ans")
        if ans == "healthy python":
            return render_template("stage-1_success.html")
        else:
            correct = False
            return render_template("stage-1.html", correct=correct)



#STAGE 0: Cyber Security, KEY: protecc
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage0questions")
STAGE0_QUESTIONS = cursor.fetchall()
connection.close()
    
@app.route('/stage0', methods=["GET", "POST"])
@login_required
def stage0_main():
    if request.method == "GET":
        q = Stage0.query.filter_by(email=current_user.email).first()
        stage0_progress = [q.q1, q.q2, q.q3, q.q4, q.q5, q.q6, q.q7, q.q8, q.q9, q.q10]

        stage0_incomplete = [i for i in range(10) if stage0_progress[i] == 0]

        if len(stage0_incomplete) == 0:
            return render_template("stage0_success.html")

        else:
            return render_template("stage0.html", question=STAGE0_QUESTIONS[random.choice(stage0_incomplete)], progress=10-len(stage0_incomplete))
    
    else:
        qn = request.form.get("qn")
        ans = request.form.get("ans")
        progress = request.form.get("progress")

        for question in STAGE0_QUESTIONS:
            if question[0] == qn:
                if ans == question[6]: # correct          
                    stage0 = Stage0.query.filter_by(email=current_user.email).first()
                    setattr(stage0, qn, 1)
                    db.session.commit()

                    return redirect("/stage0")

                else: # incorrect
                    return render_template("stage0.html", question=question, correct=False, progress=progress)



#STAGE 1: PYTHON BASICS, KEY: nextdoor
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage1questions")
STAGE1_QUESTIONS = cursor.fetchall()
connection.close()

@app.route("/stage1", methods=["GET", "POST"])
@login_required
def stage1():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage
    
    if maxstage < 1:
        return redirect("/submit")
    
    else:
        if request.method == "GET":
            q = Stage1.query.filter_by(email=current_user.email).first()
            stage1_progress = [q.q1, q.q2, q.q3]
            
            stage1_incomplete = [i for i in range(3) if stage1_progress[i] == 0]
            if len(stage1_incomplete) == 0:
                return redirect("/stage1/q4")

            else:
                question = STAGE1_QUESTIONS[random.choice(stage1_incomplete)]
                return render_template("stage1.html", question=question, progress=4-len(stage1_incomplete))
        
        else:
            qn = request.form.get("qn")
            ans = request.form.get("ans")
            progress = request.form.get("progress")

            for question in STAGE1_QUESTIONS:
                if question[0] == qn:
                    if ans == question[2]: # correct
                        stage1 = Stage1.query.filter_by(email=current_user.email).first()
                        setattr(stage1, qn, 1)
                        db.session.commit()

                        return redirect("/stage1")

                    else: # incorrect
                        return render_template("stage1.html", question=question, correct=False, progress=progress)

@app.route("/stage1/q4", methods=["GET", "POST"])
@login_required
def stage1_q4():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 1:
        return redirect("/submit")
    
    else:
        if request.method == "GET":
            q = Stage1.query.filter_by(email=current_user.email).first()
            stage1_progress = [q.q1, q.q2, q.q3, q.q4]

            for i in range(3):
                if stage1_progress[i] == 0:
                    return redirect("/stage1")

            if stage1_progress[3] == 1:
                return render_template("stage1_success.html")

            else:
                question = STAGE1_QUESTIONS[3]
                return render_template("stage1_q4.html", question=question, progress=3)

        else:
            qn = request.form.get("qn")
            code = request.form.get("code")
            progress = request.form.get("progress")
            
            if code:
                # prevent user for accessing files
                if "open" in code or "file" in code:
                    output = "No trying to open files!"
                    return render_template("stage1_q4.html", code=code, error=output, question=STAGE1_QUESTIONS[3], progress=progress)
                
                else:
                    with open("toiletpaper/toiletpaper.py", 'w') as file:
                        file.write("import sys\nsys.modules['os']=None\nsys.modules['sqlite3']=None\nsys.modules['flask']=None\nsys.modules['subprocess']=None\nsys.modules['sys']=None\ndel sys\n") # prevent importing os and sqlite3
                        file.write(code)

                    
                    toiletinput = open("toiletpaper/toiletpaper.in")
                    try:
                        output = subprocess.check_output(["python", "toiletpaper/toiletpaper.py"], timeout=1,stdin=toiletinput).decode("utf-8")
                    except subprocess.TimeoutExpired:
                        output = "Time Limit Exceed. Is your code stuck in an infinite loop? Or is it inefficient?"
                        return render_template("stage1_q4.html", code=code, error=output, question=STAGE1_QUESTIONS[3], progress=progress)
                    except subprocess.CalledProcessError:
                        output = "There's an error in your code."
                        return render_template("stage1_q4.html", code=code, error=output, question=STAGE1_QUESTIONS[3], progress=progress)
                    
                    output = output.split("\n")
                    output = output[0].replace("\r", "")

                    # check answers
                    for question in STAGE1_QUESTIONS:
                        if question[0] == qn:
                            if output == question[2]: # correct
                                stage1 = Stage1.query.filter_by(email=current_user.email).first()
                                setattr(stage1, qn, 1)
                                db.session.commit()
                                
                                return render_template("stage1_success.html")

                            else:
                                output = "Wrong Answer! Ps: How many days are there?"
                                return render_template("stage1_q4.html", code=code, error=output, question=question, progress=progress)



#STAGE 2: COMPUTATIONAL THINKING, KEY: bigbraintime
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage2questions")
STAGE2_QUESTIONS = cursor.fetchall()
connection.close()

@app.route("/stage2", methods=["GET", "POST"])
@login_required
def stage2():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage
    
    if maxstage < 2:
        return redirect("/submit")

    else:
        if request.method == "GET":
            q = Stage2.query.filter_by(email=current_user.email).first()
            stage2_progress = [q.q1, q.q2, q.q3, q.q4, q.q5, q.q6, q.q7, q.q8]


            for i in range(8):
                if stage2_progress[i] == 0:
                    return render_template("stage2.html", question=STAGE2_QUESTIONS[i], progress=i)

            return render_template("stage2_success.html")
        
        else:
            qn = request.form.get("qn")
            ans = request.form.get("ans")
            progress = request.form.get("progress")

            for question in STAGE2_QUESTIONS:
                if question[0] == qn:
                    if ans == question[2]: # correct
                        stage2 = Stage2.query.filter_by(email=current_user.email).first()
                        setattr(stage2, qn, 1)
                        db.session.commit()

                        return redirect("/stage2")

                    else: # incorrect
                        return render_template("stage2.html", question=question, correct=False, progress=progress)



#STAGE 3: SQL, KEY: hi3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage3questions")
STAGE3_QUESTIONS = cursor.fetchall()
connection.close()

@app.route("/stage3", methods=["GET", "POST"])
@login_required
def stage3():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage
    
    if maxstage < 3:
        return redirect("/submit")

    else:
        if request.method == "GET":
            q = Stage3.query.filter_by(email=current_user.email).first()
            stage3_progress = [q.q1, q.q2, q.q3]
            
            stage3_incomplete = [i for i in range(3) if stage3_progress[i] == 0]
            if len(stage3_incomplete) == 0:
                return render_template("stage3_success.html")

            else:
                return render_template("stage3.html", question=STAGE3_QUESTIONS[random.choice(stage3_incomplete)], progress=3-len(stage3_incomplete))
        
        else:
            qn = request.form.get("qn")
            ans = request.form.get("ans")
            progress = request.form.get("progress")

            for question in STAGE3_QUESTIONS:
                if question[0] == qn:
                    if ans == question[3]: # correct
                        stage3 = Stage3.query.filter_by(email=current_user.email).first()
                        setattr(stage3, qn, 1)
                        db.session.commit()

                        return redirect("/stage3")

                    else: # incorrect
                        return render_template("stage3.html", question=question, correct=False, progress=progress)



#STAGE 4: NOSQL, KEY: 3213b5
@app.route("/stage4")
@login_required
def stage4():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 4:
        return redirect("/submit")
    return render_template("stage4.html")



#STAGE 5: COMPETITIVE PROGRAMMING, KEY: hi5
@app.route("/stage5", methods=["GET", "POST"])
@login_required
def stage5():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 5:
        return redirect("/submit")
    
    else:
        if request.method == "GET":
            return render_template("stage5.html")
        
        else:
            code = request.form.get("code")
            if code:
                # prevent user for accessing files
                if "open" in code or "file" in code:
                    output = "No trying to open files!"
                    return render_template("stage5.html", code=code, error=output)
                
                else:
                    subtasks = []

                    with open("castle/castle.py", 'w') as file:
                        file.write("import sys\nsys.modules['os']=None\nsys.modules['sqlite3']=None\nsys.modules['flask']=None\nsys.modules['subprocess']=None\nsys.modules['sys']=None\ndel sys\n") # prevent importing os and sqlite3
                        file.write(code)

                    for i in range(3):
                        castleInput = open("castle/castle-{}.in".format(i))
                        try:
                            output = subprocess.check_output(["python", "castle/castle.py"], timeout=1, stdin=castleInput).decode("utf-8")
                        except subprocess.TimeoutExpired:
                            output = "Time Limit Exceed. Is your code stuck in an infinite loop? Or is it inefficient?"
                            return render_template("stage5.html", code=code, error=output)
                        except subprocess.CalledProcessError:
                            output = "There's an error in your code."
                            return render_template("stage5.html", code=code, error=output)
                        
                        # check answers
                        with open("castle/castle-ans-{}.txt".format(i), 'r') as file:
                            ans = list(file)
                        
                        output = output.split("\n")
                        n = len(output) - 1
                        if n != len(ans):
                            subtasks.append(False)
                        
                        else:
                            correct = True
                            for i in range(n):
                                output[i].strip()
                                output[i] = output[i].replace("\r", "")

                                if output[i] != ans[i].strip():
                                    correct = False

                            subtasks.append(correct)

                    return render_template("stage5.html", code=code, userans=output, subtasks=subtasks)
            
            else: # empty input
                return render_template("stage5.html")



#STAGE 6: SOCKET PROGRAMMING, KEY: hi6
@app.route("/stage6")
@login_required
def stage6():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 6:
        return redirect("/submit")
    return render_template("stage6.html")



#STAGE 7: HTML / CSS, KEY: hi7
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage7questions")
STAGE7_QUESTIONS = cursor.fetchall()
connection.close()

@app.route("/stage7", methods=["GET", "POST"])
@login_required
def stage7():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 7:
        return redirect("/submit")

    else:
        if request.method == "GET":
            q = Stage7.query.filter_by(email=current_user.email).first()
            stage7_progress = [q.q1, q.q2, q.q3, q.q4, q.q5, q.q6]

            for i in range(6):
                if stage7_progress[i] == 0:
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[i], code=STAGE7_QUESTIONS[i][2], progress=i)

            # if finished all 6 questions
            psw = Progress.query.filter_by(email=current_user.email).first().psw
            return render_template("stage7_success.html", psw=psw)
        
        else:
            qn = request.form.get("qn")
            code = request.form.get("code")

            userans = "".join(code.split())
            userans = userans.lower()

            if qn == "q1": # question 1
                pos = []
                tags = ["<!doctypehtml>", "<html>", "<head>", "<title>", "</title>", "</head>", "<body>", "<h1>", "</h1>", "<h2>", "</h2>", "<p>", "</p>", "</body>", "</html>"]

                for tag in tags:
                    temp = userans.find(tag)
                    if temp == -1: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[0], code=code, progress=0, correct=False)

                    pos.append(temp)

                if pos == sorted(pos): # correct
                    stage7 = Stage7.query.filter_by(email=current_user.email).first()
                    setattr(stage7, qn, 1)
                    db.session.commit()

                    return redirect("/stage7")

                else: # incorrect
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[0], code=code, progress=0, correct=False)

            elif qn == "q2": # question 2:
                if userans.find("body{font-family:'inconsolata',monospace;}") == -1 and userans.find("body{font-family:\"inconsolata\",monospace;}") == -1: # incorrect
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[1], code=code, progress=1, correct=False)

                else:
                    if userans.find("body{font-family:'inconsolata',monospace;}") != -1:
                        body = userans.find("body{font-family:'inconsolata',monospace;}")
                    else:
                        body = userans.find("body{font-family:\"inconsolata\",monospace;}")
                    
                    h1 = userans.find("h1{font-size:24px;}")
                    p = userans.find("p{color:red;}")
                    
                    pos = []
                    tags = ["<!doctypehtml>", "<html>", "<head>", "<style>", "</style>" "</head>", "<body>", "</body>", "</html>"]

                    for tag in tags:
                        temp = userans.find(tag)
                        if temp == -1: # incorrect
                            return render_template("stage7.html", question=STAGE7_QUESTIONS[1], code=code, progress=1, correct=False)
                        
                        pos.append(temp)

                    if pos == sorted(pos) and body > pos[3] and h1 > pos[3] and p > pos[3] and body < pos[4] and h1 < pos[4] and p < pos[4]: # correct
                        stage7 = Stage7.query.filter_by(email=current_user.email).first()
                        setattr(stage7, qn, 1)
                        db.session.commit()

                        return redirect("/stage7")

                    else: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[1], code=code, progress=1, correct=False)
            
            elif qn == "q3": # question 3
                pos = []
                tags = ["<!doctypehtml>", "<html>", "<head>", "<style>", "blockquote{background-color:#f7f1e3;}", "</style>" "</head>", "<body>", "<blockquote>", "<pre>", "</pre>", "</blockquote>", "</body>", "</html>"]
                
                for tag in tags:
                    temp = userans.find(tag)

                    if temp == -1: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[2], code=code, progress=2, correct=False)

                    pos.append(temp)

                if pos == sorted(pos): # correct
                    stage7 = Stage7.query.filter_by(email=current_user.email).first()
                    setattr(stage7, qn, 1)
                    db.session.commit()

                    return redirect("/stage7")

                else: # incorrect
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[2], code=code, progress=2, correct=False)

            elif qn == "q4": # question 4
                closingbracket = False
                    
                padding = userans.find("padding:0;")
                if padding != -1:
                    if userans.find("padding:0;}") != -1:
                        closingbracket = True
                    
                else:
                    padding = userans.find("padding:0px;")
                    if padding != -1:
                        if userans.find("padding:0px;}") != -1:
                            closingbracket = True
                    
                font_size = userans.find("font-size:18px;")
                if font_size != -1:
                    if userans.find("font-size:18px;}") != -1:
                        closingbracket = True
                    
                if not closingbracket or padding == -1 or font_size == -1: # incorrect
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[3], code=code, progress=3, correct=False)

                else:
                    pos = []
                    tags = ["<!doctypehtml>", "<html>", "<head>", "<style>", "ol{", "</style>" "</head>", "<body>", "<ol>", "<li>introduction</li>", "<li>therootsofhtml</li>", "<li>beingamarkuplanguage</li>", "</ol>", "</body>", "</html>"]

                    for tag in tags:
                        temp = userans.find(tag)
                        if temp == -1: # incorrect
                            return render_template("stage7.html", question=STAGE7_QUESTIONS[3], code=code, progress=3, correct=False)

                        pos.append(temp)

                    if pos == sorted(pos) and padding > pos[3] and font_size > pos[3] and padding < pos[5] and font_size < pos[5]: # correct
                        stage7 = Stage7.query.filter_by(email=current_user.email).first()
                        setattr(stage7, qn, 1)
                        db.session.commit()

                        return redirect("/stage7")

                    else: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[3], code=code, progress=3, correct=False)

            elif qn == "q5": # question 5
                if userans.find("<ahref='https://www.informit.com/articles/article.aspx?p=24021&seqnum=0'>article</a>") == -1 and userans.find("<ahref=\"https://www.informit.com/articles/article.aspx?p=24021&seqnum=0\">article</a>") == -1: # incorrect
                    print("what")
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[4], code=code, progress=4, correct=False)

                else:
                    if userans.find("<ahref='https://www.informit.com/articles/article.aspx?p=24021&seqnum=0'>article</a>") != -1:
                        a = userans.find("<ahref='https://www.informit.com/articles/article.aspx?p=24021&seqnum=0'>article</a>")
                    else:
                        a = userans.find("<ahref=\"https://www.informit.com/articles/article.aspx?p=24021&seqnum=0\">article</a>")
                    
                    pos = []
                    tags = ["<!doctypehtml>", "<html>", "<head>", "<style>", "</style>", "</head>", "<body>", "<p1>", "</p1>", "</body>", "</html>"]
                    
                    for tag in tags:
                        temp = userans.find(tag)

                        if temp == -1: # incorrect
                            return render_template("stage7.html", question=STAGE7_QUESTIONS[4], code=code, progress=4, correct=False)

                        pos.append(temp)

                    if pos == sorted(pos) and a > pos[7] and a < pos[8]: # correct
                        stage7 = Stage7.query.filter_by(email=current_user.email).first()
                        setattr(stage7, qn, 1)
                        db.session.commit()

                        return redirect("/stage7")
                        
                    else: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[4], code=code, progress=4, correct=False)

            else: # question 6
                targets = ["<imgsrc='static/images/stage7/italic_tag.jpg'alt='htmlirl'>", "<imgsrc='static/images/stage7/italic_tag.jpg'alt=\"htmlirl\">", "<imgsrc=\"static/images/stage7/italic_tag.jpg\"alt='htmlirl'>", "<imgsrc=\"static/images/stage7/italic_tag.jpg\"alt=\"htmlirl\">"]
                targets += ["<imgalt='htmlirl'src='static/images/stage7/italic_tag.jpg'>", "<imgalt=\"htmlirl\"src='static/images/stage7/italic_tag.jpg'>", "<imgalt='htmlirl'src=\"static/images/stage7/italic_tag.jpg\">", "<imgalt=\"htmlirl\">src=\"static/images/stage7/italic_tag.jpg\""]
                
                for target in targets:
                    img = userans.find(target)
                    print(target, img)
                    if img != -1:
                        break

                if img == -1: # incorrect
                    return render_template("stage7.html", question=STAGE7_QUESTIONS[5], code=code, progress=5, correct=False)

                else:
                    pos = []
                    tags = ["<!doctypehtml>", "<html>", "<head>", "</head>", "<body>", "<p4>", "</body>", "</html>"]
                    
                    for tag in tags:
                        temp = userans.find(tag)

                        if temp == -1: # incorrect
                            return render_template("stage7.html", question=STAGE7_QUESTIONS[5], code=code, progress=5, correct=False)

                        pos.append(temp)

                    if pos == sorted(pos) and img > pos[5]: # correct
                        stage7 = Stage7.query.filter_by(email=current_user.email).first()
                        setattr(stage7, qn, 1)
                        db.session.commit()

                        return redirect("/stage7")
                        
                    else: # incorrect
                        return render_template("stage7.html", question=STAGE7_QUESTIONS[5], code=code, progress=5, correct=False)
                


# Bonus 0: Computational thinking
@app.route("/bonus0", methods=["GET", "POST"])
@login_required
def bonus0():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage
    
    if maxstage < 2:
        return redirect("/submit")

    else:
        if request.method == "GET":
            return render_template("bonus0.html")
        
        else:
            ans = request.form.get("ans")

            if ans == "Guido van Rossum":
                progress = Progress.query.filter_by(email=current_user.email).first()
                progress.bonus0 = datetime.datetime.now()
                db.session.commit()

                return render_template("bonus0.html", correct=True)

            else:
                return render_template("bonus0.html", correct=False)



# Bonus 1: SQL
@app.route("/bonus1", methods=["GET","POST"])
@login_required
def bonus1():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 3:
        return redirect("/submit")
    
    else:
        if request.method == "POST":
            inject = request.form.get("inject")

            if inject == "tHiS_sItE_nOt_SaFe":
                progress = Progress.query.filter_by(email=current_user.email).first()
                progress.bonus1 = datetime.datetime.now()
                db.session.commit()

                return render_template("bonus1.html", correct=True)

            else:
                connection = sqlite3.connect("stage3.db")
                cursor = connection.cursor()
                sq = "SELECT * FROM users WHERE name=\'" + inject + "\'"
                cursor.execute(sq)
                results = cursor.fetchall()
                connection.close()

                return render_template("bonus1.html", results = results)

        else:
            return render_template("bonus1.html")
    


# Bonus 2: Competitive programming
@app.route("/bonus2", methods=["GET", "POST"])
@login_required
def bonus2():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 5:
        return redirect("/submit")

    else:
        if request.method == "GET":
            return render_template("bonus2.html")
        
        else:
            code = request.form.get("code")
            if code:
                # prevent user for accessing files
                if "open" in code or "file" in code:
                    output = "No trying to open files!"
                    return render_template("bonus2.html", code=code, error=output)
                
                else:
                    subtasks = []

                    with open("fibo/fibo.py", 'w') as file:
                        file.write("import sys\nsys.modules['os']=None\nsys.modules['sqlite3']=None\nsys.modules['flask']=None\nsys.modules['subprocess']=None\nsys.modules['sys']=None\ndel sys\n") # prevent importing os and sqlite3
                        file.write(code)

                    for i in range(2):
                        fiboInput = open("fibo/fibo-{}.in".format(i))
                        try:
                            output = subprocess.check_output(["python", "fibo/fibo.py"], timeout=1, stdin=fiboInput).decode("utf-8")
                        except subprocess.TimeoutExpired:
                            output = "Time Limit Exceed. Is your code stuck in an infinite loop? Or is it inefficient?"
                            return render_template("bonus2.html", code=code, error=output)
                        except subprocess.CalledProcessError:
                            output = "There's an error in your code."
                            return render_template("bonus2.html", code=code, error=output)
                        
                        # check answers
                        with open("fibo/fibo-ans-{}.txt".format(i), 'r') as file:
                            ans = list(file)
                        
                        output = output.split("\n")
                        n = len(output) - 1
                        if n != len(ans):
                            subtasks.append(False)
                        
                        else:
                            correct = True
                            for i in range(n):
                                output[i].strip()
                                output[i] = output[i].replace("\r", "")

                                if output[i] != ans[i].strip():
                                    correct = False

                            subtasks.append(correct)

                    if subtasks[0] == True and subtasks[1] == True:
                        progress = Progress.query.filter_by(email=current_user.email).first()
                        progress.bonus2 = datetime.datetime.now()
                        db.session.commit()

                    return render_template("bonus2.html", code=code, subtasks=subtasks)
            
            else: # empty input
                return render_template("bonus2.html")



# Bonus 3: HTML / CSS
@app.route("/bonus3")
@login_required
def bonus3():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage < 7:
        return redirect("/submit")
    return render_template("bonus3.html")



# MOVE UP STAGE PAGE
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    maxstage = Progress.query.filter_by(email=current_user.email).first().mainstage

    if maxstage > 7:
        return redirect("/")
    
    else:
        if request.method == "GET":
            return render_template("submit.html")
        
        else:
            userpsw = request.form.get("psw")

            psw = Mainstage.query.filter_by(stageid=maxstage).first().psw

            if userpsw == psw:
                progress = Progress.query.filter_by(email=current_user.email).first()
                progress.mainstage = maxstage + 1
                setattr(progress, "main{}".format(maxstage), datetime.datetime.now())
                db.session.commit()

                return render_template("submit.html", success=True)

            else:
                return render_template("submit.html", success=False)



# FINAL PORTAL
@app.route("/portal", methods=["GET", "POST"])
@login_required
def portal():
    if request.method == "GET":
        finished = Stage7.query.filter_by(email=current_user.email).first().q6

        if finished == 1:
            return render_template("portal.html")

        else:
            return redirect("/")

    else:
        psw = request.form.get("psw")

        password = Mainstage.query.filter_by(stageid=8).first().psw

        if psw == password:
            progress = Progress.query.filter_by(email=current_user.email).first()
            progress.mainstage += 1
            progress.end = datetime.datetime.now()
            db.session.commit()

            return render_template("congratulations.html")

        else:
            return render_template("portal.html", correct=False)



@app.route("/about")
@login_required
def about():
    return render_template("about.html")



ADMINS = ["alexander.liswandy@dhs.sg", "gu.boyuan@dhs.sg", "zhang.yuxiang@dhs.sg"]

# LEADERBOARDS
@app.route("/leaderboard")
@login_required
def leaderboard():
    data = Progress.query.order_by(Progress.mainstage.desc(), Progress.end.asc(), Progress.main7.asc(), Progress.main6.asc(), Progress.main5.asc(), Progress.main4.asc(), Progress.main3.asc(), Progress.main2.asc(), Progress.main1.asc(), Progress.main0.asc()).all()
    
    for player in data:
        if player.email in ADMINS:
            data.remove(player)

    pos = 0
    n = len(data)
    for i in range(n):
        if data[i].email == current_user.email:
            pos = i+1
            break

    return render_template("leaderboard.html", data=data, pos=pos)



# ADMINS PAGE
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.email not in ADMINS:
            return redirect("/")

    else:
        if request.method == "GET":
            if current_user.email not in ADMINS:
                return redirect("/")

            else:
                data = Progress.query.order_by(Progress.mainstage.desc(), Progress.end.asc(), Progress.main7.asc(), Progress.main6.asc(), Progress.main5.asc(), Progress.main4.asc(), Progress.main3.asc(), Progress.main2.asc(), Progress.main1.asc(), Progress.main0.asc()).all()

                return render_template("admin.html", data=data)

        else:
            operation = request.form.get("operation")
            email = request.form.get("email")
            password = request.form.get("password")
            group = request.form.get("group")

            if operation == "addtoprogress":
                progress = Progress(email=email, psw=password, group=group)
                db.session.add(progress)
                db.session.commit()
            
            elif operation == "changepsw":
                progress = Progress.query.filter_by(email=email).first()
                progress.psw = password
                db.session.commit()

            elif operation == "changegrp":
                progress = Progress.query.filter_by(email=email).first()
                progress.group = int(group)
                db.session.commit()

            return redirect("/admin")



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
    
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["name"]
    else:
        return "User email not available or not verified by Google.", 400
        
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add it to the database.
    player = Player.query.filter_by(id=unique_id).first()
    if player is None:
        player = Player(id=unique_id, name=users_name, email=users_email)
        # progress = Progress(email=users_email)
        stage0 = Stage0(email=users_email)
        stage1 = Stage1(email=users_email)
        stage2 = Stage2(email=users_email)
        stage3 = Stage3(email=users_email)
        stage7 = Stage7(email=users_email)
        db.session.add_all([player, stage0, stage1, stage2, stage3, stage7])
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # for normal local testing use this run
    #app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    # for deployment to heroku app use this
    app.run(host='0.0.0.0', port=port, debug=True)