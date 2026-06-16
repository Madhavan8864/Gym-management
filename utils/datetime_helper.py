from datetime import datetime

def get_current_datetime():
    """Get current datetime as string"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_current_date():
    """Get current date as string"""
    return datetime.now().strftime('%Y-%m-%d')

def get_current_time():
    """Get current time as string"""
    return datetime.now().strftime('%H:%M:%S')

def get_current_month():
    """Get current month number"""
    return datetime.now().month

def get_current_year():
    """Get current year"""
    return datetime.now().year

def format_date(date_str):
    """Format date for display"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d %B %Y')
    except:
        return date_str