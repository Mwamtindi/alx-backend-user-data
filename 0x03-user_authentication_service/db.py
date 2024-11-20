#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email : The user's email address.
            hashed_password : The hashed password for the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

     def find_user_by(self, **kwargs) -> User:
         """
        Finds a user in the db based on keyword arguments.

        Args:
            kwargs: Arbitrary keyword arguments to filter query.

        Returns:
            User: The first user matching the query.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If query arguments are invalid.
        """
        if not kwargs:
            raise InvalidRequestError("No query arguments provided.")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found matching the criteria.")
        except Exception as e:
            raise InvalidRequestError(f"Invalid query arguments: {e}")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arb keyword arg's rep user att's to update.

        Returns:
            None

        Raises:
            ValueError: If an attr doesn't correspond to User att.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist on User.")
            setattr(user, key, value)

        self._session.commit()
