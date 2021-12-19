from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        errors = 0
        if not EMAIL_REGEX.match(user['email']) or user['email'] == '' or User.email_check(user['email']): #or exists in database
            flash(u"Invalid Email", "registration")
            errors += 1
        if user['first_name'] == '' or not str.isalpha(user['first_name'])  or not len(user['first_name'])> 2:
            flash(u"Invalid First Name", "registration")
            errors += 1
        if user['last_name'] == '' or not str.isalpha(user['last_name']) or not len(user['last_name'])> 2:
            flash(u"Invalid Last Name", "registration")
            errors += 1
        if user['password'] == '' or not len(user['password']) > 7:
            flash(u"Invalid Password", "registration")
            errors += 1
        if not user['password'] == user['pwconfirm']:
            flash(u"Passwords must match.", "registration")
            errors+= 1
        if errors > 0:
            is_valid = False
        return is_valid

    @staticmethod
    def email_check(email):
        query = "SELECT email from USERS"
        results = connectToMySQL('login_reg').query_db(query)
        print(results)
        for emails in results:
            return email == emails['email']
    
    @staticmethod
    def login_validator(data):
        query = "SELECT email, password FROM  users"
        results = connectToMySQL('login_reg').query_db(query)
        for users in results:
            if data['email'] == users['email']:
                return True
        return False

    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('login_reg').query_db(query, data)

    @classmethod
    def one_user(cls, data):
        query = " SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('login_reg').query_db(query,data)
        return cls(results[0])

    @classmethod
    def user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('login_reg').query_db(query,data)
        return cls(results[0])