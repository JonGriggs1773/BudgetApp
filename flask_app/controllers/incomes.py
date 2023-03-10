from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.income import Income

@app.route('/monthly')
def income_form_page():
    try:
        Income.display_income_by_user_id(session['user_id'])
        return redirect('/dashboard')
    except:
        return render_template('monthly.html', user_id = session['user_id'])

@app.route('/create/income', methods = ["POST"])
def submit_income():
        if Income.create_income(request.form):
            return redirect('/dashboard')
        else:
            return redirect('/monthly')

@app.route('/calculate')
def calculation_help_page():
    try:
        Income.display_income_by_user_id(session['user_id'])
        return redirect('/dashboard')
    except:
        return render_template('calculate.html', user_id = session['user_id'])

@app.route('/create/income/weekly', methods = ['POST'])
def weekly_calculation():
    if Income.calculate_weekly(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/calculate')

@app.route('/create/income/biweekly', methods = ['POST'])
def biweekly_calculation():
    if Income.calculate_biweekly(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/calculate')

@app.route('/create/income/commission', methods = ['POST'])
def commission_calculation():
    if Income.calculate_commission(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/calculate')
