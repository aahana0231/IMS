import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

# Add the parent directory to sys.path so we can import the inventory modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.inventory_manager import InventoryManager
from app.models import Product, Category, Transaction

app = Flask(__name__)
app.secret_key = 'inventory_management_secret_key'  # For flash messages and sessions

# Get data directory
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Create inventory manager instance
inventory_manager = InventoryManager(data_dir)

@app.route('/')
def home():
    """Home page with dashboard"""
    products = inventory_manager.get_all_products()
    categories = inventory_manager.get_all_categories()
    low_stock = inventory_manager.get_low_stock_products(5)
    return render_template('index.html', 
                          products=products, 
                          categories=categories, 
                          low_stock=low_stock,
                          product_count=len(products),
                          category_count=len(categories),
                          low_stock_count=len(low_stock))

# Product routes
@app.route('/products')
def list_products():
    """List all products"""
    products = inventory_manager.get_all_products()
    categories = inventory_manager.get_all_categories()
    return render_template('products.html', products=products, categories=categories)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """Add a new product"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
            category = request.form['category']
            
            # Check if category exists
            if not inventory_manager.get_category(category):
                flash(f"Category with ID {category} not found", "danger")
                return redirect(url_for('add_product'))
            
            product = inventory_manager.add_product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                category=category
            )
            
            flash(f"Product '{product.name}' added successfully", "success")
            return redirect(url_for('list_products'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('add_product'))
    
    # GET request: display form
    categories = inventory_manager.get_all_categories()
    return render_template('product_form.html', categories=categories, product=None)

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit an existing product"""
    product = inventory_manager.get_product(product_id)
    if not product:
        flash(f"Product with ID {product_id} not found", "danger")
        return redirect(url_for('list_products'))
    
    if request.method == 'POST':
        try:
            update_data = {}
            if request.form['name']:
                update_data['name'] = request.form['name']
            if request.form['description']:
                update_data['description'] = request.form['description']
            if request.form['price']:
                update_data['price'] = float(request.form['price'])
            if request.form['quantity']:
                update_data['quantity'] = int(request.form['quantity'])
            if request.form['category']:
                category = request.form['category']
                # Check if category exists
                if not inventory_manager.get_category(category):
                    flash(f"Category with ID {category} not found", "danger")
                    return redirect(url_for('edit_product', product_id=product_id))
                update_data['category'] = category
            
            updated_product = inventory_manager.update_product(product_id, **update_data)
            flash(f"Product '{updated_product.name}' updated successfully", "success")
            return redirect(url_for('list_products'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('edit_product', product_id=product_id))
    
    # GET request: display form
    categories = inventory_manager.get_all_categories()
    return render_template('product_form.html', product=product, categories=categories)

@app.route('/products/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    """Delete a product"""
    product = inventory_manager.get_product(product_id)
    if not product:
        flash(f"Product with ID {product_id} not found", "danger")
        return redirect(url_for('list_products'))
    
    if inventory_manager.delete_product(product_id):
        flash(f"Product deleted successfully", "success")
    else:
        flash(f"Failed to delete product", "danger")
    
    return redirect(url_for('list_products'))

@app.route('/products/search')
def search_products():
    """Search for products"""
    term = request.args.get('term', '')
    if not term:
        return redirect(url_for('list_products'))
    
    products = inventory_manager.search_products(term)
    categories = inventory_manager.get_all_categories()
    return render_template('products.html', products=products, categories=categories, search_term=term)

# Category routes
@app.route('/categories')
def list_categories():
    """List all categories"""
    categories = inventory_manager.get_all_categories()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add a new category"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form.get('description', '')
            
            category = inventory_manager.add_category(
                name=name,
                description=description
            )
            
            flash(f"Category '{category.name}' added successfully", "success")
            return redirect(url_for('list_categories'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('add_category'))
    
    # GET request: display form
    return render_template('category_form.html', category=None)

@app.route('/categories/edit/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit an existing category"""
    category = inventory_manager.get_category(category_id)
    if not category:
        flash(f"Category with ID {category_id} not found", "danger")
        return redirect(url_for('list_categories'))
    
    if request.method == 'POST':
        try:
            update_data = {}
            if request.form['name']:
                update_data['name'] = request.form['name']
            if 'description' in request.form:
                update_data['description'] = request.form['description']
            
            updated_category = inventory_manager.update_category(category_id, **update_data)
            flash(f"Category '{updated_category.name}' updated successfully", "success")
            return redirect(url_for('list_categories'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('edit_category', category_id=category_id))
    
    # GET request: display form
    return render_template('category_form.html', category=category)

@app.route('/categories/delete/<category_id>', methods=['POST'])
def delete_category(category_id):
    """Delete a category"""
    category = inventory_manager.get_category(category_id)
    if not category:
        flash(f"Category with ID {category_id} not found", "danger")
        return redirect(url_for('list_categories'))
    
    if inventory_manager.delete_category(category_id):
        flash(f"Category deleted successfully", "success")
    else:
        flash(f"Failed to delete category", "danger")
    
    return redirect(url_for('list_categories'))

# Inventory operations
@app.route('/inventory/add-stock/<product_id>', methods=['GET', 'POST'])
def add_stock(product_id):
    """Add stock to inventory"""
    product = inventory_manager.get_product(product_id)
    if not product:
        flash(f"Product with ID {product_id} not found", "danger")
        return redirect(url_for('list_products'))
    
    if request.method == 'POST':
        try:
            quantity = int(request.form['quantity'])
            user = request.form.get('user', 'Web User')
            
            transaction = inventory_manager.add_stock(
                product_id=product_id,
                quantity=quantity,
                user=user
            )
            
            # Reload product to get updated quantity
            product = inventory_manager.get_product(product_id)
            flash(f"Added {quantity} units to stock. New quantity: {product.quantity}", "success")
            return redirect(url_for('list_products'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('add_stock', product_id=product_id))
    
    # GET request: display form
    return render_template('stock_form.html', product=product, action="add")

@app.route('/inventory/remove-stock/<product_id>', methods=['GET', 'POST'])
def remove_stock(product_id):
    """Remove stock from inventory"""
    product = inventory_manager.get_product(product_id)
    if not product:
        flash(f"Product with ID {product_id} not found", "danger")
        return redirect(url_for('list_products'))
    
    if request.method == 'POST':
        try:
            quantity = int(request.form['quantity'])
            user = request.form.get('user', 'Web User')
            
            if quantity > product.quantity:
                flash(f"Error: Cannot remove {quantity} units. Only {product.quantity} available.", "danger")
                return redirect(url_for('remove_stock', product_id=product_id))
            
            transaction = inventory_manager.remove_stock(
                product_id=product_id,
                quantity=quantity,
                user=user
            )
            
            # Reload product to get updated quantity
            product = inventory_manager.get_product(product_id)
            flash(f"Removed {quantity} units from stock. New quantity: {product.quantity}", "success")
            return redirect(url_for('list_products'))
        except ValueError as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('remove_stock', product_id=product_id))
    
    # GET request: display form
    return render_template('stock_form.html', product=product, action="remove")

# Transaction history
@app.route('/transactions')
def list_transactions():
    """List all transactions"""
    product_id = request.args.get('product_id')
    
    if product_id:
        product = inventory_manager.get_product(product_id)
        if not product:
            flash(f"Product with ID {product_id} not found", "danger")
            return redirect(url_for('list_transactions'))
        
        transactions = inventory_manager.get_transaction_history(product_id)
        title = f"Transaction history for product: {product.name}"
    else:
        transactions = inventory_manager.get_transaction_history()
        title = "All transactions"
    
    return render_template('transactions.html', transactions=transactions, title=title, inventory_manager=inventory_manager)

# Low stock alert
@app.route('/low-stock')
def low_stock():
    """Show products with low stock"""
    threshold = request.args.get('threshold', 10, type=int)
    products = inventory_manager.get_low_stock_products(threshold)
    categories = inventory_manager.get_all_categories()
    return render_template('low_stock.html', products=products, categories=categories, threshold=threshold)

# API endpoints for potential future use with AJAX
@app.route('/api/products', methods=['GET'])
def api_products():
    """API endpoint to get products"""
    products = inventory_manager.get_all_products()
    return jsonify([product.to_dict() for product in products])

@app.route('/api/categories', methods=['GET'])
def api_categories():
    """API endpoint to get categories"""
    categories = inventory_manager.get_all_categories()
    return jsonify([category.to_dict() for category in categories])

@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    """API endpoint to get transactions"""
    product_id = request.args.get('product_id')
    transactions = inventory_manager.get_transaction_history(product_id)
    return jsonify([transaction.to_dict() for transaction in transactions])

if __name__ == '__main__':
    app.run(debug=True, port=5000) 