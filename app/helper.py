from datetime import datetime

"""
Helper methods to convert date representations.
"""


def format_date(date):
    """Converts a datetime.date object to a date string (YYYY-MM-DD)."""
    return datetime.strftime(date, "%Y-%m-%d")


def to_date(date_string):
    """Converts a date string (YYYY-MM-DD) to a datetime.date object."""
    if date_string is None:
        return None
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        return None
