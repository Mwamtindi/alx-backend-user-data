#!/usr/bin/env python3
"""
Module with fxn filter_datum that filters sensitive info from log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specific fields in a log message

    Args:
        fields: List of field names to obfuscate.
        redaction: The string used to replace the field values.
        message: The log message containing key-value pairs.
        separator: The separator char btw fields in log message.

    Returns:
        The log message with specified fields obfuscated.
    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
