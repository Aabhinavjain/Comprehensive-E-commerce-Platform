# app/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length,  EqualTo, NumberRange, URL

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField(
        'Product Name',
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=10)]
    )
    price = FloatField(
        'Price',
        validators=[DataRequired(), NumberRange(min=0.01)]
    )
    image = StringField(
        'Image URL',
        validators=[DataRequired(), URL(), Length(min=5)]
    )
    submit = SubmitField('Add Product')
