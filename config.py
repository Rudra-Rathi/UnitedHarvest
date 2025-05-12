import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///united_farms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    LANGUAGES = ['en', 'hi', 'mr', 'te', 'ta']
    
    # Product categories
    PRODUCT_CATEGORIES = [
        'Vegetables', 
        'Fruits', 
        'Grains', 
        'Dairy', 
        'Poultry', 
        'Others'
    ]
    
    # Order status options
    ORDER_STATUS = [
        'pending_approval',
        'negotiation',
        'approved',
        'rejected',
        'completed',
        'cancelled'
    ]
    
    # Negotiation limit
    MAX_NEGOTIATION_ROUNDS = 3
    
    # Platform commission percentage
    PLATFORM_COMMISSION = 5
    
    # Minimum bulk order quantity (kg)
    MIN_BULK_ORDER_QUANTITY = 200
