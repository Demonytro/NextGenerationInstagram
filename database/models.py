from sqlalchemy import Boolean, Column, func, DateTime, Integer, String, Date, ForeignKey
from database.db import Base, engine
from sqlalchemy.orm import relationship


class Image(Base):
    __tablename__ = "image"

    id = Column('id', Integer, primary_key=True, index=True)
    picture = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contact")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)