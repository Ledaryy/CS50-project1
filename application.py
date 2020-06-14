import os
import requests

from flask import Flask, session, render_template
from flask import request
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

notes = []
   
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "z4TB9KudCF5ImXc74SI32A", "isbns": "9781632168146"})
print(res.json())


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:
        session["notes"] = []
    
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)
    
    return render_template("index.html", notes=session["notes"])
