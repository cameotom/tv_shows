from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/shows')
def dashboard():
    if 'user_id' not in session:
        print("user id not in session")
        return redirect('/user/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("shows.html", user = User.get_user_by_id(data), shows = Show.get_all_shows())

@app.route('/shows/<int:id>')
def one_show(id):
    if 'user_id' not in session:
        return redirect('/user/logout')
    data = {
        'id': id
    }
    show = Show.get_one_show(data)
    data2 = {
        'id': show.user_id
    }
    return render_template("view_show.html", show = Show.get_one_show(data), user = User.get_user_by_id(data2))

@app.route('/shows/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template("create_show.html", user = user)

@app.route('/create_show', methods=["POST"])
def create_show():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not Show.validate_creation(request.form):
        return redirect('/shows/create')

    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": request.form["user_id"]
    }
    # We pass the data dictionary into the save method from the user class.
    Show.create_show(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/shows')

@app.route('/shows/edit/<int:id>')
def show_edit(id):
    data = {
        "id": id
    }
    return render_template("edit_show.html", show = Show.get_one_show(data))


@app.route('/shows/edit', methods=['POST'])
def edit_show():
    show_id = request.form["id"]
    if not Show.validate_edit(request.form):
        return redirect(f"/shows/edit/{show_id}")
    Show.update(request.form)
    return redirect('/shows')

@app.route('/shows/delete/<int:id>')
def show_delete(id):
    data = {
        "id": id
    }
    Show.delete(data)
    return redirect('/shows')