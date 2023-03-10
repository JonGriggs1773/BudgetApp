from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Expense:
    db = 'budget_app'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_expense(cls, data):
        if not Expense.expense_validations(data):
            print('Expense validations were not met')
            return False
        else:
            query = """
                    INSERT INTO expenses (name, amount, user_id)
                    VALUES (%(name)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def get_expense_by_id(cls, id):
        data = {"id": id}
        query = """
                SELECT *
                FROM expenses
                WHERE id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        one_expense = cls(result[0])
        return one_expense
    
    @classmethod
    def edit_expense(cls, data):
        query = """
                UPDATE expenses
                SET name = %(name)s, amount = %(amount)s
                WHERE id = %(id)s
                """
        print(data, '-----------------------------------------------')
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_expense_by_id(cls, id):
        data = {"id": id}
        query = """
                DELETE
                FROM expenses
                WHERE id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_expense_total(cls, id):
        data = {'id': id}
        query = """
                SELECT *
                FROM expenses
                WHERE user_id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        expense_total = 0
        for i in range(len(result)):
            one_expense = cls(result[i])
            try:    
                expense_total += one_expense.amount
            except:
                print('-----There are no values in bills for this user.-----')
        return expense_total


    @staticmethod
    def expense_validations(data):
        is_valid = True
        if len(data['name']) < 2:
            flash('Your bills name must be at least 2 characters')
            is_valid = False
        if data['amount'] == '':
            flash('Amount must be greater than 0')
            is_valid = False
        else:
            if int(data['amount']) <= 0:
                flash('Amount must be greater than 0')
                is_valid = False
        return is_valid




