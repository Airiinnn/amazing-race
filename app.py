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
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = "685992959593-701prlcssas6vu8h87srulmbr6t40hg2.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "zKHCQ2IYsBdn50r7Umyy2ZUM"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    
@app.route("/")
def index():
    if current_user.is_authenticated:
        connection = sqlite3.connect("sqlite_db")
        cursor = connection.cursor()
        cursor.execute("SELECT mainstage FROM progress WHERE email='{}'".format(current_user.email))
        maxstage = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM mainstage")
        main_stages = cursor.fetchall()

        cursor.execute("SELECT * FROM bonusstage")
        bonus_stages = cursor.fetchall()
        connection.close()

        return render_template("index.html", maxstage=maxstage, main_stages=main_stages, bonus_stages=bonus_stages)
    else:
        return render_template("login.html")
        
#STAGE 0: Cyber Security, KEY: protecc
connection = sqlite3.connect("sqlite_db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage0questions")
STAGE0_QUESTIONS = cursor.fetchall()
connection.close()
    
@app.route('/stage0', methods=["GET", "POST"])
@login_required
def stage0_main():
    if request.method == "GET":
        connection = sqlite3.connect("sqlite_db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stage0 WHERE email='{}'".format(current_user.email))
        stage0_progress = cursor.fetchone()
        connection.close()
        
        stage0_incomplete = [i for i in range(1, 21) if stage0_progress[i] == 0]
        if len(stage0_incomplete) == 0:
            return render_template("stage0_success.html")

        else:
            return render_template("stage0.html", question=STAGE0_QUESTIONS[random.choice(stage0_incomplete)-1], progress=20-len(stage0_incomplete))
    
    else:
        qn = request.form.get("qn")
        ans = request.form.get("ans")
        progress = request.form.get("progress")

        for question in STAGE0_QUESTIONS:
            if question[0] == qn:
                if ans == question[6]: # correct
                    connection = sqlite3.connect("sqlite_db")
                    connection.execute("UPDATE stage0 SET {}=1 WHERE email='{}'".format(question[0], current_user.email))
                    connection.commit()
                    connection.close()

                    return redirect("/stage0")

                else: # incorrect
                    return render_template("stage0.html", question=question, correct=False, progress=progress)



#STAGE 1: PYTHON BASICS, KEY: hi1

@app.route("/stage1")
@login_required
def stage1():
    #type here
    pass




@app.route("/stage1/submission", methods=["POST"])
@login_required
def stage1_submission():
    #type here
    pass






#STAGE 2: COMPUTATIONAL THINKING, KEY: hi2
connection = sqlite3.connect("sqlite_db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM stage2questions")
STAGE2_QUESTIONS = cursor.fetchall()
connection.close()

@app.route("/stage2", methods=["GET", "POST"])
@login_required
def stage2():
    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    cursor.execute("SELECT mainstage FROM progress WHERE email='{}'".format(current_user.email))
    maxstage = cursor.fetchone()[0]
    connection.close()
    
    if maxstage < 2:
        return redirect("/submit")

    else:
        if request.method == "GET":
            connection = sqlite3.connect("sqlite_db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM stage2 WHERE email='{}'".format(current_user.email))
            stage2_progress = cursor.fetchone()
            connection.close()

            print(STAGE2_QUESTIONS)
            print(stage2_progress)

            for i in range(1, 9):
                if stage2_progress[i] == 0:
                    return render_template("stage2.html", question=STAGE2_QUESTIONS[i-1], progress=i-1)

            return render_template("stage2_success.html")
        
        else:
            qn = request.form.get("qn")
            ans = request.form.get("ans")
            progress = request.form.get("progress")

            for question in STAGE2_QUESTIONS:
                if question[0] == qn:
                    if ans == question[2]: # correct
                        connection = sqlite3.connect("sqlite_db")
                        connection.execute("UPDATE stage2 SET {}=1 WHERE email='{}'".format(question[0], current_user.email))
                        connection.commit()
                        connection.close()

                        return redirect("/stage2")

                    else: # incorrect
                        return render_template("stage2.html", question=question, correct=False, progress=progress)

