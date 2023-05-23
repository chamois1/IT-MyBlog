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

    id = Column("id", Integer, primary_key=True, nullable=False)
    login = Column('login', String(25), nullable=False)
    email = Column("emai", String(25), nullable=False)
    password = Column("password", String, nullable=False)
    img_avatar = Column("avatar", String, nullable=True, default='/images/avatars/default_avatar.jpeg')

    latter_view = Column("history_view", JSON, default=[])
    save_posts = Column("save_posts", JSON, default=[])
    like_posts = Column("like_posts", JSON, default=[])

    is_admin = Column(Boolean, default=False)

    is_block = Column(Boolean, default=False)
    reason_block = Column('reason_block', String, nullable=True)


# Posts
class Posts(db.Model):
    __tablename__ = "posts"   

    id = Column("id", Integer, primary_key=True)
    date = Column('date', DateTime)
    title = Column('title', String)
    description = Column("description", Text)
    tag = Column("tag", String)
    image = Column("image", String, nullable=True, default='/images/posts/default_post.jpeg')
    type = Column('type', String)

    history_view = Column('history_view', Integer, default=0)

    # connections of models
    comments = db.relationship('Comments', backref='post', lazy=True)


# Comments for post
class Comments(db.Model):
    __tablename__ = "comments"

    id = Column("id", Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column('text', Text)
    id_post = Column('id_post', Integer, ForeignKey('posts.id'))
    title_post = Column('title_post', String)
    id_author = Column('id_author', Integer)

    # save the user id in the favorites list to check if he clicked
    likes = Column('likes', JSON, default=[])


# Reply comment for main comment
class ReplyComment(db.Model):
    __tablename__ = "reply_comment"

    id = Column('id', Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column('text', Text)
    id_main_comment = Column('id_main_comment', Integer)

    id_author_reply = Column('id_author_reply', Integer)
    login_author_reply = Column('login_author_reply', String)
    avatar_author_reply = Column('avatar_author_reply', String)


# Edits to the post
class listRequestEdit(db.Model):
    __tablename__ = "listRequestPost"

    id = Column('id', Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column('text', Text)

    id_post = Column('id_post', Integer)
    title_post = Column('title_post', String)

    id_author = Column('id_author', Integer)