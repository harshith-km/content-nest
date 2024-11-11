from app import app, db
from models import User, Blog, Comment, SavedBlog, Follower
from flask import request, url_for, render_template, flash, redirect, session


@app.route('/analysis')
def analysis():
    if 'user_id' not in session:
        flash('Please log in to view your Analysis.', 'danger')
        return redirect(url_for('login'))

    followers = Follower.query.filter_by(user_id=session['user_id']).count()
    following = Follower.query.filter_by(follower_id=session['user_id']).count()
    your_blogs = Blog.query.filter_by(author_id=session['user_id']).count()
    saved_blogs = SavedBlog.query.filter_by(user_id=session['user_id']).count()
    analysis = {'followers': followers,'following':following,'your_blogs':your_blogs,'saved_blogs':saved_blogs}

    # return f'{analysis}'
    return render_template('analysis.html', analysis=analysis)


@app.route('/settings')
def settings():
    return render_template('settings.html')
@app.route('/blog_card')
def blog_card():
    return render_template('blog_card.html')


@app.route('/test', methods=['POST','GET'])
def test():
    if request.method == 'POST':
        if request.form['type'] and request.form['type']=='blog':
            user_id = request.form['user_id']
            user_name = request.form['user_name']
            return f'this is blog type content , and recevied user id {user_id}, user name {user_name}'
        else:
            return f'this is not blog type'
    else:
        return render_template('test.html')
    # return render_template('test.html')

@app.route('/')
def goto_url():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    users = User.query.limit(4).all()
    blogs = Blog.query.limit(4).all()

    saved_blogs = SavedBlog.query.filter_by(user_id=session['user_id']).all()
    saved_blog_ids = []
    for saved_blog in saved_blogs:
        saved_blog_ids.append(saved_blog.blog_id)

    follows = Follower.query.filter_by(follower_id=session['user_id']).all()
    followings_ids =[]
    for following in follows:
        followings_ids.append(following.user_id)

    return render_template('home.html',blogs=blogs,users=users, following_ids=followings_ids,saved_blog_ids=saved_blog_ids)
