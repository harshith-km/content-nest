from app import app, db
from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_

@app.route('/followed_by', methods=['GET'])
def followed_by():
    if 'user_id' not in session:
        flash('Login to view the followers', 'danger')
        return redirect(url_for('login'))

    followed_by = Follower.query.filter_by(user_id=session['user_id']).all()

    following = Follower.query.filter_by(follower_id=session['user_id']).all()

    following_ids = []
    for x in following:
        following_ids.append(x.user_id)

    if followed_by:
        users = []
        for user in followed_by:
            user = User.query.filter_by(id=user.follower_id).first()
            users.append(user)
    else:
        flash('No followers found.', 'info')
    return render_template('followed_by.html', users=users, following_ids=following_ids)
    # return f'{users}'


@app.route('/following')
def following():
    if 'user_id' not in session:
        flash('please login to view the followings')
        return redirect(url_for('login'))

    following = Follower.query.filter_by(follower_id=session['user_id']).all()
    session['following_count'] = Follower.query.filter_by(follower_id=session['user_id']).count()

    users = []

    for x in following:
        user = User.query.filter_by(id=x.user_id).first()
        users.append(user)

    return render_template('following.html', following=following, users=users)

@app.route('/follow/<int:user_id>/<user_name>/<from_addr>', methods=['POST'])
def follow(user_id, user_name, from_addr):
    if 'user_id' not in session:
        flash('Please login to follow the users', 'danger')
        return redirect(url_for('login'))

    follower_name = session['user_fname'] + ' ' + session['user_lname']
    start_follow = Follower(user_id=user_id,user_name=user_name,follower_id=session['user_id'],follower_name=follower_name)
    try:
        session['following_count'] = Follower.query.filter_by(follower_id=session['user_id']).count()
        db.session.add(start_follow)
        db.session.commit()
        flash(f'You started following {user_name}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    return redirect(url_for(from_addr,user_id=user_id))

@app.route('/unfollow', methods=['POST'])
def unfollow():
    user_id = request.form['follows_id']
    from_addr = request.form['from_addr']
    user_name = request.form['user_name']

    x = Follower.query.filter_by(user_id=user_id, follower_id=session['user_id']).first()
    if x:
        try:
            db.session.delete(x)
            db.session.commit()
            flash(f'You have unfollowed {user_name}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    else:
        flash("Couldn't find the user in your following list", 'danger')

    return redirect(url_for(from_addr, user_id=user_id))
