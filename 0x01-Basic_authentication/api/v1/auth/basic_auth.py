#!/usr/bin/env python3
"""
BasicAuth module that inherits from Auth and implements Basic Authentication
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
import base64

User = TypeVar('User')


class BasicAuth(Auth):
    """Basic Authe'n that inherits from Auth and implements Basic Authe'n"""

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Extracts the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]  # Return the part after "Basic "

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decodes Base64 string and returns decoded value as a UTF-8 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extracts the user email and password from decoded Base64 value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_pwd = decoded_base64_authorization_header.split(":",
                                                                         1)
        return user_email, user_pwd

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Returns the User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email using the User class search method
        user = User.search({'email': user_email})
        if not user:
            return None

        # Check the password with the is_valid_password method
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> User:
        """Retrieves the current user based on the request"""
        if request is None:
            return None

        # Extract and decode the Authorization header
        authorization_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header
        (authorization_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve and return the User object
        return self.user_object_from_credentials(user_email, user_pwd)
