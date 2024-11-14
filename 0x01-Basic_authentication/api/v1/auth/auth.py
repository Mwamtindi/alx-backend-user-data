#!/usr/bin/env python3
"""
Auth module for handling authentication templates
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """A template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required
        Args:
            path (str): the path to check
            excluded_paths: list of paths that do not require auth
        Returns:
            bool: False for now; will be customized later
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure that paths end with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Ensure excluded paths end with slash for comparison
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if path == excluded_path:
                return False  # Path matches an excluded path

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        Args:
            request: the Flask request object
        Returns:
            str: None for now; will be customized later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request
        Args:
            request: the Flask request object
        Returns:
            User: None for now; will be customized later
        """
        return None
