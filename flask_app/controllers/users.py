from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.income import Income
from flask_app.models.user import User
from flask_app.models.bill import Bill
from flask_app.models.expense import Expense
from flask_app.models.saving import Saving

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ["POST"])
def register_user():
    if User.create_user(request.form):
        return redirect('/income')
    else:
        return redirect('/')

@app.route('/dashboard')
def render_dashboard():
    if not Income.display_income_by_user_id(session['user_id']):
        return redirect('/income')
    else:
        #** Establishing all data that will be used and displayed in the dashboard
        one_income = Income.display_income_by_user_id(session['user_id'])
        user_with_bills = User.get_all_bills_from_one_user_by_user_id(session['user_id'])
        user_with_expenses = User.get_all_expenses_from_one_user_by_user_id(session['user_id'])
        user_with_savings = User.get_all_savings_from_one_user_by_user_id(session['user_id'])
        #** Getting all totals from the bills, expenses, and savings list that belong to the user
        bill_total = Bill.get_all_bill_total(session["user_id"])
        expense_total = Expense.get_all_expense_total(session["user_id"])
        saving_total = Saving.get_all_savings_total(session["user_id"])
        total = bill_total + expense_total + saving_total
        #** Figuring percentages used for each category
        income_after_all_math = one_income.amount - total
        fifty_percent_of_income = round(one_income.amount * .5)
        thirty_percent_of_income = round(one_income.amount * .3)
        twenty_percent_of_income = round(one_income.amount * .2)

    return render_template('dashboard.html', user_id = session['user_id'], user_name = session['user_name'], 
    income = one_income, user_with_bills = user_with_bills, user_with_expenses = user_with_expenses,
    user_with_savings = user_with_savings, income_after_expenses = income_after_all_math, fifty_percent = fifty_percent_of_income, thirty_percent = thirty_percent_of_income,
    twenty_percent = twenty_percent_of_income, bill_total = bill_total, expense_total = expense_total, saving_total = saving_total)

@app.route('/login', methods = ['POST'])
def login_user():
    if User.login_user(request.form):
        try:
            Income.display_income_by_user_id(session['user_id'])
            return redirect('/dashboard')
        except:
            print("User has not entered income.")
            return redirect('/income')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
def go_home():
    return redirect('/dashboard')

@app.route('/income')
def income_form():
    try:
        Income.display_income_by_user_id(session['user_id'])
        return redirect('/dashboard')
    except:
        return render_template('income.html')

@app.route('/learn')
def info_page():
    return render_template('learn.html')