import os
import requests

from flask import Flask, session, render_template
from flask import request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



   
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "z4TB9KudCF5ImXc74SI32A", "isbns": "9781632168146"})
print(res.json())
  
@app.route("/", methods=["POST", "GET"])
def index():
    users = db.execute("SELECT * FROM users").fetchall()
    if request.method == "POST":
    
        username = str(request.form.get("username"))
        try:
            password = int(request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="ERR:1 - Use only numbers in password")

        if db.execute("SELECT * FROM users WHERE username = :username AND userpassword = :password", 
                    {"username":username, "password":password}).rowcount >= 1:
             return redirect(url_for("user", user_id = username))
        elif db.execute("SELECT * FROM users WHERE username = :username AND userpassword = :password", 
                    {"username":username, "password":password}).rowcount <= 0:
             return render_template("error.html", message="ERR:2 - Wrong username/password")
            

    return render_template("index.html")

@app.route("/registration", methods=["POST", "GET"])
def registration():
    users = db.execute("SELECT * FROM users").fetchall()
    if request.method == "POST":
        isonline = 0
        
        username = str(request.form.get("username"))
        try:
            password = int(request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="ERR:3 - Use only numbers in password")
        
        if db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount >= 1:
            return render_template("error.html", message="ERR:4 - User already exist")
        
        db.execute("INSERT INTO users (username, userpassword, isonline) VALUES (:username, :userpassword, :isonline)",
                    {"username":username, "userpassword":password, "isonline":isonline})
        db.commit()
        return render_template("success.html", message="Registration completed")
    
    return render_template("registration.html")

@app.route("/<user_id>")
def user(user_id):
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("main.html", users=users)
    






  #  if request.method == "POST":
  #      isonline = 0
  #      username = request.form.get("username")
  #      password = request.form.get("password")
  #     # users = db.execute("SELECT username FROM users").fetchall()
  #      db.execute("INSERT INTO users (username, userpassword, isonline) VALUES (:username, :userpassword, :isonline)",
  #              {"username":username, "userpassword":password, "isonline":isonline})
  #      db.commit()
  #      
  #      return render_template("index.html")




#@app.route("/", methods=["GET", "POST"])
#def index():
#    if session.get("notes") is None:
#        session["notes"] = []
#    
#    if request.method == "POST":
#        note = request.form.get("note")
#        session["notes"].append(note)
#    
#    return render_template("index.html", notes=session["notes"])

