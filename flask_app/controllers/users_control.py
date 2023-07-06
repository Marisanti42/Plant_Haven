from flask import flash, redirect, render_template, request, session
from flask_app.models import plants_model, users_model
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Landing page route
@app.route("/")
def index():
    return render_template('index.html')

#Login/Register route
@app.route("/submit",methods=["POST"])
def submit():
    if request.form['action'] == 'register': 
        is_valid = users_model.User.validate_user(request.form)    #check validity
        if not is_valid:
            return redirect("/")
        pw_hash = bcrypt.generate_password_hash(request.form['password']) #hash password
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password':pw_hash
        }
        id = users_model.User.save_user(data)
        print(f"THIS IS THE ID: {id}")
        session['user_id'] = id                             #Session ID Register
        session['first_name'] = request.form["first_name"]
        return redirect("/dash")
    else:
        is_valid = users_model.User.validate_login(request.form)
        if not is_valid:
            return redirect("/")
        this_user = users_model.User.get_user_by_email(request.form['email'])
        if not this_user:
            flash("Invalid Email/Password")
            return redirect("/")
        if not bcrypt.check_password_hash(this_user.password, request.form['password']):
            flash("Invalid Email/Password")
            return redirect("/")
        session["user_id"]=this_user.id             #Session ID Login
        session["first_name"]=this_user.first_name
        return redirect("/dash")

#dash route
@app.route("/dash") 
def all_plants():
    if "user_id" not in session:
        return redirect("/")
    first_name = session["first_name"]
    plants = plants_model.Plant.get_all_plants()
    id = session["user_id"]
    return render_template("dash.html", plants=plants, first_name=first_name, id=id)

#Account Page route
@app.route("/user/account/<int:id>")
def user_page(id):
    if "user_id" not in session:
        return redirect("/")
    first_name = session["first_name"]
    id = session["user_id"]
    plants = plants_model.Plant.get_all_plants()
    return render_template("account.html", first_name=first_name,id=id, plants=plants)

#Logout route
@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/")
