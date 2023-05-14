from datetime import datetime
from db import db
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean


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
    is_admin = Column(Boolean, default=False)


# Posts
class Posts(db.Model):
    __tablename__ = "posts"   

    id = Column("id", Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    title = Column('title', String)
    description = Column("description", Text)
    tag = Column("tag", String)
    image = Column("image", String, nullable=True, default='/images/posts/default_post.jpeg')
    type = Column('type', String)


# Comments for post
class Comments(db.Model):
    __tablename__ = "comments"

    id = Column("id", Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    text = Column('text', Text)
    id_post = Column('id_post', Integer)
    id_author = Column('id_author', Integer)