# app/admin.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .models import Product, db
from .forms import ProductForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/products')
@login_required
def products_list():
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image=form.image.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.products_list'))
    return render_template('create_product.html', form=form)

@admin_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image = form.image.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products_list'))
    return render_template('edit_product.html', form=form)

@admin_bp.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'info')
    return redirect(url_for('admin.products_list'))
