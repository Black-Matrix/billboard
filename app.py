from cs50 import SQL
from datetime import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///final.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # Show all of the posts made by all of the users in a single page
    posts = db.execute("""SELECT CASE WHEN p.anonymous THEN
                       'Anonymous'ELSE u.username END AS name, p.title AS title, p.post_id AS id,
                       p.posted AS posted FROM users AS u INNER JOIN posts AS p ON u.id = p.user_id ORDER BY p.posted DESC""")
    return render_template("index.html", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        bio = request.form.get("bio")
        if not (username and password and confirmation and bio):
            return apology("Please fill all three fields")
        if password != confirmation:
            return apology("Passwords dosen't match")
        if username.lower() == "anonymous":
            return apology("Sussy Baka", 419)
        # Attempt to create new user
        try:
            user_id = db.execute("INSERT INTO users(username, hash, bio) VALUES(?, ?, ?)",
                             username, generate_password_hash(password), bio)
            session["user_id"] = user_id
            return redirect("/")
        # If username already exists
        except ValueError:
            return apology("Username already exists")
    return render_template("register.html")

@app.route("/create", methods = ["GET", "POST"])
@login_required

# Function to create a new post only if the user is logged in
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        user = session["user_id"]
        title = str(request.form.get("title"))
        if (len(title) == 0) or (len(title) > 100):
            return apology("please let the content between bounds")
        content = str(request.form.get("contents"))
        if (len(content) == 0) or (len(content) > 255):
            return apology("please let the content between bounds")
        anonymous = str(request.form.get("anonymous"))
        print(title, content, user, anonymous)
        if (user and content):
            try:
                # if the user wants the post to be anonymous
                if anonymous == "on":
                    db.execute("INSERT INTO posts(user_id, title, contents, anonymous) VALUES(?, ?, ?, TRUE)", user, title, content)
                # else if the user dosent want the post to be anonymous
                elif anonymous != "on" :
                    db.execute("INSERT INTO posts(user_id, title, contents, anonymous) VALUES(?, ?, ?, FALSE)", user, title, content)
                else:
                    db.execute("INSERT INTO posts(user_id, title, contents) VALUES(?, ?, ?)", user, title, content)
            except:
                 return apology("something wrong with your input please try later")
        return redirect("/")

@app.route("/posts/<int:id>")
def posts(id):
    # to fetch a post based on the post ID
    try:
        post = db.execute("""SELECT CASE WHEN p.anonymous THEN
                        'Anonymous'ELSE u.username END AS name,
                        p.title AS title, p.posted, p.contents
                        FROM posts AS p INNER JOIN users AS u ON
                        u.id = p.user_id
                        WHERE p.post_id = ?""", id)
        if len(post) == 0:
            return apology("Skill issue", 404)
    except:
        return apology("Something went wrong, sorry", 500)
    date = datetime.strptime(post[0]["posted"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y at %I:%M %p")

    return render_template("posts.html", post=post[0], date=date)

@app.route("/profile/Anonymous")

# Find this functionality for youself ;)
def anonymous():
    return redirect("https://www.youtube.com/watch?v=QDia3e12czc")

@app.route("/me")
@login_required

# to display one's own profile when they are logged in
def me():
    try:
        uid = session["user_id"]
        uname = db.execute("SELECT username FROM users WHERE id = ?", uid)[0]["username"]
        return redirect(f"/profile/{uname}")
    except:
        return apology("Could not find your profile.")

@app.route("/profile/<string:usr>")

# to display a user's profile consisting their post history
def profile(usr):
    try:
        username = ""
        logged = False
        if session:
            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        result = db.execute("SELECT id, bio FROM users WHERE username = ?", usr)
        if len(result) == 0:
            return apology("No can do", 404)

        user_id, bio= result[0]["id"], result[0]["bio"]
        posts = []

        # if the logged in user is same as the request's user profile then also display anonymous posts
        if username and len(username) > 0 and username[0]["username"] == usr:
            posts = db.execute("""SELECT u.username AS name, p.title AS title, p.post_id AS id,
                            p.posted AS posted, p.anonymous as anonymous
                            FROM users AS u INNER JOIN posts AS p ON u.id = p.user_id WHERE u.id = ?""", user_id)
            logged = True
        else:
            posts = db.execute("""SELECT u.username AS name, p.title AS title, p.post_id AS id,
                            p.posted AS posted
                            FROM users AS u INNER JOIN posts AS p ON u.id = p.user_id WHERE p.anonymous = FALSE AND u.id = ?""", user_id)
        return render_template("profile.html", posts=posts, bio=bio, username=usr, logged=logged)
    except:
        return apology("Something went wrong, sorry", 500)

@app.route("/delete/<int:id>", methods=["POST"])
@login_required

def delete(id):
    if request.method == "POST":
        uname = request.form.get("uname")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        print(uname, username)
        try:
            if uname == username:
                db.execute("DELETE FROM posts WHERE post_id = ?", id)
        except:
            return apology("Sussy Baka", 419)
    return redirect(f"/profile/{uname}")


@app.route("/updatebio/<string:uname>", methods=["POST"])
@login_required

def update_bio(uname):
    if request.method == "POST":
        bio = request.form.get("bio")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        print(uname, username)
        try:
            if uname == username and len(bio) != 0:
                db.execute("UPDATE users SET bio = ? WHERE username = ?",bio, uname)
        except:
            return apology("Sussy Baka", 419)
    return redirect(f"/profile/{uname}")


@app.route("/changepassword/<string:uname>", methods=["POST"])
@login_required

def update_pass(uname):
    if request.method == "POST":
        current = request.form.get("current_password")
        new = request.form.get("new_password")
        result = db.execute("SELECT username, hash FROM users WHERE id = ?", session["user_id"])
        username = result[0]["username"]
        uhash = result[0]["hash"]
        passcheck = check_password_hash(uhash, current)
        if not passcheck:
            return apology("wrong password")
        try:
            if uname == username and passcheck:
                db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(new), uname)
        except:
            return apology("Sussy Baka", 419)
    return redirect("/logout")

