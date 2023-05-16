import os
import uuid
from functools import wraps

from flask import render_template, request, redirect, flash, session, url_for, Blueprint, current_app
from flask_bcrypt import Bcrypt, check_password_hash

from db import db
from models import Accounts_Users, Posts, Comments


# This file, for urls /my-profile/settings, or other
profiles = Blueprint('my-profile', __name__)


# decorator, checking session on user, whether the user is logged into the account
def auth_user(f):
    @wraps(f)
    def decorated_if_session(*args, **kwargs):
        # parameters for functions
        id_user = session.get('id')
        account = db.session.query(Accounts_Users).filter_by(id=id_user).first()

        # checking sesion
        if 'id' not in session:
            return redirect(url_for('sign_in'))
        return f(id_user, account, *args, **kwargs)
    
    return decorated_if_session


# my profile
@profiles.route('/my-profile', methods=['POST', 'GET'])
@auth_user
def my_profile(id_user, account):
    latter_posts = db.session.query(Posts).filter(Posts.id.in_(account.latter_view)).all()

    # latter posts
    if len(account.latter_view) > 10:
        list_post = account.latter_view[10:]

        db.session.query(Accounts_Users).filter_by(id=id_user).update({'latter_view': list_post})
        db.session.commit()


    # button logout account
    if 'logout' in request.form:
        session.clear()
        return redirect('sign-in')

    return render_template('my_profile.html', account=account, latter_posts=latter_posts)


# settings
@profiles.route('/my-profile/settings', methods=['POST', 'GET'])
@auth_user
def settings_profile(id_user, account):

    # form
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        actual_password = request.form['actual_password']
        new_password = request.form['new_password']
        avatar = request.files['avatar']

        if check_password_hash(account.password, actual_password):       
            bcrypt = Bcrypt()

            if new_password:
                password_hash = bcrypt.generate_password_hash(new_password)

            if avatar:
                # Generate a unique image using UUID and save the avatar
                img = str(uuid.uuid4()) + os.path.splitext(avatar.filename)[1]
                app_config = os.path.join(current_app.config['UPLOAD_FOLDER'] + f'avatars/{img}') 

                avatar.save(app_config)
                avatar_path = os.path.join(app_config)
            else: 
                avatar_path = current_app.config['UPLOAD_FOLDER'] + '/avatars/default_avatar.jpg'

            db.session.query(Accounts_Users).filter_by(id=id_user).update(
                {
                    'login': login,
                    'email': email,
                    'password': password_hash if new_password else account.password,
                    'img_avatar': avatar_path
                }
            )

            db.session.commit()
            session.clear()
            return redirect('/sign-in')
        else:
            flash('Поточний пароль не вірний')
            return redirect('./settings')    
 

    return render_template('profile_settings.html', account=account)


# history comments
@profiles.route('/my-profile/history-comments', methods=['POST', 'GET'])
@auth_user
def history_comments(id_user, account):
    comments = db.session.query(Comments).filter_by(id_author=id_user).all()

    # button delete comment
    if request.method == 'POST':
        delete_comment = request.form['comment-delete']
        
        db.session.query(Comments).filter_by(id=delete_comment).delete()
        db.session.commit()
          
        return redirect('./history-comments')


    return render_template('history_comments.html', account=account, comments=comments)        


#TODO: buttons delete save post, and like
#TODO: Показувати у пості скільки лайків, зберегло, коментарів (число)

# save posts
@profiles.route('/my-profile/save-posts')
@auth_user
def save_posts(id_user, account):
    save_posts = db.session.query(Posts).filter(Posts.id.in_(account.save_posts)).all()

    return render_template('save_posts.html', account=account, save_posts=save_posts)


# like posts
@profiles.route('/my-profile/like-posts')
@auth_user
def like_post(id_user, account):
    like_posts = db.session.query(Posts).filter(Posts.id.in_(account.like_posts)).all()

    return render_template('like_post.html', account=account, like_posts=like_posts)