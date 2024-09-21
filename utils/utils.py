import re


def is_valid_price_format(price):
    """Check if given price has a valid format '0,00€', '23,65 €', '10.99$', etc."""
    if not price:
        return False
    pattern = r"^\d+[\.,]?\d*\s?[€$]$"
    return bool(re.match(pattern, price.strip()))