@app.route("/stage2/submission", methods=["POST"])
@login_required
def stage2_submission():
    correct = ["31", "37777", "45", "5", "8", "83", "buildingblocs", "42"]
    answers = []
    results = []
    score = 0
    answers.append(request.form.get("ans1"))
    answers.append(request.form.get("ans2"))
    answers.append(request.form.get("ans3"))
    answers.append(request.form.get("ans4"))
    answers.append(request.form.get("ans5"))
    answers.append(request.form.get("ans6"))
    answers.append(request.form.get("ans7"))
    answers.append(request.form.get("ans8"))
    
    for i in range(8):
        if correct[i] == answers[i]:
            results.append(True)
            score += 1
        else:
            results.append(False)
        
    print(answers)

    return render_template("stage2_submission.html", answers=answers, results=results, score=score)





#STAGE 3: SQL, KEY: hi3

@app.route("/stage3")
@login_required
def stage3():
    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    cursor.execute("SELECT mainstage FROM progress WHERE email='{}'".format(current_user.email))
    maxstage = cursor.fetchone()[0]
    connection.close()
    
    if maxstage < 3:
        return redirect("/submit")
    return render_template("stage3.html")

@app.route("/stage3/submission", methods=["POST"])
@login_required
def stage3_submission():
    corr1 = True
    corr2 = True
    corr3 = True
    q1 = request.form.get("q1")
    q2 = request.form.get("q2")
    q3 = request.form.get("q3")
    if q1 != "SELECT * FROM sql_data":
        corr1 = False
    if q2 != "SELECT * FROM sql_data WHERE id=1":
        corr2 = False
    if q3 != "INSERT INTO sql_data (id) VALUES (1)":
        corr3 = False
    inject = request.form.get("inject")
    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    #n = ("test2", "staffkuanxin")
    #cursor.execute("INSERT INTO sql_test (name, password) VALUES (?, ?)", n)  
    sq = "SELECT * FROM sql_users WHERE name=\'" + inject + "\'"
    #ans: 'or''='
    print(sq)
    cursor.execute(sq)
    results = cursor.fetchall()
    res = ""
    if not corr1:
        res = "Error, please enter correct answer for Q1 first"
        results = None
    elif not corr2:
        res = "Error, please enter correct answer for Q2 first"
        results = None
    elif not corr3:
        res = "Error, please enter correcct answer for Q3 first"
        results = None

    connection.close()
    return render_template("stage3_submission.html", results=results, res=res)




#STAGE 4: NOSQL, KEY: hi4

@app.route("/stage4")
@login_required
def stage4():
    #type here
    pass




@app.route("/stage4/submission", methods=["POST"])
@login_required
def stage4_submission():
    #type here
    pass






#STAGE 5: COMPETITIVE PROGRAMMING, KEY: hi5

@app.route("/stage5", methods=["GET", "POST"])
@login_required
def stage5():
    if request.method == "GET":
        connection = sqlite3.connect("sqlite_db")
        cursor = connection.cursor()
        cursor.execute("SELECT mainstage FROM progress WHERE email='{}'".format(current_user.email))
        maxstage = cursor.fetchone()[0]
        connection.close()

        if maxstage < 5:
            return redirect("/submit")
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
    #type here
    pass




@app.route("/stage6/submission", methods=["POST"])
@login_required
def stage6_submission():
    #type here
    pass









#STAGE 7: HTML / CSS, KEY: hi7

@app.route("/stage7")
@login_required
def stage7():
    #type here
    pass

@app.route("/stage7/submission", methods=["POST"])
@login_required
def stage7_submission():
    #type here
    pass



# Bonus 0: Computational thinking:
@app.route("/bonus0")
@login_required
def bonus0():
    pass




# Bonus 1: SQL:
@app.route("/bonus1")
@login_required
def bonus1():
    pass





# Bonus 2: Competitive programming:
@app.route("/bonus2")
@login_required
def bonus2():
    pass





# Bonus 3: HTML / CSS:
@app.route("/bonus3")
@login_required
def bonus3():
    pass


#KEY INSERT, TO GET TO NEXT STAGE

@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    
    else:
        userpsw = request.form.get("psw")

        connection = sqlite3.connect("sqlite_db")
        cursor = connection.cursor()
        cursor.execute("SELECT mainstage FROM progress WHERE email='{}'".format(current_user.email))
        maxstage = cursor.fetchone()[0]

        cursor.execute("SELECT psw FROM mainstage WHERE stageid='{}'".format(maxstage))
        psw = cursor.fetchone()[0]

        if userpsw == psw:
            cursor.execute("UPDATE progress SET mainstage=mainstage+1, lastupdated=(?) WHERE email=(?)", (datetime.datetime.now(), current_user.email,))
            connection.commit()
            connection.close()
            return render_template("submit.html", success=True)

        else:
            connection.close()
            return render_template("submit.html", success=False)

    







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
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email)


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