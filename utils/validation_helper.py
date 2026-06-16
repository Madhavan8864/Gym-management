import re

def validate_email(email):
    """Validate email address"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    if not phone:
        return False
    return re.match(r'^[0-9]{10}$', phone) is not None

def validate_name(name):
    """Validate name (at least 2 characters, letters only)"""
    if not name:
        return False
    return len(name) >= 2 and name.replace(' ', '').isalpha()

def validate_amount(amount):
    """Validate amount is positive number"""
    try:
        return float(amount) > 0
    except:
        return False