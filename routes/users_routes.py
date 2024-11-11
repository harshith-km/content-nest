from app import app, db
from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_

@app.route('/view_user/<int:user_id>')
def view_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    blogs = Blog.query.filter_by(author_id=user_id).all()

    follows = Follower.query.filter_by(follower_id=session['user_id']).all()
    followings_ids =[]
    for following in follows:
        followings_ids.append(following.user_id)

    return render_template('view_user.html', user=user, blogs=blogs, followings_ids=followings_ids)

@app.route('/all_users')
def all_users():
    if 'user_id' not in session:
        flash('login to view all users')
        return redirect(url_for('login'))
    else:
        users = User.query.all()
        return render_template('view_users.html', users=users)



