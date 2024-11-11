from app import app, db, socketio
from models import User, Blog, Comment, SavedBlog, Follower, Like, Notification, Message, ChatUser
from flask import request, url_for, render_template, flash, redirect, session
from sqlalchemy import func, or_



@app.route('/chat_with_user', methods=['POST'])
def chat_with_user():
    if 'user_id' not in session:
        flash('please login to chat with users')
        return redirect(url_for('login'))
    
    chat_user_id = int(request.form['user_id'])
    chat_user_name = request.form['user_name']
    recipient = {'id':chat_user_id,'name':chat_user_name}

    old_msgs = Message.query.filter(
        or_(
            (Message.sender_id == session['user_id']) & (Message.recipient_id == chat_user_id),
            (Message.sender_id == chat_user_id) & (Message.recipient_id == session['user_id'])
        )
    ).all()    


    return  render_template('chat_with_user.html', old_msgs=old_msgs, recipient=recipient)


@socketio.on('send_message')
def handle_send_message(msg):
    if 'user_id' not in session:
        flash('please login to send and receive messages')
        return redirect(url_for('login'))

    chat_users = [] 
    users = ChatUser.query.filter_by(user_id=session['user_id']).all() 
    users_f = ChatUser.query.filter_by(chat_user_id=session['user_id']).all() 
    
    for user in users: 
        chat_users.append(int(user.chat_user_id)) 
    for user in users_f: 
        chat_users.append(int(user.chat_user_id)) 
    
    if int(msg['recipient_id']) not in chat_users:
        new_chat_user = ChatUser(user_id=session['user_id'], chat_user_id=int(msg['recipient_id']), last_message=f"Message: {msg['content']}") 
        try: 
            db.session.add(new_chat_user) 
            db.session.commit() 
            print(f'recipient id {recipient_id} not in {chat_users})') 
        except Exception as e: 
            db.session.rollback() 
            print(f'Error: {e}') 
    else:
        new_msg = Message(sender_id=msg['sender_id'], recipient_id=msg['recipient_id'], content=msg['content'])
        try:
            db.session.add(new_msg)
            db.session.commit()
            print('msg saved successfully')
        except Exception as e:
            db.session.rollback()
            print(f'Error: {e}')


@socketio.on('send_blog') 
def handle_send_blog(type, blog_id, recipient_list): 
    blog = Blog.query.filter_by(blog_id=blog_id).first() 
    sent_user = [] 
    attachment_url = f'/blog/{blog_id}' 
    
    chat_users = [] 
    users = ChatUser.query.filter_by(user_id=session['user_id']).all() 
    users_f = ChatUser.query.filter_by(chat_user_id=session['user_id']).all() 
    
    for user in users: 
        chat_users.append(int(user.chat_user_id)) 
    for user in users_f: 
        chat_users.append(int(user.chat_user_id)) 

    
    for recipient_id in recipient_list: 

        if int(recipient_id) not in chat_users: 
            new_chat_user = ChatUser(user_id=session['user_id'], chat_user_id=recipient_id, last_message=f"author: {blog.author_name} Blog: {blog.blog_title}") 
            try: 
                db.session.add(new_chat_user) 
                db.session.commit() 
                print(f'recipient id {recipient_id} not in {chat_users})')
            except Exception as e: 
                db.session.rollback() 
                print(f'Error: {e}') 
        else: 
            new_msg = Message(sender_id=session['user_id'], recipient_id=recipient_id, content=f"author: {blog.author_name} Blog: {blog.blog_title}", attachment_url=attachment_url, message_type='blog') 
            try: 
                db.session.add(new_msg) 
                db.session.commit() 
                sent_user.append(recipient_id) 
                print(f'blogs shared with user id {recipient_id}') 
            except Exception as e:
                db.session.rollback() 
                print(f'Error: {e}')

# @app.route('/send_msg',methods=['POST'])
# def send_msg():
#     if 'user_id' not in session:
#         flash('please login ro send and receive messages')
#         return redirect(url_for('login'))

#     if request.form['type']=='blog':
#         recipient_ids = request.form.getlist('user_ids')
#         blog_id = int(request.form['blog_id'])
        
#         blog = Blog.query.filter_by(blog_id=blog_id).first()
#         blog_title = blog.blog_title

#         content = f'Blog: {blog_title}'
#         attachment_url = f'/blog/{blog_id}'

#         sent_to =[]
#         errors_list = []

#         for recipient_id in recipient_ids:
#             recipient_id = int(recipient_id)
#             existing_chat = ChatUser.query.filter_by(user_id=session['user_id'],chat_user_id=recipient_id).first()

#             if not existing_chat:
#                 try:
#                     new_chat = ChatUser(user_id=session['user_id'],chat_user_id=recipient_id,last_message=content)
#                     db.session.add(new_chat)
#                     db.session.commit()
#                 except Exception as e:
#                     db.session.rollback()
#                     return f'Error: {e}'

#             new_msg = Message(
#                 sender_id = session['user_id'],
#                 recipient_id = recipient_id,
#                 content = content,
#                 message_type = 'blog',
#                 attachment_url = attachment_url
#             )
#             try:
#                 db.session.add(new_msg)
#                 db.session.commit()
#                 sent_to.append(recipient_id)
#             except Exception as e:
#                 db.session.rollback()
#                 errors_list.append(e)
        
#         return f'blog sent to {sent_to} ,Errors: {errors_list}'



@app.route('/chat_users', methods=['GET'])
def chat_users():
    if 'user_id' not in session:
        flash('please login to view messages')
        return redirect(url_for('login'))

    user_id = session['user_id']
    chat_users = ChatUser.query.filter_by(user_id=user_id).all()
    users = [chat.chat_user for chat in chat_users]

    return render_template('chat_users.html', chat_users=chat_users, users=users)



