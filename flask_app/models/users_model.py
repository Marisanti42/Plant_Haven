from flask_app.config.mysqlconnnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "plant_haven"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.plants = []

#CREATE
    @classmethod
    def save_user(cls, data):
        query="""INSERT INTO users(first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query,data)
    
#READ
    @classmethod
    def get_user_by_email(cls,email):
        data = {"email":email}
        query="SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return []
        return cls(results[0])

#validate registering user's information
    @staticmethod
    def validate_user(user):
        print(user)
        is_valid = True         #valid is true by default
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 2:
            flash("Email must be entered.")
            is_valid = False
        elif User.get_user_by_email(user['email']):
            flash("Email is already in use.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Email address is invalid.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must contain at least 8 characters.")
            is_valid = False
        return is_valid
    
#validate user's login information
    @staticmethod
    def validate_login(user):
        print(user)
        is_valid = True         #valid is true by default
        if len(user['email']) < 2:
            flash("Email must be entered.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Email address is invalid.")
            is_valid = False
        if len(user['password']) < 10:
            flash("Password must contain at least 10 characters.")
            is_valid = False
        return is_valid

