from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from .models import Product, Cart, CartItem, db
from .utils import get_or_create_cart  # hypothetical helper

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart = get_or_create_cart(current_user.id)
    # We'll show cart items in a cart.html template
    return render_template('cart.html', cart=cart)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart = get_or_create_cart(current_user.id)
    product = Product.query.get_or_404(product_id)

    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('main.product_details', product_id=product_id))

@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_cart_item(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    # Ensure this item belongs to the current user's cart
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart_bp.view_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart_bp.view_cart'))

@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart_bp.view_cart'))

    # parse new quantity from form
    new_quantity = request.form.get('quantity', type=int, default=1)
    if new_quantity < 1:
        new_quantity = 1  # or remove item
    cart_item.quantity = new_quantity
    db.session.commit()
    flash('Item quantity updated.', 'success')
    return redirect(url_for('cart_bp.view_cart'))
