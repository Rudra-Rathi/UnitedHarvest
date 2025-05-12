from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRole(enum.Enum):
    FARMER = 'farmer'
    VENDOR = 'vendor'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    preferred_language = db.Column(db.String(10), default='en')

    # Relationships
    farmer = db.relationship('Farmer', backref='user', uselist=False, cascade='all, delete-orphan')
    vendor = db.relationship('Vendor', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    farm_name = db.Column(db.String(128), nullable=False)
    license_number = db.Column(db.String(64), nullable=False)
    license_image_path = db.Column(db.String(256))
    address = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    products = db.relationship('Product', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    reviews_received = db.relationship('Review', foreign_keys='Review.farmer_id', backref='farmer_reviewed', lazy='dynamic')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', 
                                    primaryjoin="and_(Review.reviewer_id==Farmer.user_id, Review.reviewer_type=='farmer')",
                                    backref='farmer_reviewer', lazy='dynamic')
    
    def __repr__(self):
        return f'<Farmer {self.farm_name}>'

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_name = db.Column(db.String(128), nullable=False)
    business_type = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    orders = db.relationship('Order', backref='vendor', lazy='dynamic', cascade='all, delete-orphan')
    reviews_received = db.relationship('Review', foreign_keys='Review.vendor_id', backref='vendor_reviewed', lazy='dynamic')
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', 
                                    primaryjoin="and_(Review.reviewer_id==Vendor.user_id, Review.reviewer_type=='vendor')",
                                    backref='vendor_reviewer', lazy='dynamic')
    
    def __repr__(self):
        return f'<Vendor {self.business_name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price_per_kg = db.Column(db.Float, nullable=False)
    available_quantity = db.Column(db.Float, nullable=False)  # in kg
    unit = db.Column(db.String(20), default='kg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)
    
    # Relationships
    price_history = db.relationship('PriceHistory', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PriceHistory {self.product_id} {self.date}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    status = db.Column(db.String(20), default='pending_approval', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_amount = db.Column(db.Float, default=0.0)
    commission_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, default=0.0)
    delivery_address = db.Column(db.String(256))
    delivery_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    negotiations = db.relationship('Negotiation', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # in kg
    price_per_kg = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

class Negotiation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    proposed_price = db.Column(db.Float, nullable=False)
    counter_price = db.Column(db.Float)
    round_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, accepted, rejected, countered
    vendor_note = db.Column(db.Text)
    farmer_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Negotiation {self.id}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer_type = db.Column(db.String(10), nullable=False)  # 'farmer' or 'vendor'
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}>'
