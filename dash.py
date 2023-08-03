from flask import Flask, render_template, request, redirect, url_for, flash, session
from cs50 import SQL
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("static/img")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQL("sqlite:///MentorIQ.db")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('AdminLogin'))
    return wrap

def image_path(file):
    filename = ''
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'img', filename)
    return file_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/AdminPanel")
@login_required
def AdminPanel():
    num_vid = db.execute("SELECT COUNT(id) FROM COURSES")
    num_teq = db.execute("SELECT COUNT(id) FROM TEQ")
    return render_template("AdminPanel.html", numvid=num_vid, numvTeq=num_teq)

@app.route("/", methods=["GET", "POST"])
@app.route("/AdminLogin", methods=["GET", "POST"])
def AdminLogin():
    """Log admin in"""

    # Forget any admin_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for admin account
        p=request.form.get("password")
        rows = db.execute("SELECT * FROM admins WHERE name = :name AND password = :p", name=request.form.get("name"),p= p)
        print("SELECT * FROM admins WHERE name ='"+request.form.get("name")+"' AND password ='"+ p+"'")
        # Ensure admin name was submitted
        if not request.form.get("name"):
            return render_template("AdminLogin.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash('must provide password')
            return render_template("AdminLogin.html")
      
        # Ensure name exists and password is correct
       
        print(len(rows))       
        if len(rows) != 1 :
            return render_template("AdminLogin.html")

        # Redirect admin to home page
        session['name']=request.form.get('name')
        return redirect(url_for('AdminPanel'))
    # User reached route via GET (as by clicking a link or via redirect)
    else :
        return render_template("AdminLogin.html")
#------------------- Admin Logout ---------------------------------------------------------------------------#
@app.route("/logout")
def logout():
    """Log admin out"""

    # Forget any admin_id
    session.clear()

    flash("You have been logged out")

    # Redirect admin to login form
    return redirect(url_for('AdminLogin'))

#------------------- Admin Posts ---------------------------------------------------------------------------#
@app.route("/AdminPosts", methods=["GET", "POST"])
@login_required
def AdminPosts():
    if request.method == "POST":
        COURSES = request.form['COURSES']
        # search by course name
        COURSES = db.execute("SELECT * from COURSES", COURSES=COURSES)
        # all in the search box will return all the rows
        if len(COURSES) == 0: 
            COURSES = db.execute("SELECT * from COURSES")
        return render_template('AdminPosts.html', COURSES=COURSES)
    else:
        COURSES = db.execute("SELECT * FROM COURSES")
        return render_template("AdminPosts.html", COURSES=COURSES)

@app.route("/DeleteCourse/<id>")
@login_required
def DeleteCourse(id):
    db.execute("DELETE FROM COURSES WHERE id = :id", id=id)
    return redirect(url_for('AdminPosts'))


@app.route("/AdminAddPost", methods=["GET", "POST"])
@login_required
def AdminAddPost():
    if request.method == "GET":
        COURSES = db.execute("SELECT * FROM COURSES")
        TEQ = db.execute("SELECT * FROM TEQ")
        return render_template("AdminAddPost.html", COURSES=COURSES, TEQ=TEQ)
    else:
        name = request.form.get("name")
        VidNum = request.form.get("VidNum")
        Type = request.form.get("Type")
        ins = request.form.get("ins")
        link = request.form.get("link")
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        img = image_path(file)
        db.execute("INSERT INTO COURSES (name, VidNum, Type, ins, link, img) VALUES (:name, :VidNum, :Type, :ins, :link, :img)",
                   name=name, VidNum=VidNum, Type=Type, ins=ins, link=link, img=img)
        return redirect(url_for('AdminPosts'))

@app.route("/AdminTeq", methods=["GET", "POST"])
@login_required
def AdminTeq():
    if request.method == "POST":
        TEQ = request.form['TEQ']
        # search by course name
        TEQ = db.execute("SELECT * from TEQ", TEQ=TEQ)
        # all in the search box will return all the rows
        if len(TEQ) == 0: 
            TEQ = db.execute("SELECT * from TEQ")
        return render_template('AdminTeq.html', TEQ=TEQ)
    else:
        TEQ = db.execute("SELECT * FROM TEQ")
        return render_template("AdminTeq.html", TEQ=TEQ)

@app.route("/DeleteTeq/<id>")
@login_required
def DeleteTeq(id):
    db.execute("DELETE FROM TEQ WHERE id = :id", id=id)
    return redirect(url_for('AdminTeq'))

@app.route("/AdminAddTeq", methods=["GET", "POST"])
@login_required
def AdminAddTeq():
    if request.method == "GET":
        TEQ = db.execute("SELECT * FROM TEQ")
        return render_template("AdminAddTeq.html",TEQ=TEQ )
    else:
        T_name = request.form.get("T_name")
        db.execute("INSERT INTO TEQ (T_name) VALUES (:T_name)",
                        T_name=T_name)
        return redirect(url_for('AdminTeq'))