#!/usr/bin/env python3
""" Module with  Auth method that takes in psswd strings arguments and
returns a byte string.
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import uuid
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ Hashes a given password. """
    return hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates the unique id to be used """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Constructor used """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers, returns new user if email isn't listed. """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if login used is valid. """
        if not email or not password:
            return False
        try:
            users_found = self._db.find_user_by(email=email)
            hashed_password = users_found.hashed_password
            return checkpw(password.encode(),
                           hashed_password.encode('utf-8'))
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """ Creating a new session for any user """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Finds user in the data by session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Updates the user's session_id to None """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a reset password token that can be used """
        try:
            user = self._db.find_user_by(email=email)
            if user.reset_token:
                return user.reset_token
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode('utf-8')
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
