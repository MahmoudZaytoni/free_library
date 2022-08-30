import imp,os
from flask import Blueprint, render_template, request, flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)
admin_email = "admin@gmail.com"

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if email == admin_email:
                    flash("Admin Logged in Successfully", category='success')
                else:
                    flash(f"Welcome Back {user.first_name}!\n Start having Fun with our free books", category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.homePage'))
            else:
                flash("Incorrect password, try Again. ", category='error')
        else:
            flash("Email Doesn't Exist. ", category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist. ", category='error')
        elif password1 != password2:
            flash("Password don't match ", category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            if email == admin_email:
                flash("Created Admin Account Successfuly", categroy='success')
            else:
                flash(f"Welcome {firstName}\nStart having fun with our Free books", category='success')
            return redirect(url_for("view.homePage"))
    return render_template('register.html', user=current_user)
