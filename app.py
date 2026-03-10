from flask import Flask, render_template, request, jsonify, session, redirect    # type: ignore
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash # type: ignore
from werkzeug.security import check_password_hash    # type: ignore

from icecream import ic                              # type: ignore
ic.configureOutput(prefix=f'~~~~~~~~~~~~~~~~~~~~~~~~ | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

################################################################################################

#                                        Routes                                                #

################################################################################################
@app.get("/")
@x.no_cache
def show_index():
    from app import app 
    try:
        user = session.get("user","")

        db, cursor = x.db()
        q = "SELECT * FROM travels"

        cursor.execute(q)
        travels = cursor.fetchall()
        app.logger.info('travels:%s',travels)
        return render_template("page_index.html",user=user, x=x, travels=travels)
    
    except Exception as ex:
        ic(ex)
        return ("ups ...")
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

################################################################################################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user","")
        if not user: 
            return render_template("page_signup.html", user=user, x=x)
        return redirect("/profile")
    except Exception as ex:
        ic(ex)
        return ("ups ...")
################################################################################################

@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: 
            return render_template("page_login.html", user=user, x=x)
        return redirect("/profile")
    
    except Exception as ex:
        ic(ex)
        return "ups"
################################################################################################

@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user","")
        if not user : return redirect("/login")
        return render_template("page_profile.html", user = user, x=x)
    except Exception as ex:
        ic(ex)
        return ("ups ...")

################################################################################################

@app.get("/logout")
def show_logout():
    try:
       session.clear()
       return redirect("/login")
    except Exception as ex:
        ic(ex)
        return ("ups ...")
    
################################################################################################

@app.get("/createtravel")
def show_createtravel():
    try:
        return render_template("page_createtravel.html", x=x)
    except Exception as ex:
        ic(ex)
        return ("ups ...")
    
################################################################################################

@app.get("/updatetravel")
def show_updatetravel():
    try:
        return render_template("page_updatetravel.html", x=x)
    except Exception as ex:
        ic(ex)
        return ("ups ...")


################################################################################################

#                                        USER                                                  #

################################################################################################

@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_hashed_password = generate_password_hash(user_password)
        # ic(user_hashed_password) # 'scrypt:32768:8:1$V0NLEqHQsgKyjyA7$3a9f6420e4e9fa7a4e4ce6c89927e7dcb532e5f557aee6309277243e5882cc4518c94bfd629b61672553362615cd5d668f62eedfe4905620a8c9bb7db573de31'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
            <browser mix-replace="#form_signup">{form_signup}</browser>
            <browser mix-redirect="/login"></browser>
        """
    
    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exists"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500
    
    finally:
        if "cursor" in locals(): cursor.close() #is "cursor" in the local function then close.
        if "db" in locals(): db.close()
    
################################################################################################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db,cursor =x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q,(user_email,))
        user = cursor.fetchone()
        if not user:
            error_message = "Invalid credentials"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        user.pop("user_password")
        session["user"] = user
        ic(user)

        return """<browser mix-redirect="/profile"></browser>"""
    
    except Exception as ex:
        ic(ex)
        
        if "company_exception in user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception in user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        #Worst case scenarios # allways have a worst case
        error_message = "system under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500
    
    finally:
        if "cursor" in locals(): cursor.close() #is "cursor" in the local function then close.
        if "db" in locals(): db.close()


################################################################################################

#                                   Travel Destinations                                        #

################################################################################################
@app.post("/api-create-travel")
def api_create_travel():
    try:
        travel_title = x.validate_travel_title()
        travel_date_from = x.validate_travel_date_from()
        travel_date_to = x.validate_travel_date_to()
        travel_description = x.validate_travel_description()
        travel_location = x.validate_travel_location()
        travel_country = x.validate_travel_country()

        travel_pk = uuid.uuid4().hex
        travel_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO travels VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (travel_pk, travel_title, travel_date_from, travel_date_to, travel_description, travel_location,travel_country,travel_created_at))
        db.commit()

        form_create_travel = render_template("___form_createtravel.html", x=x)
        
        return f"""
            <browser mix-replace="#form_create_travel">{form_create_travel}</browser>
        """
    
    except Exception as ex:
        ic(ex)
        if "company_exception travel_title" in str(ex):
            error_message = f"travel title {x.TRAVEL_TITLE_MIN} to {x.TRAVEL_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception travel_date_from" in str(ex):
            error_message = f"travel date from {x.TRAVEL_DATE_FROM_MIN} to {x.TRAVEL_DATE_FROM_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception travel_date_to" in str(ex):
            error_message = f"travel date to {x.TRAVEL_DATE_TO_MIN} to {x.TRAVEL_DATE_TO_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception travel_description" in str(ex):
            error_message = f"travel description {x.TRAVEL_DESCRIPTTION_MIN} to {x.TRAVEL_DESCRIPTTION_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception travel_location" in str(ex):
            error_message = f"travel location {x.TRAVEL_LOCATION_MIN} to {x.TRAVEL_LOCATION_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-before-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500
    
    finally:
        if "cursor" in locals(): cursor.close() #is "cursor" in the local function then close.
        if "db" in locals(): db.close()


################################################################################################