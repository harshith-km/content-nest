from app import app, db
from models import User, Follower
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        user = User.query.filter_by(user_email=user_email).first()
        if user and check_password_hash(user.user_password, user_password):
            session['user_id'] = user.id
            session['user_fname'] = user.user_fname
            session['user_lname'] = user.user_lname
            session['user_email'] = user.user_email
            try:
                session['followers_count'] = Follower.query.filter_by(user_id=session['user_id']).count()
                session['following_count'] = Follower.query.filter_by(follower_id=session['user_id']).count()
                flash(f"Welcome {session['user_fname']}", 'success')
            except Exception as e:
                flash(f'Error {e}')

            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_fname = request.form['user_fname'].capitalize()
        user_lname = request.form['user_lname'].capitalize()
        user_mob_no = request.form['user_mob_no']
        user_email = request.form['user_email']
        user_password = generate_password_hash(request.form['user_password'])
        new_user = User(user_fname=user_fname, user_lname=user_lname, user_mob_no=user_mob_no, user_email=user_email, user_password=user_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", 'danger')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_fname', None)
    session.pop('user_lname', None)
    session.pop('user_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))