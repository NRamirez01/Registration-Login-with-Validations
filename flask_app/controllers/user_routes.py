from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask import render_template,redirect,request,session
from flask_app.models.user import User
bcrypt = Bcrypt(app)

@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/home')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['user_id'] = User.register_user(data)
    return redirect('/splash')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form['email'],
        "password": request.form['password']
    }
    if not User.login_validator(data):
        flash(u"Invalid Email/Password", "login")
        return redirect('/home')
    else: 
        user = User.user_by_email(data)
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash(u"Invalid Email/Password", "login")
            return redirect('/home')
        else: 
            session['user_id'] = user.id
            return redirect('/splash')

@app.route('/splash')
def home_screen():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        return render_template("splash.html", user = User.one_user(data))
    else: 
        flash(u"Invalid Username/Password", "login")
        return redirect('/home')

@app.route('/logout', methods=['POST'])
def log_out():
    session.clear()
    return redirect('/home')


if __name__=="__main__":
    app.run(debug=True)

