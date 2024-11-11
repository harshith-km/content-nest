from app import app
from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_


@app.route('/view_notifications')
def view_notifications():
    if 'user_id' not in session:
        flash('You have to login to check your notifications', 'danger')
        return redirect(url_for('login'))

    ntfy = Notification.query.filter_by(user_id=session['user_id']).order_by(Notification.date_created.desc()).all()
    for notif in ntfy:
        notif.date_created = notif.date_created.strftime('%d-%m-%Y %I:%M %p')
    return render_template('notifications.html', ntfy=ntfy)


