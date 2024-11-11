from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy import ForeignKey
from app import db



class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    follower_name = db.Column(db.String(100), nullable=False)
    date_followed = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='following')
    follower = db.relationship('User', foreign_keys=[follower_id], backref='followed_by')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(100), nullable=False)
    user_lname = db.Column(db.String(100), nullable=False)
    user_mob_no = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)
    followed = db.relationship('Follower', foreign_keys=[Follower.user_id], backref='user_following')
    followers = db.relationship('Follower', foreign_keys=[Follower.follower_id], backref='user_followed_by')
    notifications = db.relationship('Notification', backref='notified_user', lazy=True)  # Uncommented and renamed backref
   

class ChatUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    chat_user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    last_message = db.Column(db.Text, nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='chats')
    chat_user = db.relationship('User', foreign_keys=[chat_user_id])


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    message_type = db.Column(db.String(20), nullable=False, default='text')
    attachment_url = db.Column(db.String(500), nullable=True)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='recevied_message')


class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.String(200), db.ForeignKey('user.id'), nullable=False)
    author_name = db.Column(db.String(200), nullable=False)
    blog_title = db.Column(db.String(200), nullable=False)
    blog_content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', back_populates='blog', lazy=True)
    likes = db.relationship('Like', back_populates='blog', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id'), nullable=False)
    user_email = db.Column(db.String(100), db.ForeignKey('user.user_email'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blog = db.relationship('Blog', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

class SavedBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id'), nullable=False)
    date_saved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref='saved_blogs')
    blog = db.relationship('Blog', backref='saved_blogs')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id'), nullable=False)
    date_liked = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref='likes')
    blog = db.relationship('Blog', back_populates='likes')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref='user_notifications', lazy=True)  # Correct backref
