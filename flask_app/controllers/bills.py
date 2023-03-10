from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.bill import Bill
from flask_app.models.income import Income

@app.route('/add/bill')
def add_bill_page():
    return render_template('add_bill.html', user_id = session['user_id'])

@app.route("/create/bill", methods = ['POST'])
def add_bill():
    if Bill.create_bill(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/add/bill')

@app.route("/edit/bills/<int:id>")
def bill_edit_page(id):
    bill = Bill.get_bill_by_id(id)
    return render_template('edit_bill.html', bill = bill)

@app.route("/update/bill/<int:id>", methods = ["POST"])
def update_bill(id):
    isValid = Bill.bill_validations(request.form)
    if not isValid:
        return redirect(f"/edit/bills/{id}")
    else:
        data = {
            "id": id,
            "name": request.form["name"],
            "amount": request.form["amount"]
        }
        Bill.edit_bill(data)
        return redirect('/dashboard')
    
@app.route('/delete/bill/<int:id>')
def delete_bill(id):
    Bill.delete_bill_by_id(id)
    return redirect('/dashboard')