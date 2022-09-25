from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



# model the class after the user table from our database
class Show:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM tv_shows;"
        result = connectToMySQL('tv_shows').query_db(query)
        return result

    @classmethod
    def get_one_show(cls, data):
        query = "SELECT * FROM tv_shows where id = %(id)s;"
        result = connectToMySQL('tv_shows').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_creation(show):
        is_valid = True
        query = "SELECT * FROM tv_shows WHERE title = %(title)s;"
        results = connectToMySQL('tv_shows').query_db(query, show)
        if len(results) >= 1:
            flash("Title already taken")
            is_valid = False
        if len(show['title']) < 3:
            flash("First Name must be at least 3 characters")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid = False
        if len(show['release_date']) < 3:
            flash("Release Date must not be blank")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit(show):
        is_valid = True
        query = "SELECT * FROM tv_shows WHERE title = %(title)s;"
        results = connectToMySQL('tv_shows').query_db(query, show)
        if len(show['title']) < 3:
            flash("First Name must be at least 3 characters")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters", "register")
            is_valid = False
        return is_valid

    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO tv_shows (title,network,release_date,description, user_id) VALUES(%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s)"
        return connectToMySQL('tv_shows').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE tv_shows SET title = %(title)s , network= %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW() where id=%(id)s;"
        return connectToMySQL('tv_shows').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tv_shows WHERE id=%(id)s;"
        return connectToMySQL('tv_shows').query_db(query, data)