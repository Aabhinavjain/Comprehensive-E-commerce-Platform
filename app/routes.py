from flask import Blueprint, render_template
from .models import Product

main = Blueprint('main', __name__)

@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

