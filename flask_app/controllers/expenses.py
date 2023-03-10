from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.income import Income
from flask_app.models.expense import Expense


@app.route('/add/expense')
def render_expense_page():
    return render_template('add_expense.html', user_id = session['user_id'])

@app.route('/create/expense', methods = ['POST'])
def add_expense():
    if Expense.create_expense(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/add/expense')
    
@app.route("/edit/expenses/<int:id>")
def expense_edit_page(id):
    expense = Expense.get_expense_by_id(id)
    return render_template("edit_expenses.html", expense = expense)

@app.route("/update/expense/<int:id>", methods = ["POST"])
def update_expense(id):
    isValid = True
    if not Expense.expense_validations(request.form):
        return redirect(f"/edit/expenses/{id}")
    else:
        data = {
            "id": id,
            "name": request.form["name"],
            "amount": request.form["amount"]
        }
        Expense.edit_expense(data)
        return redirect("/dashboard")
    
@app.route('/delete/expense/<int:id>')
def delete_expense(id):
    Expense.delete_expense_by_id(id)
    return redirect('/dashboard')
