#!/usr/bin/env python3
"""
Module with fxn filter_datum that filters sensitive info from log messages.
"""

import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with given fields to redact.

        Args:
            fields: List of field names to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record, redacting sensitive info from specified fields.

        Args:
            record: The log record to format.

        Returns:
            The formatted log message with redacted sensitive fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
