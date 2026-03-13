from flask import Flask, render_template, request, jsonify, session, redirect    # type: ignore
import x
import uuid
import time, datetime
from datetime import datetime
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
    try:
        user = session.get("user","")
        return render_template("page_index.html",user=user)
    
    except Exception as ex:
        ic(ex)
        return ("ups ...")

################################################################################################
@app.get("/travellist")
@x.no_cache
def show_travellist():
    try:
        user = session.get("user","")
        db, cursor = x.db()
        q = "SELECT * FROM travels"

        cursor.execute(q)
        all_travels = cursor.fetchall()

        for travel in all_travels:
            travel["travel_date_from"] = datetime.fromtimestamp(
                travel["travel_date_from"]
            ).strftime("%Y-%m-%d %H:%M")

            travel["travel_date_to"] = datetime.fromtimestamp(
                travel["travel_date_to"]
            ).strftime("%Y-%m-%d %H:%M")

        if not user: return redirect("/login")
        return render_template("page_travellist.html",user=user, x=x, travels=all_travels)
    
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
@x.no_cache
def show_logout():
    try:
       session.clear()
       return redirect("/login")
    except Exception as ex:
        ic(ex)
        return ("ups ...")
    
################################################################################################

@app.get("/createtravel")
@x.no_cache
def show_createtravel():
    try:
        user = session.get("user","")
        if not user: return redirect("/login")
        return render_template("page_createtravel.html",user=user, x=x)
    except Exception as ex:
        ic(ex)
        return ("ups ...")
    
################################################################################################

@app.get("/updatetravel/<travel_pk>")
@x.no_cache
def show_updatetravel_by_travel_pk(travel_pk):
    try:
        user = session.get("user","")
        db, cursor = x.db()
        q = "SELECT * FROM travels WHERE travel_pk = %s"
        cursor.execute(q, (travel_pk,))
        onetravel = cursor.fetchone()

        onetravel["travel_date_from"] = datetime.fromtimestamp(onetravel["travel_date_from"]).strftime("%Y-%m-%dT%H:%M")
        onetravel["travel_date_to"] = datetime.fromtimestamp(onetravel["travel_date_to"]).strftime("%Y-%m-%dT%H:%M")

        updatetravel_html = render_template("page_updatetravel.html",user=user, x=x, travel=onetravel)
        
        if not user: return redirect("/login")
        return updatetravel_html
    
    except Exception as ex:
        ic(ex, flush=True)
        return "ups ...", 500
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


################################################################################################

#                                        USER                                                  #

################################################################################################

@app.post("/api-create-user")
@x.no_cache
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_hashed_password = generate_password_hash(user_password)

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
@x.no_cache
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
@x.no_cache
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
        travel_updated_at = int(time.time())

        db, cursor = x.db()

        q = "INSERT INTO travels VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(q, (travel_pk, travel_title, travel_date_from, travel_date_to, travel_description, travel_location,travel_country,travel_created_at,travel_updated_at ))
        db.commit()

        form_create_travel = render_template("___form_createtravel.html", x=x)
        
        return f"""
            <browser mix-replace="#form_create_travel">{form_create_travel}</browser>
        """, 200
    
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
            error_message = f"travel date to {TRAVEL_DATE_TO_MIN} to {TRAVEL_DATE_TO_MAX} characters"
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
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
###############################################################################################

