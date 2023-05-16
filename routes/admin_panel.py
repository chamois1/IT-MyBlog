import os
import uuid
from functools import wraps

from flask import Blueprint, render_template, session, redirect, url_for, request, current_app

from models import Posts
from db import db


# This file, for urls /admin, or /admin/settings other
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# decorator, checking of admin user or not, and authorization
def is_admin(f):
    @wraps(f)
    def decorated_is_admin(*args, **kwargs):
        session_is_admin = session.get('is_admin')
        if session_is_admin == False or not 'is_admin' in session:
            return redirect(url_for('my_profile'))
        return f(*args, **kwargs)
    return decorated_is_admin


@admin_bp.route('/')
@is_admin
def admin():
    return render_template('admin_panel.html')


@admin_bp.route('/add-post', methods=['POST', 'GET'])
@is_admin
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tag = request.form['tags']
        image = request.files['image-post']
        type = request.form['type']

        if image:
            # Generate a unique image using UUID and save the avatar
            img = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + f'posts/{img}'))
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'] + f'posts/{img}')
        else: 
            image_path = current_app.config['UPLOAD_FOLDER'] + 'posts/default_post.jpeg'


        # save
        tags = tag.split()
        edit_tags = ""

        for i in tags:
            edit_tags += f'#{i} '


        save_data = Posts(title=title, description=description, tag=edit_tags, image=image_path, type=type)
        db.session.add(save_data)
        db.session.commit()

      
        return redirect('/')

    return render_template('add_post.html')