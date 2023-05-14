from flask import Blueprint, render_template, session, redirect, request

from models import Posts, Comments, Accounts_Users
from db import db

# This file, for urls /post/resources, or /post/news other
posts_bp = Blueprint('post', __name__)


@posts_bp.route('/news')
def news_posts():
    posts = db.session.query(Posts).filter_by(type='news').all()

    return render_template('news.html', posts=posts)


@posts_bp.route('/<string:title>/<int:id>', methods=['POST', 'GET'])
def post(title, id):
    session_id_author = session.get('id')

    posts = db.session.query(Posts).filter_by(id=id).all()  
    all_news = db.session.query(Posts).filter_by(type='news').all()
    comments_for_post = db.session.query(Comments).filter_by(id_post=id).all()
    if not posts:
        return render_template('not_found_post.html')

    
    author_comment = db.session.query(Accounts_Users).all()
        

    # Comment
    if request.method == 'POST':
        text_comment = request.form['text_comment']

        # save
        save_comment = Comments(text=text_comment, id_post=id, id_author=session_id_author)
        db.session.add(save_comment)
        db.session.commit()    

        return redirect(f'/post/{title}/{id}')


    return render_template('post.html', posts=posts, all_news=all_news, comments_for_post=comments_for_post, author_comment=author_comment)    