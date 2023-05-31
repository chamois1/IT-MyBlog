from flask import Blueprint, render_template, session, redirect, request
from flask_paginate import Pagination, get_page_args
from sqlalchemy import cast, String

from models import Posts, Comments, Accounts_Users, ReplyComment, listRequestEdit
from db import db

from datetime import datetime

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
    
    return render_template('news.html', posts=posts, pagination=pagination, now_date=datetime.now())


@posts_bp.route('/post/<string:title>/<int:id>', methods=['POST', 'GET'])
def post(title, id):
    """ See post. Adding Comment, reply, other """

    response = redirect(f'/post/{title}/{id}')
    session_id_author = session.get('id')

    # info for post
    post = db.session.query(Posts).filter_by(id=id)
    post_likes = db.session.query(Accounts_Users).filter(cast(Accounts_Users.like_posts, String).like('%{}%'.format(id))).all()
    post_saves = db.session.query(Accounts_Users).filter(cast(Accounts_Users.save_posts, String).like('%{}%'.format(id))).all()

    comments_for_post = db.session.query(Comments).filter_by(id_post=id).all()
    replys_comments = db.session.query(ReplyComment).all()

    all_posts = db.session.query(Posts).all()
    user = db.session.query(Accounts_Users).filter_by(id=session_id_author)

    if not post:
        return render_template('not_found_post.html')
    
    # save view
    history_view = post.first().history_view 
    history_view += 1
    
    post.update({'history_view': history_view})
    db.session.commit()

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

    
        if 'textEditsPosts' in request.form:
            # What should be changed in the post
            # The user sends a request to change it
            
            textEditsPosts = request.form['textEditsPosts']
            
            saveList_EditPost = listRequestEdit(text=textEditsPosts, title_post=title, id_post=id, id_author=session_id_author)
            db.session.add(saveList_EditPost)
            db.session.commit()

            return response
           

        # Comments
        if 'text_comment' in request.form:
            # create comment
            text_comment = request.form['text_comment']

            # save
            save_comment = Comments(text=text_comment, title_post=title, id_post=id, id_author=session_id_author)
            db.session.add(save_comment)
            db.session.commit()    

            return response


        # buttons for comments
        # Reply comment
        if 'reply-text' in request.form:
            # interact other comment
            reply_comment = request.form['reply-text']
            id_main_comment = request.form['comment-id']
            
            save_replyComment = ReplyComment(text=reply_comment, id_main_comment=id_main_comment, id_author_reply=session_id_author, login_author_reply=user.login, avatar_author_reply=user.img_avatar)
            db.session.add(save_replyComment)
            db.session.commit()
            
            return response


        if 'like-comment' in request.form:
            like_comment = request.form['like-comment']

            # save like in list
            comment_like = db.session.query(Comments).filter_by(id=like_comment).first()

            if not session_id_author in comment_like.likes:
                comment_like.likes.append(session_id_author)

                db.session.query(Comments).filter_by(id=like_comment).update({'likes': comment_like.likes})
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


        # admin buttons
        if 'delete-comment-user' in request.form:
            delete_comment_user = request.form['delete-comment-user']

            db.session.query(Comments).filter_by(id=delete_comment_user).delete()
            db.session.commit()

            return response


    author_comment = db.session.query(Accounts_Users).all()     
    

    context = {
        'post': post.first(),
        'all_posts': all_posts,
        'comments_for_post': comments_for_post,
        'post_likes': post_likes,
        'post_saves': post_saves,

        'author_comment': author_comment,
        'replys_comments': replys_comments,
        'user': user
    }
    return render_template('post.html', **context)    