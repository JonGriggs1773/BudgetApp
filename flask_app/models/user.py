from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
from flask_app.models import income
from flask_app.models import expense
from flask_app.models import bill
from flask_app.models import saving


class User:
    db = 'budget_app'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.income = []
        self.expenses = []
        self.savings = []
        self.bills = []

#? Assigning user in database and putting user id and full name in session
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        data = cls.parse_user_data(data)
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        user_id = connectToMySQL(cls.db).query_db(query, data)
        session['user_id'] = user_id
        session['user_name'] = f"{data['first_name']} {data['last_name']}"
        return True

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email':email}
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {"id": id}
        query = """
                SELECT *
                FROM users
                WHERE id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        one_user = cls(result[0])
        return one_user

    @classmethod
    def get_all_bills_from_one_user_by_user_id(cls, id):
        data = {'id':id}
        query = """
                SELECT *
                FROM users
                LEFT JOIN bills
                ON users.id = bills.user_id
                WHERE users.id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        one_user = cls(result[0])
        for row_in_db in result:
            bill_data = {
                'id': row_in_db['bills.id'],
                'name': row_in_db['name'],
                'amount': row_in_db['amount'],
                'created_at': row_in_db['created_at'],
                'updated_at': row_in_db['updated_at'],
            }
            one_user.bills.append(bill.Bill(bill_data))
        return one_user

    @classmethod
    def get_all_expenses_from_one_user_by_user_id(cls, id):
        data = {'id':id}
        query = """
                SELECT *
                FROM users
                LEFT JOIN expenses
                ON users.id = expenses.user_id
                WHERE users.id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        one_user = cls(result[0])
        for row_in_db in result:
            expense_data = {
                'id': row_in_db['expenses.id'],
                'name': row_in_db['name'],
                'amount': row_in_db['amount'],
                'created_at': row_in_db['created_at'],
                'updated_at': row_in_db['updated_at'],
            }
            one_user.expenses.append(expense.Expense(expense_data))
        return one_user

    @classmethod
    def get_all_savings_from_one_user_by_user_id(cls, id):
        data = {'id':id}
        query = """
                SELECT *
                FROM users
                LEFT JOIN savings
                ON users.id = savings.user_id
                WHERE users.id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        one_user = cls(result[0])
        for row_in_db in result:
            savings_data = {
                'id': row_in_db['savings.id'],
                'name': row_in_db['name'],
                'amount': row_in_db['amount'],
                'created_at': row_in_db['created_at'],
                'updated_at': row_in_db['updated_at'],
            }
            one_user.savings.append(expense.Expense(savings_data))
        return one_user



#? Validations and password hashing for user
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must have at least 2 characters', 'error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must have at least 2 characters', 'error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email must be in proper format', 'error')
            is_valid = False
        if User.get_user_by_email(data['email'].lower().strip()):
            flash('Email is already in our system, please try again', 'error')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Password and confirm password does not match', 'error')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False
        return is_valid


    @staticmethod
    def parse_user_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'].lower())
        return parsed_data

    @staticmethod
    def login_user(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            print('Got this user')
            if bcrypt.check_password_hash(this_user.password, data['password'].lower()):
                session['user_id'] = this_user.id
                session['user_name'] = f"{this_user.first_name} {this_user.last_name}"
                return True
        else:
            flash('Your login failed.', 'login')
            return False