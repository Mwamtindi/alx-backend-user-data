#!/usr/bin/env python3
"""
A module for securely hashing passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with automatic salting.

    Args:
        password: The plain text password to hash.

    Returns:
        The hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that provided password matches the hashed password.

    Args:
        hashed_password: The hashed password to validate against.
        password: The plain text password to check.

    Returns:
        True if psswd matches the hashed passwd, otherwise False.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
