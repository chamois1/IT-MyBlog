from datetime import datetime
from db import db
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, JSON, ForeignKey


# Column accounts for users
class Accounts_Users(db.Model):
    """
       If user - Allow users to leave comments under posts
       if admin - edit comments, create post, other
    """

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False)
    password = Column(String(255), nullable=False)
    img_avatar = Column(String(255), nullable=True, default='/images/avatars/default_avatar.jpeg')

    latter_view = Column(JSON, default=[])
    save_posts = Column(JSON, default=[])
    like_posts = Column(JSON, default=[])

    is_admin = Column(Boolean, default=False)

    is_block = Column(Boolean, default=False)
    reason_block = Column(String, nullable=True)


# Posts
class Posts(db.Model):
    __tablename__ = "posts"   

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String)
    description = Column(Text)
    tag = Column(String)
    image = Column(String, nullable=True, default='static/images/posts/default_post.jpeg')
    type = Column(String)

    history_view = Column(Integer, default=0)

    # connections of models
    comments = db.relationship('Comments', backref='post', lazy=True)


# Comments for post
class Comments(db.Model):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    id_post = Column(Integer, ForeignKey('posts.id'))
    title_post = Column(String)
    id_author = Column(Integer)

    # save the user id in the favorites list to check if he clicked
    likes = Column(JSON, default=[])


# Reply comment for main comment
class ReplyComment(db.Model):
    __tablename__ = "reply_comment"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    id_main_comment = Column(Integer)

    id_author_reply = Column(Integer)
    login_author_reply = Column(String)
    avatar_author_reply = Column(String)


# Edits to the post
class listRequestEdit(db.Model):
    __tablename__ = "listRequestPost"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)

    id_post = Column(Integer)
    title_post = Column(String)

    id_author = Column(Integer)