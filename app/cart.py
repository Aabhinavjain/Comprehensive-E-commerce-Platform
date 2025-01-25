# app/cart.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, CartItem, Order, OrderItem

cart_bp = Blueprint('cart_bp', __name__, url_prefix='/cart')

@cart_bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += int(quantity)
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=int(quantity))
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.home'))

@cart_bp.route('/view_cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('view_cart.html', cart_items=cart_items)

@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    # Implement checkout logic here
    # For simplicity, we'll just create an order and clear the cart
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart_bp.view_cart'))
    
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.session.add(order_item)
        db.session.delete(item)  # Remove item from cart

    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('main.home'))
