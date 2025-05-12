from app import app, db
from models import User, Product
import os

# Create test users (farmer and vendor)
def create_test_data():
    with app.app_context():
        # Check if test users already exist
        test_farmer = User.query.filter_by(email='farmer@example.com').first()
        test_vendor = User.query.filter_by(email='vendor@example.com').first()
        
        if not test_farmer:
            # Create a test farmer
            farmer = User(
                username='testfarmer',
                email='farmer@example.com',
                full_name='Test Farmer',
                phone='9876543210',
                address='123 Farm Road, Agricultural District, Delhi',
                role='farmer',
                is_verified=True
            )
            farmer.set_password('password123')
            db.session.add(farmer)
            print("Created test farmer account")
            
            # Add some test products for the farmer
            if farmer.id:
                products = [
                    Product(
                        farmer_id=farmer.id,
                        name='Fresh Tomatoes',
                        category='vegetable',
                        description='Organic farm-fresh tomatoes',
                        price_per_kg=35.0,
                        available_quantity=500.0,
                        is_available=True
                    ),
                    Product(
                        farmer_id=farmer.id,
                        name='Premium Apples',
                        category='fruit',
                        description='Sweet and juicy apples from the hills',
                        price_per_kg=75.0,
                        available_quantity=300.0,
                        is_available=True
                    )
                ]
                db.session.add_all(products)
                print("Added test products for farmer")
        
        if not test_vendor:
            # Create a test vendor
            vendor = User(
                username='testvendor',
                email='vendor@example.com',
                full_name='Test Vendor',
                phone='9876543211',
                address='456 Market Street, Commercial Zone, Mumbai',
                role='vendor'
            )
            vendor.set_password('password123')
            db.session.add(vendor)
            print("Created test vendor account")
        
        db.session.commit()
        print("Test data creation complete")

if __name__ == '__main__':
    create_test_data()