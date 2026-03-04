from flask import request, make_response
import mysql.connector
import re # Regular expressions also called Regex
from functools import wraps

##############################
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "2026_1_game"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)

####################################
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view

#####################################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
REGEX_USER_FIRST_NAME = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if not re.match(REGEX_USER_FIRST_NAME,user_first_name):
        raise Exception("company_exception")
    return user_first_name
