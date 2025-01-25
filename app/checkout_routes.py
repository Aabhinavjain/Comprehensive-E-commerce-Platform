# app/checkout_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Cart, CartItem, Order, OrderItem, db
from .utils import get_or_create_cart

checkout_bp = Blueprint('checkout_bp', __name__)

@checkout_bp.route('/checkout', methods=['GET'])
@login_required
def start_checkout():
    # Show a simple form or summary for the user to confirm
    cart = get_or_create_cart(current_user.id)
    if not cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart_bp.view_cart'))
    return render_template('checkout.html', cart=cart)

@checkout_bp.route('/checkout/confirm', methods=['POST'])
@login_required
def confirm_checkout():
    # In a real scenario, you'd process payment here (e.g., Stripe, PayPal).
    # We'll skip payment and directly convert cart to an order.

    cart = get_or_create_cart(current_user.id)
    if not cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart_bp.view_cart'))

    # Create order
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.flush()  # get order.id before creating items

    total = 0
    for cart_item in cart.items:
        item_price = cart_item.product.price
        quantity = cart_item.quantity
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=quantity,
            price=item_price
        )
        db.session.add(order_item)
        total += item_price * quantity
    
    # Set total and mark status
    order.total_amount = total
    order.status = "Paid"  # or "Pending Payment" if you do a real gateway
    db.session.commit()

    # Clear the cart
    db.session.delete(cart)
    db.session.commit()

    flash(f"Order #{order.id} placed successfully! Total: ${total:.2f}", "success")
    return redirect(url_for('checkout_bp.order_confirmation', order_id=order.id))

@checkout_bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    # ensure user owns this order
    if order.user_id != current_user.id:
        flash("That order doesn't belong to you.", "danger")
        return redirect(url_for('main.home'))
    return render_template('order_confirmation.html', order=order)
