from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.saving import Saving

@app.route('/add/saving')
def add_savings_page():
    return render_template('add_saving.html', user_id = session['user_id'])

@app.route('/create/savings', methods = ['POST'])
def add_savings():
    if Saving.create_savings(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/add/saving')
    
@app.route('/edit/savings/<int:id>')
def edit_savings_page(id):
    saving = Saving.get_savings_by_id(id)
    return render_template("edit_savings.html", saving = saving)

@app.route("/update/saving/<int:id>", methods = ["POST"])
def update_saving(id):
    if not Saving.savings_validations(request.form):
        return redirect(f"/edit/savings/{id}")
    else:
        data = {
            "id": id,
            "name": request.form["name"],
            "amount": request.form["amount"]
        }
        Saving.edit_savings(data)
        return redirect("/dashboard")
    
@app.route('/delete/savings/<int:id>')
def delete_savings(id):
    Saving.delete_savings_by_id(id)
    return redirect('/dashboard')