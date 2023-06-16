from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func, Boolean, Text, Date, Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String, nullable=False)
    description = Column(String)
    tags = relationship('Tag', secondary='image_tag')
    comments = relationship('Comment', backref='image')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)

    user = relationship('User', backref="image")
    is_active = Column(Boolean, default=True)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    images = relationship('Image', secondary='image_tag')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    update_status = Column(Boolean, default=False)

    user = relationship('User', backref="comments")
    image = relationship('Image', backref="comments")
# =======
#     image_id = Column(Integer, ForeignKey('images.id'))
#     content = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
# >>>>>>> dev


image_tag = Table(
    'image_tag',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)

    role = Column(String(20), default=UserRole.USER)


class BlacklistToken(Base):
    __tablename__ = 'blacklist_tokens'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String(255), nullable=False)


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    date_of_birth = Column(Date)
    user = relationship('User', backref='profile')


class Qr(Base):
    __tablename__ = "qr"
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship('Image', backref="qr")
    qr_code_url = Column(Text)



class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numbers_rating = Column(Integer)
    text_rating = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="rating")
    image = relationship('Image', backref="rating")


class RatingImage(Base):
    __tablename__ = "rating_image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    now_number_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="rating_image")