from application import app
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.forms import LoginForm, RegisterForm
from application.temp_login import User

users = User()
@app.route("/")
@app.route("/home")
def home():
    if session.get('username'):
       return redirect(url_for('group'))
    return render_template("home.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if session.get('username'):
        return redirect(url_for('group'))
    form = LoginForm()
    if form.validate_on_submit():
        email      = form.email.data
        password    = form.password.data
        if users.check(email, password):
            flash("You are successfully Logged In!","success")
            session['username'] = email
            return redirect(url_for('login'))
        flash("Incorrect Username or Password", "error")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if session.get('username'):
        return redirect(url_for('group'))
    form = RegisterForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        username = email
        if users.add(email, password):
            flash("You are successfully registered!","success")
            return redirect(url_for('login'))
        flash("Username already in use", "error")
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/groups", methods = ['POST', 'GET'])
def group():
    if session.get('username'):
        return render_template("group.html")
    return redirect(url_for('register'))

@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("You have logged out", "success")
   return redirect(url_for('home'))