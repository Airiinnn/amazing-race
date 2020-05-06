# Python standard libraries
import json
import os
import sqlite3
import csv

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
        cursor.execute("SELECT stage FROM user WHERE id='{}'".format(current_user.id))
        maxstage = cursor.fetchone()[0]
        connection.close()

        with open("stages.csv", 'r') as file:
            reader = csv.reader(file)
            stages = list(reader)

        return render_template("index.html", maxstage=maxstage, stages=stages)
    else:
        return render_template("login.html")

#STAGE 0: Cyber Security, KEY: --NIL--
        
@app.route("/stage0")
@login_required
def stage0():
    with open("stage0.csv", 'r') as file:
        reader = csv.reader(file)
        questions = [read[0:5] for read in reader]
    # print(questions)    
    return render_template("stage0.html",questions = questions)

@app.route("/stage0/submission", methods=['POST'])
@login_required
def stage0_submission():
    with open("stage0.csv", 'r') as file:
        reader = csv.reader(file)
        everything = [read for read in reader]
        questions = [read[0:5] for read in everything]
        answers = [read[-2] for read in everything]
        tips = [read[-1] for read in everything]
    #print(answers)    
    correct = []
    marks = 0
    for i in range(len(answers)):
        #print(request.form[str(i+1)])
        if str(request.form[str(i+1)]) == answers[i]:
            marks += 1
            correct.append('y')

        else:
            correct.append(request.form[str(i+1)])

    print(correct)
    print(answers)
    return render_template("stage0_submission.html", correct=correct, marks=marks, questions = questions,answers = answers,tips = tips)




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

@app.route("/stage2")
@login_required
def stage2():
    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    cursor.execute("SELECT stage FROM user WHERE id='{}'".format(current_user.id))
    maxstage = cursor.fetchone()[0]
    connection.close()
    
    if maxstage < 2:
        return render_template("submit.html")
    return render_template("stage2.html")

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
    cursor.execute("SELECT stage FROM user WHERE id='{}'".format(current_user.id))
    maxstage = cursor.fetchone()[0]
    connection.close()
    
    if maxstage < 1:
        return render_template("submit.html")
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
    return render_template("stage3_submission.html", results=results, res = res)




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
# @login_required
def stage5():
    if request.method == "GET":
        return render_template("stage5.html")
    else:
        code = request.form.get("code")
        with open("paint/paint.py", 'w') as file:
            file.writelines(code)

        # exec(open("paint.py").read())
        # return code
        cmd = "podman build -t paint-python ."
        os.system(cmd)
        cmd = "podman run -p 3333:3333 hello-world-python"
        os.system(cmd)

        return yes


@app.route("/stage5/submission", methods=["POST"])
# login_required
def stage5_submission():
    #type here
    pass






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











#STAGE 8: JAVASCRIPT, KEY: hi8

@app.route("/stage8")
@login_required
def stage8():
    #type here
    pass




@app.route("/stage8/submission", methods=["POST"])
@login_required
def stage8_submission():
    #type here
    pass









#KEY INSERT, TO GET TO NEXT STAGE

@app.route("/submission", methods=["POST"])
@login_required
def submission():
    psw = request.form.get("psw")

    connection = sqlite3.connect("sqlite_db")
    cursor = connection.cursor()
    cursor.execute("SELECT stage FROM user WHERE id='{}'".format(current_user.id))
    maxstage = cursor.fetchone()[0]
    with open("stages.csv", 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
    if psw == lines[maxstage+1][3]:
        cursor.execute("UPDATE user SET stage=stage+1 WHERE id=(?)", (current_user.id,))
        connection.commit()
        connection.close()
        return redirect(lines[maxstage+1][2])
    else:
        connection.close()
        return render_template("failure.html")

    







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
    #app.debug = False
    #for normal local testing use this run
    #app.run(ssl_context="adhoc",host='127.0.0.1', port=port, debug=True)
    #for deployment to heroku app use this
    app.run(host='0.0.0.0', port=port, debug=True)