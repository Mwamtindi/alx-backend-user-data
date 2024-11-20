#!/usr/bin/env python3
"""
Module for defining User model using SQLAlchemy.
This module contains User class, which maps to the users table in the db.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model for the users table.

    Attributes:
        id (int): primary key of the user.
        email (str): email of the user (non-nullable).
        hashed_password (str): hashed pswd of user (non-nullable).
        session_id (str): session ID of the user (nullable).
        reset_token (str): reset token of the user (nullable).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
