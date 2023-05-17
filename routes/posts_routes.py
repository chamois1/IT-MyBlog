from flask import Blueprint, render_template, session, redirect, request
from flask_paginate import Pagination, get_page_args

from models import Posts, Comments, Accounts_Users, ReplyComment
from db import db

# This file, for urls /post/resources, or /post/news other
posts_bp = Blueprint('post', __name__)


@posts_bp.route('/news')
def news_posts():
    """ Geting all posts for 'news', and pagination to split them into multiple pages """

    # page arguments
    page, per_page, offset = get_page_args()

    # Apply pagination, and create object paginations
    query  = Posts.query.filter_by(type='news')
    posts = query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, per_page=per_page, total=Posts.query.count(), css_framework='bootstrap4')
    
    return render_template('news.html', posts=posts, pagination=pagination)


@posts_bp.route('/post/<string:title>/<int:id>', methods=['POST', 'GET'])
def post(title, id):
    """ See post. Adding Comment, reply, other """

    response = redirect(f'/post/{title}/{id}')
    session_id_author = session.get('id')

    posts = db.session.query(Posts).filter_by(id=id).all()  
    all_posts = db.session.query(Posts).filter_by(type='news').all()
    comments_for_post = db.session.query(Comments).filter_by(id_post=id).all()
    replys_comments = db.session.query(ReplyComment).all()
    user = db.session.query(Accounts_Users).filter_by(id=session_id_author)


    if not posts:
        return render_template('not_found_post.html')
    

    if session_id_author:
        # save id post in history
        user = db.session.query(Accounts_Users).filter_by(id=session_id_author).first()

        if not id in user.latter_view:
            latter_history = user.latter_view
            latter_history.append(id)

            db.session.query(Accounts_Users).filter_by(id=session_id_author).update({'latter_view': latter_history})
            db.session.commit()

   
        # buttons, save post, like
        if 'save_post' in request.form:
            save_post = user.save_posts

            if not id in user.save_posts:
                save_post.append(id)    
                
                db.session.query(Accounts_Users).filter_by(id=session_id_author).update({'save_posts': save_post})
                db.session.commit()


        if 'like_post' in request.form:
            like_post = user.like_posts

            if not id in user.like_posts:
                like_post.append(id)
                
                db.session.query(Accounts_Users).filter_by(id=session_id_author).update({'like_posts': like_post})
                db.session.commit()


        # Comment
        if 'text_comment' in request.form:
            # create comment
            text_comment = request.form['text_comment']

            # save
            save_comment = Comments(text=text_comment, title_post=title, id_post=id, id_author=session_id_author)
            db.session.add(save_comment)
            db.session.commit()    
        

            return response


        # Reply comment
        if 'reply-text' in request.form:
            # interact other comment
            reply_comment = request.form['reply-text']
            id_main_comment = request.form['comment-id']
            
            save_replyComment = ReplyComment(text=reply_comment, id_main_comment=id_main_comment, id_author_reply=session_id_author, login_author_reply=user.login, avatar_author_reply=user.img_avatar)
            db.session.add(save_replyComment)
            db.session.commit()
            
            return response


        # edit my comment
        # delete 
        if 'del-id-my-comment' in request.form:
            del_id_my_comment = request.form['del-id-my-comment']

            db.session.query(Comments).filter_by(id=del_id_my_comment).delete()
            db.session.commit()
            db.session.close()
            
            return response

        
        # edit text
        if 'id-com-edit' in request.form:
            id_com_edit = request.form['id-com-edit']
            text_edit = request.form['text_edit']

            db.session.query(Comments).filter_by(id=id_com_edit).update({'text': text_edit})
            db.session.commit()


    author_comment = db.session.query(Accounts_Users).all()     
    

    context = {
        'posts': posts,
        'all_posts': all_posts,
        'comments_for_post': comments_for_post,
        'author_comment': author_comment,
        'replys_comments': replys_comments,
        'user': user
    }
    return render_template('post.html', **context)    