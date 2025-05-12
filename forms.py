from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, BooleanField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    role = SelectField('I am a', choices=[('farmer', 'Farmer'), ('vendor', 'Vendor')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class FarmerVerificationForm(FlaskForm):
    license_number = StringField('License Number', validators=[DataRequired()])
    license_image = FileField('Upload License Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Submit for Verification')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('fruit', 'Fruit'), ('vegetable', 'Vegetable')], validators=[DataRequired()])
    description = TextAreaField('Description')
    price_per_kg = FloatField('Price per kg (₹)', validators=[DataRequired(), NumberRange(min=0.1)])
    available_quantity = FloatField('Available Quantity (kg)', validators=[DataRequired(), NumberRange(min=1)])
    is_available = BooleanField('Available for Order')
    submit = SubmitField('Save Product')

class OrderForm(FlaskForm):
    quantity = FloatField('Quantity (kg)', validators=[DataRequired(), NumberRange(min=200, message="Minimum order quantity is 200kg")])
    proposed_price = FloatField('Proposed Price per kg (₹)', validators=[DataRequired(), NumberRange(min=0.1)])
    message = TextAreaField('Message to Farmer')
    submit = SubmitField('Place Order Request')

class NegotiationForm(FlaskForm):
    proposed_price = FloatField('Counter Offer Price per kg (₹)', validators=[DataRequired(), NumberRange(min=0.1)])
    message = TextAreaField('Message')
    submit = SubmitField('Send Counter Offer')

class AcceptRejectForm(FlaskForm):
    action = HiddenField('Action', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review')
    submit = SubmitField('Submit Rating')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
