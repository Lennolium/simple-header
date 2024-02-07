#!/usr/bin/env python3

"""
exceptions.py: Implement custom exceptions for simple-header package.

This module provides custom exceptions for the simple-header package.
The exceptions are used to raise errors in the package's classes and
methods. The exceptions are derived from the base Exception class.
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "simple-header@lennolium.dev"
__license__ = "GNU GPLv3"
__version__ = "0.1.0"
__date__ = "2024-02-07"
__status__ = "Development"
__github__ = "https://github.com/Lennolium/simple-header"


# Imports.
class SimpleHeaderException(Exception):
    """
    Base exception class for simple-header package.
    """


class InvalidURLError(SimpleHeaderException):
    """
    Raise an exception for invalid URLs passed to the Header instance
    while initialization.
    """


class TemplateNotFoundError(SimpleHeaderException):
    """
    Raise an exception for missing templates in the data folder.
    """
