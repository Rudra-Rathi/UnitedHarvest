import datetime
import random
import string

def generate_order_number():
    """Generate a unique order number"""
    prefix = 'UF'
    date_part = datetime.datetime.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{date_part}-{random_part}"

def calculate_commission(total_amount):
    """Calculate the platform commission (5%)"""
    return round(total_amount * 0.05, 2)
