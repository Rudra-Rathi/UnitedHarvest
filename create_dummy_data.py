import random
from datetime import datetime, timedelta
from app import app, db
from models import User, FarmerVerification, Product, ProductPriceHistory, Order, OrderItem, Negotiation, Rating

def create_dummy_users():
    users = []
    for i in range(5):
        user = User(
            username=f'farmer{i}',
            email=f'farmer{i}@example.com',
            full_name=f'Farmer {i}',
            phone=f'900000000{i}',
            address=f'Village {i}, India',
            role='farmer',
            is_verified=True
        )
        user.set_password('password')
        users.append(user)
    for i in range(5):
        user = User(
            username=f'vendor{i}',
            email=f'vendor{i}@example.com',
            full_name=f'Vendor {i}',
            phone=f'800000000{i}',
            address=f'City {i}, India',
            role='vendor',
            is_verified=True
        )
        user.set_password('password')
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    return users

def create_dummy_verifications(farmers):
    verifications = []
    for farmer in farmers:
        verification = FarmerVerification(
            user_id=farmer.id,
            license_number=f'LIC-{farmer.id:04d}',
            license_image_path='dummy_license.jpg',
            status='approved',
            created_at=datetime.utcnow() - timedelta(days=30),
            reviewed_at=datetime.utcnow() - timedelta(days=15),
            reviewer_notes='Verified successfully'
        )
        verifications.append(verification)
    db.session.add_all(verifications)
    db.session.commit()

def create_dummy_products(farmers):
    categories = ['fruit', 'vegetable']
    products = []
    for i in range(10):
        farmer = random.choice(farmers)
        product = Product(
            farmer_id=farmer.id,
            name=f'Product {i}',
            category=random.choice(categories),
            description=f'Description for product {i}',
            price_per_kg=round(random.uniform(10, 100), 2),
            available_quantity=round(random.uniform(100, 1000), 2),
            is_available=True,
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.utcnow() - timedelta(days=random.randint(0, 10))
        )
        products.append(product)
    db.session.add_all(products)
    db.session.commit()
    return products

def create_dummy_price_history(products):
    price_histories = []
    for product in products:
        for days_ago in range(10, 0, -1):
            price_history = ProductPriceHistory(
                product_id=product.id,
                price=round(product.price_per_kg * random.uniform(0.8, 1.2), 2),
                date=datetime.utcnow() - timedelta(days=days_ago)
            )
            price_histories.append(price_history)
    db.session.add_all(price_histories)
    db.session.commit()

def create_dummy_orders(vendors, farmers, products):
    orders = []
    order_items = []
    for i in range(10):
        vendor = random.choice(vendors)
        farmer = random.choice(farmers)
        order_number = f'ORD{i:05d}'
        total_amount = 0
        commission_amount = 0
        farmer_payout = 0
        order = Order(
            order_number=order_number,
            vendor_id=vendor.id,
            farmer_id=farmer.id,
            total_amount=0,
            commission_amount=0,
            farmer_payout=0,
            status='completed',
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.utcnow() - timedelta(days=random.randint(0, 10))
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        # Add 1-3 order items
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            product = random.choice(products)
            quantity = round(random.uniform(50, 200), 2)
            unit_price = product.price_per_kg
            total_price = quantity * unit_price
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            order_items.append(order_item)
            total_amount += total_price

        commission_amount = total_amount * 0.05  # 5% commission
        farmer_payout = total_amount - commission_amount

        order.total_amount = total_amount
        order.commission_amount = commission_amount
        order.farmer_payout = farmer_payout

        orders.append(order)

    db.session.add_all(order_items)
    db.session.commit()
    return orders

def create_dummy_negotiations(orders):
    negotiations = []
    for order in orders:
        for i in range(2):
            negotiation = Negotiation(
                order_id=order.id,
                proposed_by='vendor' if i % 2 == 0 else 'farmer',
                proposed_price=round(order.total_amount / random.uniform(50, 200), 2),
                status='accepted' if i == 1 else 'pending',
                message=f'Negotiation message {i}',
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
                responded_at=datetime.utcnow() - timedelta(days=random.randint(0, 5)) if i == 1 else None
            )
            negotiations.append(negotiation)
    db.session.add_all(negotiations)
    db.session.commit()

def create_dummy_ratings(orders, users):
    ratings = []
    for order in orders:
        rater = random.choice(users)
        ratee = order.farmer_id if rater.id != order.farmer_id else order.vendor_id
        rating = Rating(
            rater_id=rater.id,
            ratee_id=ratee,
            order_id=order.id,
            rating=random.randint(3, 5),
            review='Good transaction',
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
        )
        ratings.append(rating)
    db.session.add_all(ratings)
    db.session.commit()

def main():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        users = create_dummy_users()
        farmers = [u for u in users if u.role == 'farmer']
        vendors = [u for u in users if u.role == 'vendor']

        create_dummy_verifications(farmers)
        products = create_dummy_products(farmers)
        create_dummy_price_history(products)
        orders = create_dummy_orders(vendors, farmers, products)
        create_dummy_negotiations(orders)
        create_dummy_ratings(orders, users)

        print("Dummy data created successfully.")

if __name__ == "__main__":
    main()
