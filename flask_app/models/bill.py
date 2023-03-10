from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Bill:
    db = 'budget_app'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_bill(cls, data):
        if not cls.bill_validations(data):
            print('Bill validations were not met')
            return False
        else:
            query = """
                    INSERT INTO bills (name, amount, user_id)
                    VALUES (%(name)s, %(amount)s, %(user_id)s)
                    """
            result = connectToMySQL(cls.db).query_db(query, data)
        return True

    @classmethod
    def get_bill_by_id(cls, id):
        data = {"id": id}
        query = """
                SELECT *
                FROM bills
                WHERE id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        one_bill = cls(result[0])
        return one_bill
    
    @classmethod
    def edit_bill(cls, data):
        query = """
                UPDATE bills
                SET name = %(name)s, amount = %(amount)s
                WHERE id = %(id)s
                """
        print(data, '-----------------------------------------------')
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_bill_by_id(cls, id):
        data = {"id": id}
        query = """
                DELETE
                FROM bills
                WHERE id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    #? Argument will pass in user id in session
    @classmethod
    def get_all_bill_total(cls, id):
        data = {'id': id}
        query = """
                SELECT *
                FROM bills
                WHERE user_id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        bill_total = 0
        for i in range(len(result)):
            one_bill = cls(result[i])
            try:    
                bill_total += one_bill.amount
            except:
                print('-----There are no values in bills for this user.-----')
        return bill_total

    @staticmethod
    def bill_validations(data):
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