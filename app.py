from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functools import wraps
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
UPLOAD_FOLDER = "/static/imag/"
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQL("sqlite:///MentorIQ.db")
global courses
courses=db.execute("SELECT * FROM COURSES")
global Teq
Teq=db.execute("SELECT * FROM TEQ")

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    numvid=db.execute("SELECT COUNT(id) FROM COURSES")
    numvTeq=db.execute("SELECT COUNT(id) FROM TEQ")
    return render_template("index.html",numvid=numvid,numvTeq=numvTeq)

@app.route("/FrontEnd", methods=["GET", "POST"])
def FrontEnd():
    return render_template("FrontEnd.html")


@app.route("/HtmlC", methods=["GET", "POST"])
def HtmlC():
    if request.method == "POST":
        COURSES = request.form['COURSES']
        # search by course name
        COURSES = db.execute("SELECT * from COURSES WHERE Type = 'Html'", COURSES=COURSES)
        # all in the search box will return all the rows
        if len(COURSES) == 0: 
            COURSES = db.execute("SELECT * from COURSES WHERE Type = 'Html'")
        return render_template('HtmlC.html', COURSES=COURSES)
    else:
        COURSES = db.execute("SELECT * FROM COURSES WHERE Type = 'Html'")
        return render_template("HtmlC.html", COURSES=COURSES)
@app.route("/HtmlE", methods=["GET", "POST"])
def HtmlE():
    return render_template("HtmlE.html")
# if __name__ == "__main__":
#     app.run(port=5000, debug=True)