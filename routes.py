import os
import secrets
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from models import (User, FarmerVerification, Product, ProductPriceHistory, 
                   Order, OrderItem, Negotiation, Rating)
from forms import (LoginForm, RegistrationForm, FarmerVerificationForm, 
                  ProductForm, OrderForm, NegotiationForm, AcceptRejectForm, 
                  RatingForm, ContactForm)
from utils import generate_order_number, calculate_commission

# Home page
@app.route('/')
def index():
    return render_template('index.html', title='Welcome to United Farms')

# User Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'farmer':
            return redirect(url_for('farmer_dashboard'))
        else:
            return redirect(url_for('vendor_dashboard'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            
            # Check if farmer is verified
            if user.role == 'farmer' and not user.is_verified:
                # Check if verification is pending
                verification = FarmerVerification.query.filter_by(user_id=user.id).first()
                if verification:
                    flash('Your account verification is pending. You will be notified once approved.', 'info')
                else:
                    return redirect(url_for('farmer_verification'))
            
            if user.role == 'farmer':
                return redirect(next_page or url_for('farmer_dashboard'))
            else:
                return redirect(next_page or url_for('vendor_dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            address=form.address.data,
            role=form.role.data,
            is_verified=False if form.role.data == 'farmer' else True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        if form.role.data == 'farmer':
            flash('Account created! Please complete verification to activate your account.', 'success')
            login_user(user)
            return redirect(url_for('farmer_verification'))
        else:
            flash('Account created! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Farmer Verification
@app.route('/farmer-verification', methods=['GET', 'POST'])
@login_required
def farmer_verification():
    if current_user.role != 'farmer':
        flash('Only farmers need verification.', 'warning')
        return redirect(url_for('index'))
        
    if current_user.is_verified:
        flash('Your account is already verified.', 'info')
        return redirect(url_for('farmer_dashboard'))
        
    # Check if verification is already submitted
    existing_verification = FarmerVerification.query.filter_by(user_id=current_user.id).first()
    if existing_verification:
        flash('Your verification is currently under review.', 'info')
        return redirect(url_for('farmer_dashboard'))
        
    form = FarmerVerificationForm()
    if form.validate_on_submit():
        # Save the license image
        if form.license_image.data:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.license_image.data.filename)
            filename = random_hex + f_ext
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.license_image.data.save(filepath)
            
            verification = FarmerVerification(
                user_id=current_user.id,
                license_number=form.license_number.data,
                license_image_path=filename,
                status='pending'
            )
            db.session.add(verification)
            db.session.commit()
            
            flash('Verification submitted successfully! We will review your application shortly.', 'success')
            return redirect(url_for('farmer_dashboard'))
    
    return render_template('farmer_verification.html', title='Farmer Verification', form=form)

# Dashboards
@app.route('/farmer-dashboard')
@login_required
def farmer_dashboard():
    if current_user.role != 'farmer':
        flash('Access denied. You are not registered as a farmer.', 'danger')
        return redirect(url_for('index'))
        
    # Get farmer's products
    products = Product.query.filter_by(farmer_id=current_user.id).all()
    
    # Get recent orders
    orders = Order.query.filter_by(farmer_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    
    # Get pending negotiations
    pending_negotiations = db.session.query(Order, Negotiation)\
        .join(Negotiation, Order.id == Negotiation.order_id)\
        .filter(Order.farmer_id == current_user.id, 
                Negotiation.status == 'pending',
                Negotiation.proposed_by == 'vendor')\
        .order_by(Negotiation.created_at.desc()).all()
    
    return render_template('farmer_dashboard.html', 
                          title='Farmer Dashboard',
                          products=products,
                          orders=orders,
                          pending_negotiations=pending_negotiations)

@app.route('/vendor-dashboard')
@login_required
def vendor_dashboard():
    if current_user.role != 'vendor':
        flash('Access denied. You are not registered as a vendor.', 'danger')
        return redirect(url_for('index'))
    
    # Get recent orders
    orders = Order.query.filter_by(vendor_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    
    # Get pending negotiations
    pending_negotiations = db.session.query(Order, Negotiation)\
        .join(Negotiation, Order.id == Negotiation.order_id)\
        .filter(Order.vendor_id == current_user.id, 
                Negotiation.status == 'pending',
                Negotiation.proposed_by == 'farmer')\
        .order_by(Negotiation.created_at.desc()).all()
    
    # Get available products
    available_products = Product.query.filter_by(is_available=True).order_by(Product.updated_at.desc()).limit(10).all()
    
    return render_template('vendor_dashboard.html',
                          title='Vendor Dashboard',
                          orders=orders,
                          pending_negotiations=pending_negotiations,
                          available_products=available_products)

# Product Management
@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.role != 'farmer':
        flash('Only farmers can add products.', 'danger')
        return redirect(url_for('index'))
        
    if not current_user.is_verified:
        flash('Your account needs to be verified before adding products.', 'warning')
        return redirect(url_for('farmer_dashboard'))
        
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            farmer_id=current_user.id,
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            price_per_kg=form.price_per_kg.data,
            available_quantity=form.available_quantity.data,
            is_available=form.is_available.data
        )
        db.session.add(product)
        db.session.commit()
        
        # Create initial price history
        price_history = ProductPriceHistory(
            product_id=product.id,
            price=form.price_per_kg.data
        )
        db.session.add(price_history)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('farmer_dashboard'))
        
    return render_template('product_listing.html', title='Add New Product', form=form, product=None)

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.farmer_id != current_user.id:
        abort(403)
        
    form = ProductForm()
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.category = form.category.data
        product.description = form.description.data
        
        # Check if price has changed
        if product.price_per_kg != form.price_per_kg.data:
            # Create new price history entry
            price_history = ProductPriceHistory(
                product_id=product.id,
                price=form.price_per_kg.data
            )
            db.session.add(price_history)
            product.price_per_kg = form.price_per_kg.data
            
        product.available_quantity = form.available_quantity.data
        product.is_available = form.is_available.data
        product.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('farmer_dashboard'))
        
    elif request.method == 'GET':
        form.name.data = product.name
        form.category.data = product.category
        form.description.data = product.description
        form.price_per_kg.data = product.price_per_kg
        form.available_quantity.data = product.available_quantity
        form.is_available.data = product.is_available
        
    return render_template('product_listing.html', title='Edit Product', form=form, product=product)

@app.route('/products')
@login_required
def browse_products():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_available=True)
    
    if category:
        query = query.filter_by(category=category)
        
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%') | 
                            Product.description.ilike(f'%{search}%'))
                            
    products = query.order_by(Product.updated_at.desc()).all()
    
    return render_template('product_listing.html', 
                          title='Browse Products', 
                          products=products,
                          category=category,
                          search=search)

# Order Management
@app.route('/products/<int:product_id>/order', methods=['GET', 'POST'])
@login_required
def place_order(product_id):
    if current_user.role != 'vendor':
        flash('Only vendors can place orders.', 'danger')
        return redirect(url_for('index'))
        
    product = Product.query.get_or_404(product_id)
    
    if not product.is_available:
        flash('This product is currently unavailable.', 'warning')
        return redirect(url_for('browse_products'))
        
    form = OrderForm()
    if form.validate_on_submit():
        if form.quantity.data > product.available_quantity:
            flash(f'Only {product.available_quantity}kg available for this product.', 'danger')
            return redirect(url_for('place_order', product_id=product_id))
            
        order_number = generate_order_number()
        total_amount = form.quantity.data * form.proposed_price.data
        commission_amount = calculate_commission(total_amount)
        farmer_payout = total_amount - commission_amount
        
        # Create order
        order = Order(
            order_number=order_number,
            vendor_id=current_user.id,
            farmer_id=product.farmer_id,
            total_amount=total_amount,
            commission_amount=commission_amount,
            farmer_payout=farmer_payout,
            status='negotiating'
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=form.quantity.data,
            unit_price=form.proposed_price.data,
            total_price=total_amount
        )
        db.session.add(order_item)
        
        # Create initial negotiation
        negotiation = Negotiation(
            order_id=order.id,
            proposed_by='vendor',
            proposed_price=form.proposed_price.data,
            message=form.message.data,
            status='pending'
        )
        db.session.add(negotiation)
        db.session.commit()
        
        flash('Order placed successfully! Waiting for farmer response.', 'success')
        return redirect(url_for('order_details', order_id=order.id))
        
    # Prefill proposed price with product price
    if request.method == 'GET':
        form.proposed_price.data = product.price_per_kg
        
    return render_template('negotiation.html', 
                          title='Place Order', 
                          form=form, 
                          product=product,
                          action='place_order')

@app.route('/orders/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if current user is either the farmer or vendor of this order
    if order.farmer_id != current_user.id and order.vendor_id != current_user.id:
        abort(403)
        
    # Get order items
    items = OrderItem.query.filter_by(order_id=order.id).all()
    
    # Get negotiations
    negotiations = Negotiation.query.filter_by(order_id=order.id).order_by(Negotiation.created_at).all()
    
    # Get farmer and vendor info
    farmer = User.query.get(order.farmer_id)
    vendor = User.query.get(order.vendor_id)
    
    # Check if rating exists
    user_rating = None
    if order.status == 'completed':
        user_rating = Rating.query.filter_by(
            order_id=order.id,
            rater_id=current_user.id
        ).first()
    
    # Prepare negotiation form if needed
    negotiation_form = NegotiationForm()
    accept_reject_form = AcceptRejectForm()
    rating_form = RatingForm()
    
    # Count negotiations from each side
    vendor_negotiations = Negotiation.query.filter_by(
        order_id=order.id, 
        proposed_by='vendor'
    ).count()
    
    farmer_negotiations = Negotiation.query.filter_by(
        order_id=order.id, 
        proposed_by='farmer'
    ).count()
    
    # Check if negotiation limit reached
    can_negotiate = True
    if (current_user.role == 'vendor' and vendor_negotiations >= 3) or \
       (current_user.role == 'farmer' and farmer_negotiations >= 3):
        can_negotiate = False
    
    return render_template('order_details.html',
                          title=f'Order #{order.order_number}',
                          order=order,
                          items=items,
                          negotiations=negotiations,
                          farmer=farmer,
                          vendor=vendor,
                          negotiation_form=negotiation_form,
                          accept_reject_form=accept_reject_form,
                          rating_form=rating_form,
                          can_negotiate=can_negotiate,
                          user_rating=user_rating)

@app.route('/orders/<int:order_id>/negotiate', methods=['POST'])
@login_required
def negotiate_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if current user is either the farmer or vendor of this order
    if order.farmer_id != current_user.id and order.vendor_id != current_user.id:
        abort(403)
        
    # Check if order is still in negotiating state
    if order.status != 'negotiating':
        flash('This order is no longer in negotiation.', 'warning')
        return redirect(url_for('order_details', order_id=order.id))
    
    form = NegotiationForm()
    if form.validate_on_submit():
        proposed_by = current_user.role
        
        # Count negotiations from current user
        negotiation_count = Negotiation.query.filter_by(
            order_id=order.id, 
            proposed_by=proposed_by
        ).count()
        
        # Check if negotiation limit reached
        if negotiation_count >= 3:
            flash('You have reached the maximum number of negotiation attempts.', 'warning')
            return redirect(url_for('order_details', order_id=order.id))
            
        # Create new negotiation
        negotiation = Negotiation(
            order_id=order.id,
            proposed_by=proposed_by,
            proposed_price=form.proposed_price.data,
            message=form.message.data,
            status='pending'
        )
        db.session.add(negotiation)
        
        # Update latest negotiation from other party to 'rejected'
        latest_negotiation = Negotiation.query.filter_by(
            order_id=order.id,
            proposed_by='vendor' if proposed_by == 'farmer' else 'farmer',
            status='pending'
        ).order_by(Negotiation.created_at.desc()).first()
        
        if latest_negotiation:
            latest_negotiation.status = 'rejected'
            latest_negotiation.responded_at = datetime.utcnow()
            
        db.session.commit()
        
        flash('Counter offer sent successfully!', 'success')
        return redirect(url_for('order_details', order_id=order.id))
        
    return redirect(url_for('order_details', order_id=order.id))

@app.route('/orders/<int:order_id>/respond', methods=['POST'])
@login_required
def respond_to_negotiation(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if current user is either the farmer or vendor of this order
    if order.farmer_id != current_user.id and order.vendor_id != current_user.id:
        abort(403)
        
    # Check if order is still in negotiating state
    if order.status != 'negotiating':
        flash('This order is no longer in negotiation.', 'warning')
        return redirect(url_for('order_details', order_id=order.id))
    
    form = AcceptRejectForm()
    if form.validate_on_submit():
        # Get the latest negotiation from the other party
        latest_negotiation = Negotiation.query.filter_by(
            order_id=order.id,
            proposed_by='vendor' if current_user.role == 'farmer' else 'farmer',
            status='pending'
        ).order_by(Negotiation.created_at.desc()).first()
        
        if not latest_negotiation:
            flash('No pending negotiation to respond to.', 'warning')
            return redirect(url_for('order_details', order_id=order.id))
            
        action = form.action.data
        if action == 'accept':
            latest_negotiation.status = 'accepted'
            latest_negotiation.responded_at = datetime.utcnow()
            
            # Update order with the accepted price
            for item in order.items:
                item.unit_price = latest_negotiation.proposed_price
                item.total_price = item.quantity * latest_negotiation.proposed_price
                
            order.total_amount = sum(item.total_price for item in order.items)
            order.commission_amount = calculate_commission(order.total_amount)
            order.farmer_payout = order.total_amount - order.commission_amount
            order.status = 'accepted'
            
            # Update product available quantity
            for item in order.items:
                product = Product.query.get(item.product_id)
                product.available_quantity -= item.quantity
                if product.available_quantity <= 0:
                    product.is_available = False
                    
            flash('Order accepted! Payment processing will begin.', 'success')
            
        elif action == 'reject':
            latest_negotiation.status = 'rejected'
            latest_negotiation.responded_at = datetime.utcnow()
            
            # Count negotiations from both sides
            vendor_negotiations = Negotiation.query.filter_by(
                order_id=order.id, 
                proposed_by='vendor'
            ).count()
            
            farmer_negotiations = Negotiation.query.filter_by(
                order_id=order.id, 
                proposed_by='farmer'
            ).count()
            
            # Check if both parties have reached negotiation limit
            if (vendor_negotiations >= 3 and farmer_negotiations >= 3) or \
               (current_user.role == 'farmer' and vendor_negotiations >= 3) or \
               (current_user.role == 'vendor' and farmer_negotiations >= 3):
                order.status = 'rejected'
                flash('Negotiation ended. The order has been rejected.', 'info')
            else:
                flash('Offer rejected. You can submit a counter offer.', 'info')
                
        db.session.commit()
        
    return redirect(url_for('order_details', order_id=order.id))

@app.route('/orders/<int:order_id>/complete', methods=['POST'])
@login_required
def complete_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Only admin or system would typically do this
    # For now, both farmer and vendor can mark as completed
    if order.farmer_id != current_user.id and order.vendor_id != current_user.id:
        abort(403)
        
    if order.status != 'accepted':
        flash('Only accepted orders can be marked as completed.', 'warning')
        return redirect(url_for('order_details', order_id=order.id))
        
    order.status = 'completed'
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Order marked as completed! Please rate your experience.', 'success')
    return redirect(url_for('order_details', order_id=order.id))

@app.route('/orders/<int:order_id>/rate', methods=['POST'])
@login_required
def rate_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if current user is either the farmer or vendor of this order
    if order.farmer_id != current_user.id and order.vendor_id != current_user.id:
        abort(403)
        
    if order.status != 'completed':
        flash('Only completed orders can be rated.', 'warning')
        return redirect(url_for('order_details', order_id=order.id))
    
    # Check if user already rated this order
    existing_rating = Rating.query.filter_by(
        order_id=order.id,
        rater_id=current_user.id
    ).first()
    
    if existing_rating:
        flash('You have already rated this order.', 'warning')
        return redirect(url_for('order_details', order_id=order.id))
    
    form = RatingForm()
    if form.validate_on_submit():
        # Determine who is being rated
        ratee_id = order.farmer_id if current_user.id == order.vendor_id else order.vendor_id
        
        rating = Rating(
            rater_id=current_user.id,
            ratee_id=ratee_id,
            order_id=order.id,
            rating=form.rating.data,
            review=form.review.data
        )
        db.session.add(rating)
        db.session.commit()
        
        flash('Thank you for your rating!', 'success')
        
    return redirect(url_for('order_details', order_id=order.id))

# Market Trends
@app.route('/daily-mandi')
@login_required
def daily_mandi():
    category = request.args.get('category', '')
    
    # Get all products with their price history
    query = db.session.query(Product)
    
    if category:
        query = query.filter_by(category=category)
        
    products = query.all()
    
    # For each product, get its price history
    product_data = []
    for product in products:
        price_history = ProductPriceHistory.query.filter_by(product_id=product.id).order_by(ProductPriceHistory.date).all()
        
        dates = [history.date.strftime('%Y-%m-%d') for history in price_history]
        prices = [history.price for history in price_history]
        
        product_data.append({
            'id': product.id,
            'name': product.name,
            'farmer_id': product.farmer_id,
            'farmer_name': User.query.get(product.farmer_id).full_name,
            'current_price': product.price_per_kg,
            'dates': dates,
            'prices': prices
        })
    
    return render_template('daily_mandi.html',
                          title='Daily Mandi - Price Trends',
                          products=product_data,
                          category=category)

# Ratings and Reviews
@app.route('/ratings')
@login_required
def ratings():
    # Get ratings received by current user
    received_ratings = Rating.query.filter_by(ratee_id=current_user.id).order_by(Rating.created_at.desc()).all()
    
    # Get ratings given by current user
    given_ratings = Rating.query.filter_by(rater_id=current_user.id).order_by(Rating.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = 0
    if received_ratings:
        avg_rating = sum(r.rating for r in received_ratings) / len(received_ratings)
    
    return render_template('ratings.html',
                          title='Ratings & Reviews',
                          received_ratings=received_ratings,
                          given_ratings=given_ratings,
                          avg_rating=avg_rating)

# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='My Profile')

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # In a real app, send email here
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', title='Contact Us', form=form)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, message='Page not found'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, message='Forbidden'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, message='Server error'), 500
