from flask import *
from sqlalchemy import func, update
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "vwnWWDM+igMGbmvsOw=="

# TODO: Fill in methods and routes  

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        users = db_session.query(User).all()
        for user in users:
            if user.username == username and user.password == password:
                session["username"] = username
                session["is_admin"] = False
                if user.is_admin:
                    session["is_admin"] = True
                    return redirect(url_for("admin_lunch"))
                return redirect(url_for("review"))
            
        flash("Incorrect Username/Password", "error")
        return render_template("login.html")
        
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        re_password = request.form["re-password"]
        admin_code = request.form["admin_code"]

        if password != re_password:
            flash("Your passwords don't match!", "error")
            return render_template("signup.html")
        elif username == "" or password == "":
            flash("You must enter a username and password!", "error")
            return render_template("signup.html")
        elif admin_code == 'code':
            db_session.add(User(username=username, password=password, has_rated=False, is_admin=True))
        else:
            db_session.add(User(username=username, password=password, has_rated=False, is_admin=False))
        
        db_session.commit()
        return redirect(url_for("login"))

@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        if "username" in session:
            user = db_session.query(User).where(User.username == session["username"]).first()
            lunch = db_session.query(Lunch).where(Lunch.is_today).first()
            try:
                past_review = db_session.query(Review).where(Review.user_id == user.id).where(Review.lunch_id == lunch.id).first()
                return render_template("review.html", lunch=lunch.title, has_rated=user.has_rated, avg_rating=lunch.avg_rating, past_rating=past_review.rating)
            except: 
                if lunch:
                    return render_template("review.html", lunch=lunch.title)
                return render_template("review.html", lunch="No lunch yet!")
        return redirect(url_for("login"))
    elif request.method == "POST":
        user = db_session.query(User).where(User.username == session["username"]).first()
        lunch = db_session.query(Lunch).where(Lunch.is_today).first()
        rating = request.form["rating"]
        feedback = request.form["feedback"]
        if lunch and user.has_rated == False:
            new_review = Review(user_id=user.id, lunch_id=lunch.id, rating=rating, feedback=feedback)
            db_session.add(new_review)
            user.has_rated = True
            db_session.flush()
            avg_rating = db_session.query(func.avg(Review.rating)).where(Review.lunch_id == lunch.id).scalar()
            lunch.avg_rating = avg_rating
            db_session.commit()

            return render_template("review.html", lunch=lunch.title, has_rated=user.has_rated, avg_rating=lunch.avg_rating, past_rating=new_review.rating)
        return render_template("review.html", lunch="No lunch yet!")

        
    
@app.route("/request", methods=["GET", "POST"])
def requests():
    if request.method == "GET":
        if "username" in session:
            return render_template("request.html")
        return redirect(url_for("login"))
    elif request.method == "POST":
        title = request.form["request-title"]
        description = request.form["request-description"]
        user = db_session.query(User).where(User.username == session["username"]).first()
        db_session.add(Request(user_id=user.id, title=title, description=description))
        db_session.commit()
    return render_template("request.html")

@app.route("/lunch", methods=["GET", "POST"])
def admin_lunch():
    if request.method == "GET":
        if "username" in session and session["is_admin"]:
            return render_template("admin_lunch.html")
        return redirect(url_for("login"))
    elif request.method == "POST":
        lunch_title = request.form["lunch"]
        if lunch_title != "":
            lunches = db_session.query(Lunch)
            for lunch in lunches:
                lunch.is_today = False

            existing_lunches = db_session.query(Lunch)
            lunch_exists = False
            for lunch in existing_lunches:
                if lunch.title == lunch_title:
                    lunch_exists = True
                    existing_lunch = lunch
            if lunch_exists:
                existing_lunch.is_today = True
            else:
                db_session.add(Lunch(title=lunch_title, is_today=True))
                
            users = db_session.query(User)
            for user in users:
                user.has_rated = False
            db_session.commit()
        return render_template("admin_lunch.html")

@app.route("/feedback", methods=["GET", "POST"])
def admin_feedback():
    if request.method == "GET":
        if "username" in session and session["is_admin"]:
            try:
                lunch = db_session.query(Lunch).where(Lunch.is_today).first()
                reviews = db_session.query(Review).where(Review.lunch_id == lunch.id).all()
                requests = db_session.query(Request).all()
                lunches = db_session.query(Lunch).all()
                return render_template("admin_feedback.html", reviews=reviews, requests=requests, lunches=lunches)
            except: 
                return render_template("admin_feedback.html")
            
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")

    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
