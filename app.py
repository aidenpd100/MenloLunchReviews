from flask import *
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
                return redirect(url_for("review"))
            
        flash("Incorrect Username/Password", "error")
        return render_template("login.html")
        


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        if "username" in session:
            return render_template("review.html")
        else:
            return redirect(url_for("login"))
    
@app.route("/request", methods=["GET", "POST"])
def requests():
    if request.method == "GET":
        return render_template("request.html")
    
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
            flash("Passwords Don't Match", "error")
            return render_template("signup.html")
        elif admin_code == 'code':
            db_session.add(User(username=username, password=password, is_admin=True))
        else:
            db_session.add(User(username=username, password=password, is_admin=False))
        
        db_session.commit()
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
