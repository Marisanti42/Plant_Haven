from flask import flash, redirect, render_template, request, session
from flask_app.models import plants_model
from flask_app import app

#Plant a plant route
@app.route("/new/plant")
def new_plant():
    if "user_id" not in session:
        return redirect ("/")
    first_name = session["first_name"]
    id = session["user_id"]
    return render_template("new_plant.html", first_name=first_name, id=id)

#New plant added to database
@app.route("/plant/create", methods=["POST"])
def add_plant():
    if "user_id" not in session:
        return redirect("/")
    is_valid = plants_model.plant.validate_plant(request.form)
    if not is_valid:
        return redirect("/new/plant")
    else:
        data = {
            'plant_name':request.form["plant_name"],
            'type':request.form["type"],
            'info':request.form["info"],
            'date_planted':request.form["date_planted"],
            'user_id':session["user_id"]
        }
        plants_model.plant.new_plant(data)
        return redirect("/dash")

#View a specific plant route 
@app.route("/show/<int:id>")
def show_plant(id):
    if "user_id" not in session:
        return redirect("/")
    first_name = session["first_name"]
    this_plant = plants_model.plant.view_plant(id)
    id = session["user_id"]
    return render_template("show_plant.html", first_name=first_name, plant=this_plant, id=id)

#Edit a plant route
@app.route("/edit/<int:id>")
def edit_plant(id):
    if 'user_id' not in session:
        return redirect("/")
    first_name = session["first_name"]
    plants = plants_model.plant.view_plant(id)
    id = session["user_id"]
    return render_template("edit_plant.html", plant=plants, first_name=first_name, id=id)

#plant is updated in the database
@app.route("/edit/<int:id>/update", methods=["POST"])
def update_plant(id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = plants_model.plant.validate_plant(request.form)
    if not is_valid:
        return redirect(f"/edit/{id}")
    else:
        data = {
            'plant_name':request.form["plant_name"],
            'type':request.form["type"],
            'info':request.form["info"],
            'user_id':session["user_id"],
            'id':id
        }
        plants_model.plant.update_plant(data)
        return redirect("/dash")

#Delete a plant route
@app.route("/edit/<int:id>/destroy")
def delete_plant(id):
    if 'user_id' not in session:
        return redirect("/")
    plants_model.plant.delete_plant(id)
    return redirect(f"/user/account/{id}")

