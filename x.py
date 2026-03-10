
from flask import request, make_response, app    # type: ignore

import mysql.connector                      # type: ignore
import re # Regular expressions also called Regex
import time
from datetime import datetime, timedelta
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
        raise Exception("company_exception in user_first_name")
    return user_first_name

#####################################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_USER_LAST_NAME = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(REGEX_USER_LAST_NAME,user_last_name):
        raise Exception("company_exception in user_last_name")
    return user_last_name


############################## Copied from Teams BackEnd
REGEX_USER_EMAIL = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_USER_EMAIL, user_email):
        raise Exception("company_exception user_email")
    return user_email

##############################
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD,user_password):
        raise Exception("company_exception in user_password")
    return user_password

##############################

#           Travels          #

##############################

TRAVEL_TITLE_MIN = 2
TRAVEL_TITLE_MAX = 100
REGEX_TRAVEL_TITLE = f"^.{{{TRAVEL_TITLE_MIN},{TRAVEL_TITLE_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_travel_title():

    travel_title = request.form.get("travel_title", "").strip()
    if not re.match(REGEX_TRAVEL_TITLE,travel_title):
        raise Exception("company_exception in travel_title")
    return travel_title


#################################################################################

REGEX_DATE = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"

def validate_travel_date_from():
    # from app import app                                                # Reformat the datetime into another string format
    TRAVEL_DATE_FROM_MIN = int(time.time()) #Makes Epoch time
    TRAVEL_DATE_FROM_MAX = int((datetime.now() + timedelta(days=90)).replace(hour=23, minute=59, second=59, microsecond=0).timestamp())

    travel_date_from = request.form.get("travel_date_from", "")        # Get form input data
    dt = datetime.strptime(travel_date_from, "%Y-%m-%dT%H:%M")         # Convert the string into a datetime object, should have with hours and min.
    travel_date_from_epoch = int(dt.timestamp())   
    
    # app.logger.info('TRAVEL_DATE_FROM_MIN:%s, travel_date_from:%d,travel_date_from_epoch:%s , TRAVEL_DATE_FROM_MAX:%s ', TRAVEL_DATE_FROM_MIN, travel_date_from,travel_date_from_epoch, TRAVEL_DATE_FROM_MAX)

    if not re.match(REGEX_DATE,travel_date_from):
            raise Exception("company_exception in travel_date_from")
    if travel_date_from_epoch < TRAVEL_DATE_FROM_MIN:
        raise Exception("company_exception in travel_date_from")

    if travel_date_from_epoch > TRAVEL_DATE_FROM_MAX:
        raise Exception("company_exception in travel_date_from")
    
    return travel_date_from_epoch


#################################################################################

def validate_travel_date_to():
    from app import app  
    
    TRAVEL_DATE_TO_MIN = int(time.time()) 
    TRAVEL_DATE_TO_MAX = int((datetime.now() + timedelta(days=90)).replace(hour=23, minute=59, second=59, microsecond=0).timestamp())
    travel_date_to = request.form.get("travel_date_to", "")
    dt = datetime.strptime(travel_date_to, "%Y-%m-%dT%H:%M")
    travel_date_to_epoch = int(dt.timestamp())   

    app.logger.info('TRAVEL_DATE_TO_MIN:%s, travel_date_to:%d,travel_date_to_epoch:%s , TRAVEL_DATE_TO_MAX:%s ', TRAVEL_DATE_TO_MIN, travel_date_to,travel_date_to_epoch, TRAVEL_DATE_TO_MAX)
    
    if not re.match(REGEX_DATE,travel_date_to):
            raise Exception("company_exception in travel_date_to")
    if travel_date_to_epoch < TRAVEL_DATE_TO_MIN:
        raise Exception("company_exception in travel_date_to")

    if travel_date_to_epoch > TRAVEL_DATE_TO_MAX:
        raise Exception("company_exception in travel_date_to")
    
    return travel_date_to_epoch

##############################################################################################

TRAVEL_DESCRIPTTION_MIN = 2
TRAVEL_DESCRIPTTION_MAX = 500
REGEX_TRAVEL_DESCRIPTTION = f"^.{{{TRAVEL_DESCRIPTTION_MIN},{TRAVEL_DESCRIPTTION_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_travel_description():
    travel_description = request.form.get("travel_description", "").strip()
    if not re.match(REGEX_TRAVEL_DESCRIPTTION,travel_description):
        raise Exception("company_exception in travel_description")
    return travel_description

##############################################################################################

TRAVEL_LOCATION_MIN = 2
TRAVEL_LOCATION_MAX = 100
REGEX_TRAVEL_LOCATION = f"^.{{{TRAVEL_LOCATION_MIN},{TRAVEL_LOCATION_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_travel_location():
    travel_location = request.form.get("travel_location", "").strip()
    if not re.match(REGEX_TRAVEL_LOCATION,travel_location):
        raise Exception("company_exception in travel_location")
    return travel_location

##############################################################################################

TRAVEL_COUNTRY_MIN = 2
TRAVEL_COUNTRY_MAX = 100
REGEX_TRAVEL_COUNTRY = f"^.{{{TRAVEL_COUNTRY_MIN},{TRAVEL_COUNTRY_MAX}}}$" # the . is you can put whatever, so it can be letters, numbers so on.

def validate_travel_country():
    travel_country = request.form.get("travel_country", "").strip()
    if not re.match(REGEX_TRAVEL_COUNTRY,travel_country):
        raise Exception("company_exception in travel_country")
    return travel_country