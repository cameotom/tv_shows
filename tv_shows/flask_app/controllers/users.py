from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/user/create', methods=["POST"])
def user_create():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_registration(request.form):
        return redirect('/register')

    hashed_password = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_password
    }
    # We pass the data dictionary into the save method from the user class.
    user_id = User.create_user(data)
    session['user_id'] = user_id
    # Don't forget to redirect after saving to the database.
    return redirect('/shows')

@app.route('/user/login', methods=["POST"])
def user_login():
    user_in_db = User.get_user_by_email(request.form)
    if not user_in_db:
        flash("Email not registered")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Password")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/shows')

@app.route('/users')
def users():
    users = User.get_all_users()
    return render_template("users.html", users = users)

@app.route('/user/logout')
def user_logout():
    session.clear()
    return redirect('/')

