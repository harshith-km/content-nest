from app import app, db
from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_


@app.route('/write_blog', methods=['POST','GET'])
def write_blog():
    if request.method == 'POST':
        author_id = session['user_id']
        author_name = session['user_fname'] + ' ' + session['user_lname']
        blog_title = request.form['title']
        blog_content = request.form['content']
        new_blog = Blog(author_id=author_id, author_name=author_name, blog_title=blog_title, blog_content=blog_content)
        try:
            db.session.add(new_blog)
            db.session.commit()

            followers = Follower.query.filter_by(user_id=author_id).all()
            notified_users = set()

            notification_msg = f'{author_name} has published a new blog: {blog_title}'

            for follower in followers:
                new_notification = Notification(user_id=follower.follower_id,message=notification_msg)
                db.session.add(new_notification)
                notified_users.add(follower.follower_id)

            db.session.commit()
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('your_blogs'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('write_blog'))
    return render_template('blog_edit.html')

@app.route('/like_blog/<int:blog_id>/<from_addr>', methods=['GET'])
def like_blog(blog_id, from_addr):
    if 'user_id' not in session:
        flash('Please login to like the blog', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    existing_like = Like.query.filter_by(user_id=user_id, blog_id=blog_id).first()

    if existing_like:
        db.session.delete(existing_like)
        flash('You unliked the blog', 'info')
    else:
        new_like = Like(user_id=user_id, blog_id=blog_id)
        db.session.add(new_like)
        flash('You liked the blog', 'success')

    db.session.commit()
    return redirect(url_for(from_addr, blog_id=blog_id))


@app.route('/save_blog/<int:blog_id>/<from_addr>', methods=['GET'])
def save_blog(blog_id, from_addr=False):
    if 'user_id' not in session:
        flash('Please log in to save blogs.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    x = SavedBlog.query.filter_by(user_id=user_id, blog_id=blog_id).first()
    if x:
        flash('Blog already saved')
    else:
        saved_blog = SavedBlog(user_id=user_id, blog_id=blog_id)
        try:
            db.session.add(saved_blog)
            db.session.commit()
            flash(f'Blog saved')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}")

    return redirect(url_for(from_addr,blog_id=blog_id))

@app.route('/saved_blogs', methods=['GET'])
def saved_blogs():
    if 'user_id' not in session:
        flash('Please log in to view your saved blogs.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    saved_blogs = SavedBlog.query.filter_by(user_id=user_id).all()
    return render_template('saved_blogs.html', saved_blogs=saved_blogs)

@app.route('/blog/<int:blog_id>')
def view_blog(blog_id):
    blog = Blog.query.filter_by(blog_id=blog_id).first()
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    liked = Like.query.filter_by(user_id=session['user_id'],blog_id=blog_id).first()
    saved = SavedBlog.query.filter_by(user_id=session['user_id'],blog_id=blog_id).first()

    saved_blogs = SavedBlog.query.filter_by(user_id=session['user_id']).all()
    saved_blog_ids = []
    for saved_blog in saved_blogs:
        saved_blog_ids.append(saved_blog.blog_id)

    for comment in comments:
        comment.date_posted = comment.date_posted.strftime("%m-%d-%Y %I:%M %p")

    return render_template('view_blog.html', blog=blog, liked=liked, saved=saved, comments=comments, saved_blog_ids=saved_blog_ids)



@app.route('/your_blogs', methods=['GET'])
def your_blogs(message=False):
    if 'user_id' not in session:
        flash('Please log in to view your blogs.', 'danger')
        return redirect(url_for('login'))

    saved_blogs = SavedBlog.query.filter_by(user_id=session['user_id']).all()
    saved_blog_ids = []
    for saved_blog in saved_blogs:
        saved_blog_ids.append(saved_blog.blog_id)

    blogs = Blog.query.filter_by(author_id=session['user_id']).all()
    return render_template('your_blogs.html', blogs=blogs, saved_blog_ids=saved_blog_ids)


@app.route('/share_blog/<int:blog_id>',methods=['GET','POST'])
def share_blog(blog_id):
    if 'user_id' not in session:
        flash('Please log in to share blogs.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'GET':
        users = Follower.query.filter_by(follower_id=session['user_id']).all()
        users_f = []
        for user in users:
            x = User.query.filter_by(id=user.user_id).first()
            users_f.append(x)
        return render_template('share_blog.html',blog_id=blog_id,users_f=users_f)


@app.route('/suggest_more')
def suggest_more():
    if 'user_id' not in session:
        flash('plsease login to view more blogs')
        return redirect(url_for('login'))

    blogs = SavedBlog.query.filter_by(user_id=session['user_id']).all()

    saved_blog_ids = []
    for blog in blogs:
        saved_blog_ids.append(blog.blog_id)


    blogs = Blog.query.all()
    return render_template('suggest_more.html',blogs=blogs, saved_blog_ids=saved_blog_ids)


@app.route('/delete_saved_blog/<int:blog_id>/<from_addr>', methods=['POST','GET'])
def delete_saved_blog(blog_id,from_addr):
    if 'user_id' not in session:
        flash('Please log in to view delete blogs.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    blog = SavedBlog.query.filter_by(user_id=user_id, blog_id=blog_id).first()
    if blog:
        try:
            db.session.delete(blog)
            db.session.commit()
            flash(f'Blog with ID: {blog_id} deleted successfully')
        except Exception as e:
            db.session.rollback()
            flash(f'ERROR: {e}')
    else:
        flash(f'Blog with ID: {blog_id} not found in saved.')

    return redirect(url_for(from_addr, blog_id=blog_id))


@app.route('/comment',methods=['POST'])
def comment():
    if 'user_id' not in session:
        flash('Please login to comment on blogs')
        return redirect(url_for('login'))

    blog_id = request.form['blog_id']
    content = request.form['content']
    user_email = session['user_email']
    new_comment = Comment(blog_id=blog_id,user_email=user_email,content=content)
    try:
        db.session.add(new_comment)
        db.session.commit()
        flash('comment has been posted')
    except Exception as e:
        db.session.rollback()
        flash('Error: {e}')
    return redirect(url_for('view_blog',blog_id=blog_id))
