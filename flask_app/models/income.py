from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Income:
    db = 'budget_app'
    def __init__(self, data):
        self.id = data['id']
        self.occupation = data['occupation']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_income(cls, data):
        if not cls.validate_income(data):
            return False
        else:
            query = """
                    INSERT INTO income(occupation, amount, user_id)
                    VALUES (%(occupation)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True

    @classmethod
    def calculate_weekly(cls, data):
        data = data.copy()
        # data['amount'] = int(data['amount']) * 4
        data['amount'] = int(data['amount'])
        data['amount'] *= 4
        print(data['amount'])
        if not cls.validate_income(data):
            return False
        else:
            query = """
                    INSERT INTO income(occupation, amount, user_id)
                    VALUES (%(occupation)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True

    @classmethod
    def calculate_biweekly(cls, data):
        data = data.copy()
        data['amount'] = int(data['amount']) * 2
        print(data['amount'])
        if not cls.validate_income(data):
            return False
        else:
            query = """
                    INSERT INTO income(occupation, amount, user_id)
                    VALUES (%(occupation)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True

    @classmethod
    def calculate_commission(cls, data):
        data = data.copy()
        data['amount'] = int(data['amount']) / 12
        print(data['amount'])
        if not cls.validate_income(data):
            return False
        else:
            query = """
                    INSERT INTO income(occupation, amount, user_id)
                    VALUES (%(occupation)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True

    @classmethod
    def display_income_by_user_id(cls, id):
        data = {'id':id}
        query = """
                SELECT * 
                FROM income
                WHERE income.user_id = %(id)s
                """
        result =  connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @staticmethod
    def validate_income(data):
        is_valid = True
        if len(data['occupation']) <= 2:
            flash('Your occupation must be at least 2 characters')
            is_valid = False
        if int(data['amount']) <= 0:
            flash('You must have an amount greater than 0')
            is_valid = False
        return is_valid