@app.patch("/api-update-travel/<travel_pk>")
@x.no_cache
def api_update_travels(travel_pk): 
    try:
        travel_title = x.validate_travel_title()
        travel_date_from = x.validate_travel_date_from()
        travel_date_to = x.validate_travel_date_to()
        travel_description = x.validate_travel_description()
        travel_location = x.validate_travel_location()
        travel_country = x.validate_travel_country()

        parts = []
        values = []

        travel_updated_at = int(time.time())
        parts.append("travel_updated_at = %s")
        values.append(travel_updated_at)

        travel_title = travel_title.strip()
        if travel_title:
            parts.append("travel_title = %s")
            values.append(travel_title)

        travel_date_from = travel_date_from
        if travel_date_from:
            parts.append("travel_date_from = %s")
            values.append(travel_date_from)
        
        travel_date_to = travel_date_to
        if travel_date_to:
            parts.append("travel_date_to = %s")
            values.append(travel_date_to)

        travel_description = travel_description.strip()
        if travel_description:
            parts.append("travel_description = %s")
            values.append(travel_description)

        travel_location = travel_location.strip()
        if travel_location:
            parts.append("travel_location = %s")
            values.append(travel_location)

        travel_country = travel_country.strip()
        if travel_country:
            parts.append("travel_country = %s")
            values.append(travel_country)

        if not travel_title and not travel_date_from and not travel_date_to and not travel_description and not travel_location and not travel_country: return "nothing to update", 400
        partial_query = ", ".join(parts)

        values.append(travel_pk)

        q = f"""
            UPDATE travels
            SET	{partial_query}
            WHERE travel_pk = %s
        """
        
        db, cursor = x.db()
        cursor.execute(q, values)
        db.commit()

        return """<browser mix-replace="">
                    <div>
                        <label> Title <span> {{x.TRAVEL_TITLE_MIN}} to {{x.TRAVEL_TITLE_MAX}} characters</span> </label>
                        <input  type="text" aria-label="travel title" placeholder="{{travel.travel_title}}" id="travel_title" name="travel_title"  mix-validate="{{x.REGEX_TRAVEL_TITLE}}" >
                    </div>
                    <div>
                        <label> Date from<span> {{x.REGEX_TRAVEL_DATE_FROM}}</span> </label>
                        <input   type="datetime-local" aria-label="travel date from"  id="travel_date_from"  name="travel_date_from" mix-validate="{{x.REGEX_TRAVEL_DATE_FROM}}">
                    </div>
                    <div>
                        <label> Date to <span> {{x.REGEX_TRAVEL_DATE_TO}}</span> </label>
                        <input   type="datetime-local" aria-label="travel date to"   id="travel_date_to"     name="travel_date_to"      mix-validate="{{x.REGEX_TRAVEL_DATE_TO}}">
                    </div>
                    <div>
                        <label> Description <span>{{x.TRAVEL_DESCRIPTTION_MIN}} to {{x.TRAVEL_DESCRIPTTION_MAX}} characters</span> </label>
                        <input   type="text" aria-label="travel description"  placeholder="{{travel.travel_description}}"  id="travel_description"   name="travel_description" mix-validate="{{x.REGEX_TRAVEL_DESCRIPTTION}}">
                    </div>
                    <div>
                        <label> Location <span> {{x.TRAVEL_LOCATION_MIN}} to {{x.TRAVEL_LOCATION_MAX}} characters</span> </label>
                        <input   type="text" aria-label="travel location"  placeholder="{{travel.travel_location}}"  id="travel_location"   name="travel_location"    mix-validate="{{x.REGEX_TRAVEL_LOCATION}}">
                    </div>
                    <div>
                        <label> Country <span> {{x.TRAVEL_COUNTRY_MIN}} to {{x.TRAVEL_COUNTRY_MAX}} characters</span> </label>
                        <input   type="text" aria-label="travel country"  placeholder="{{travel.travel_country}}"  id="travel_country"   name="travel_country"    mix-validate="{{x.REGEX_TRAVEL_COUNTRY}}">
                    </div>
            </browser> """, 200

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
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

###############################################################################################

@app.delete("/travels/<travel_pk>")
@x.no_cache
def delete_travel(travel_pk):
    try:
        # TODO: validate user_pk
        db, cursor = x.db()

        q = "DELETE FROM travels WHERE travel_pk = %s"
        cursor.execute(q, (travel_pk,))
        db.commit()
        return f"""
            <browser mix-remove="#travel-{travel_pk}" mix-fade-1500>
            </browser>
        """ , 204

    except Exception as ex:
        ic(ex)

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()