
from datetime import datetime

def safe_parse_date(date_str):
    """
    Parse a date string that may or may not include a time portion.

    Args:
        date_str (str): A date string in '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' format

    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return datetime.strptime(date_str, '%Y-%m-%d')
