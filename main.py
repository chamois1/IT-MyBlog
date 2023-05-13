import os
import uuid
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash
from flask_ckeditor import CKEditor

from db import db_init, db  
from models import Accounts_Users, Posts
from admin_panel import admin_bp

# settings
app = Flask(__name__)
ckeditor = CKEditor(app)

# urls from file admin_panel
app.register_blueprint(admin_bp)

# config
app.config['SECRET_KEY'] = '(#U(@FU*AUF*UIAJ091E)!(@#$*190()$!2497() FUIAJQIJ*($@#!*7EDSAIJIDJAS)))'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/'

db_init(app)
Session(app)


# decorator, checking session on user, whether the user is logged into the account
def session_required(f):
    @wraps(f)
    def decorated_if_session(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('sign_in'))
        return f(*args, **kwargs)
    return decorated_if_session


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
                avatar.save(os.path.join(app.config['UPLOAD_FOLDER'] + f'avatars/{img}'))
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'] + f'avatars/{img}')
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
       
       if check_password_hash(search_account.password, password):
           # save session
           session['id'] = search_account.id
           session['is_admin'] = search_account.is_admin
           return redirect('/my-profile')
       
       else:
           flash('Пароль не вірний')
           return redirect('/sign-in')

    return render_template('sign_in.html')


@app.route('/my-profile', methods=['POST', 'GET'])
@session_required
def my_profile():
    session_id = session.get('id')
    session_is_admin = session.get('is_admin')
    account = db.session.query(Accounts_Users).filter_by(id=session_id).first()


    # button
    if 'logout' in request.form:
        session.clear()
        return redirect('sign-in')


    context = {
        'account': account,
        'session_is_admin': session_is_admin
    }


    return render_template('my_profile.html', **context)



if __name__ == '__main__':
    app.run(debug=True)