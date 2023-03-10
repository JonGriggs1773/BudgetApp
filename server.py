from flask_app import app
from flask_app.controllers import users, incomes, bills, expenses, savings
if __name__ == "__main__":
    app.run(debug = True)