"""
Custom exceptions.
"""


class AppError(Exception):
    """
    Generic exception for application errors.
    """


class LoadingError(AppError):
    """
    Exception for report loaders errors.
    """
