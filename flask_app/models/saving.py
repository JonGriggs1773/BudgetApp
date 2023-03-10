from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Saving:
    db = 'budget_app'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_savings(cls, data):
        if not Saving.savings_validations(data):
            print('Savings validations were not met')
            return False
        else:
            query = """
                    INSERT INTO savings (name, amount, user_id)
                    VALUES (%(name)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def get_savings_by_id(cls, id):
        data = {"id": id}
        query = """
                SELECT *
                FROM savings
                WHERE id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        one_saving = cls(result[0])
        return one_saving

    @classmethod
    def edit_savings(cls, data):
        query = """
                UPDATE savings
                SET name = %(name)s, amount = %(amount)s
                WHERE id = %(id)s
                """
        print('-----------------------------------------------')
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_savings_by_id(cls, id):
        data = {"id": id}
        query = """
                DELETE
                FROM savings
                WHERE id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_savings_total(cls, id):
        data = {'id': id}
        query = """
                SELECT *
                FROM savings
                WHERE user_id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        savings_total = 0
        for i in range(len(result)):
            one_saving = cls(result[i])
            try:    
                savings_total += one_saving.amount
            except:
                print('-----There are no values in bills for this user.-----')
        return savings_total


    @staticmethod
    def savings_validations(data):
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