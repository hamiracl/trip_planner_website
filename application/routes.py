from application import app
from application.models import db, Users, Groups, Room, Posts
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.forms import LoginForm, RegisterForm, GroupCreation, JoinGroup
from application.models import Users, Room, Groups
from werkzeug.security import check_password_hash

@app.route("/")
@app.route("/home")
def home():
    if session.get('username'):
       return redirect(url_for('group'))
    return render_template("home.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if session.get('id'):
        return redirect(url_for('group'))
    form = LoginForm()
    if form.validate_on_submit():
        email      = form.email.data
        password    = form.password.data

        user = Users.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You are successfully Logged In!","success")
                session['id'] = user.id
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
        if Users.query.filter_by(email = email).first() == None:
            user = Users(email = email, password = password)
            db.session.add(user)
            db.session.commit()
            flash("You are successfully registered!","success")
            return redirect(url_for('login'))
        flash("Username already in use", "error")
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/groups", methods = ['POST', 'GET'])
def group():
    if session.get('id'):
        groups = Groups.query.filter_by(user = session.get('id')).all()
        rooms = []
        for group in groups:
            room = Room.query.filter_by(id = group.room).first()
            if rooms.count(room) == 0:
                rooms.append(room)
        return render_template("group.html", roomData = rooms)
    return redirect(url_for('register'))

@app.route('/create', methods = ['POST', 'GET'])
def create_group():
    if session.get('id'):
        form = GroupCreation()
        if form.validate_on_submit():
            name = form.name.data
            if Room.query.filter_by(name = name, admin = session.get('id')).first() == None:
                room = Room(admin = session.get('id'), name = name)
                db.session.add(room)
                db.session.commit()
                rooms = Room.query.all()
                group  = Groups(room = room.id, user = session.get('id'))
                db.session.add(group)
                db.session.commit()
            else: 
                flash("You have already created a group with this name", "error")
            groups = Groups.query.filter_by(user = session.get('id')).all()
            rooms = []
            for group in groups:
                room = Room.query.filter_by(id = group.room).first()
                if rooms.count(room) == 0:
                    rooms.append(room)
            return render_template("group.html", roomData = rooms)
        return render_template("create_group.html", form = form)
    return redirect(url_for('register'))

@app.route('/join', methods = ['POST', 'GET'])
def join_group():
    if session.get('id'):
        form = JoinGroup()
        if form.validate_on_submit():
            id = form.groupID.data
            if Room.query.filter_by(id = id).first() != None:
                if Groups.query.filter_by(user = session.get('id'), room = id).first() != None:
                    flash("You are already in this group", "error")
                else:
                    group  = Groups(room = id, user = session.get('id'))
                    db.session.add(group)
                    db.session.commit()
            else: 
                flash("Group does not exist", "error")
            groups = Groups.query.filter_by(user = session.get('id')).all()
            rooms = []
            for group in groups:
                room = Room.query.filter_by(id = group.room).first()
                if rooms.count(room) == 0:
                    rooms.append(room)
            return render_template("group.html", roomData = rooms)
        return render_template("join.html", form = form)
    return redirect(url_for('register'))


@app.route('/logout')
def logout():
   session.pop('id', None)
   flash("You have logged out", "success")
   return redirect(url_for('home'))