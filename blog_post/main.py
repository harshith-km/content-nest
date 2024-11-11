from app import app, db
from models import ChatUser
from flask import session

# from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
# from flask import request, url_for, render_template, flash, redirect
# from sqlalchemy import func, or_

from routes import auth_routes, blog_routes, follow_routes, message_routes, misc_routes, notification_routes, users_routes


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
