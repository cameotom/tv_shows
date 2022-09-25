from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('tv_shows').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['password2']:
            flash("Passwords don't match", "register")
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('tv_shows').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        print(data)
        query = "SELECT * FROM users where email = %(email)s;"
        result = connectToMySQL('tv_shows').query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        print(data)
        query = "SELECT * FROM users where id = %(id)s;"
        result = connectToMySQL('tv_shows').query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL('tv_shows').query_db(query)
        return result

