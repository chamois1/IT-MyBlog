import os
import uuid

from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash
from flask_ckeditor import CKEditor

from db import db_init, db
from models import Accounts_Users
from routes.admin_panel import admin_bp
from routes.posts_routes import posts_bp
from routes.profile_users import profiles

"""
This file for starting server, settings and users authorizations
"""

# settings
app = Flask(__name__)
ckeditor = CKEditor(app)

# urls from file admin_panel
app.register_blueprint(admin_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(profiles)

# config
app.config['SECRET_KEY'] = '(#U(@FU*AUF*UIAJ091E)!(@#$*190()$!2497() FUIAJQIJ*($@#!*7EDSAIJIDJAS)))'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/'

db_init(app)
Session(app)


# function will pass variables for all html
@app.context_processor
def session_base():
    session_is_admin = session.get('is_admin')
    id_session = session.get('id')
    return dict(session_is_admin=session_is_admin, id_session=id_session)


# Main page
@app.route('/')
def index():    
    return render_template('index.html')


# Sign up
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
       # form       
       login = request.form["login"]
       email = request.form["email"]
       avatar = request.files['avatar']
       password = request.form["password"].encode('utf-8') 


       # checking existing account
       search_dublicate_account = db.session.query(Accounts_Users).filter_by(email=email).first()

       if not search_dublicate_account:
    
            bcrypt = Bcrypt()
            password_hash = bcrypt.generate_password_hash(password)


            if avatar:
                # Generate a unique image using UUID and save the avatar
                img = str(uuid.uuid4()) + os.path.splitext(avatar.filename)[1]
                app_config = os.path.join(app.config['UPLOAD_FOLDER'] + f'avatars/{img}') 

                avatar.save(app_config)
                avatar_path = os.path.join(app_config)
            else: 
                avatar_path = app.config['UPLOAD_FOLDER'] + '/avatars/default_avatar.jpg'


            # save
            save_data = Accounts_Users(img_avatar=avatar_path, login=login, email=email, password=password_hash)
            db.session.add(save_data)
            db.session.commit()
            

            return redirect('/sign-in')
       else:
            flash('Така пошта вже зарегестрована')
            return redirect('/sign-up')


    return render_template('sign_up.html')


# Sign in 
@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():    
    if request.method == "POST":
       # form       
       email = request.form["email"]
       password = request.form["password"].encode('utf-8') 

    
       search_account = db.session.query(Accounts_Users).filter_by(email=email).first()
       if not search_account:
            flash('Такого користувача не існує')
            return redirect('/sign-in')
       
       elif search_account.is_block == True:
           flash(f'Ви були заблоковані, по причині\n "{search_account.reason_block}"')
           return redirect('/sign-in')
       

       if check_password_hash(search_account.password, password):
           # save session
           session['id'] = search_account.id
           session['is_admin'] = search_account.is_admin
           return redirect('/my-profile')
       else:
           flash('Пароль не вірний')
           return redirect('/sign-in')

    return render_template('sign_in.html')



if __name__ == '__main__':
    app.run(debug=True)