from db import db
from sqlalchemy import Column, String, Integer, DateTime, Text


# Columnt posts
class Posts(db.Model):
    __tablename__ = "posts"   

    id = Column("id", Integer, primary_key=True)
    date = Column("date", DateTime)
    title_posts = Column('title_posts', String)
    description_posts = Column("description_posts", Text)
    tag_posts = Column("tag_posts", String)

    
# Column accounts for users
class Accounts_Users(db.Model):
    """Allow users to leave comments under posts"""

    __tablename__ = "accounts"   

    id = Column("id", Integer, primary_key=True, nullable=False)
    login = Column('login', String(25), nullable=False)
    email = Column("emai", String(25), nullable=False)
    password = Column("password", String, nullable=False)
    img_avatar = Column("avatar", String, nullable=True)