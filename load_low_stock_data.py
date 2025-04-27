#!/usr/bin/env python3
"""
Low Stock Sample Data Loader for Inventory Management System
This script adds some products with low stock quantities to demonstrate the low stock alert feature.
"""

import os
import sys
from datetime import datetime

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.inventory_manager import InventoryManager
from load_sample_data import load_sample_data

def load_low_stock_data():
    """Load products with low stock for demonstration"""
    # First ensure we have regular sample data
    load_sample_data()
    
    # Initialize the inventory manager
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    manager = InventoryManager(data_dir)
    
    # Get all categories
    categories = manager.get_all_categories()
    if not categories:
        print("No categories found. Please run load_sample_data.py first.")
        return
    
    # Map category names to IDs
    category_ids = {}
    for category in categories:
        category_ids[category.name] = category.category_id
    
    # Low stock products
    low_stock_products = [
        {
            "name": "Graphics Card", 
            "description": "High-performance gaming graphics card", 
            "price": 499.99, 
            "quantity": 2, 
            "category": "Electronics"
        },
        {
            "name": "Designer Handbag", 
            "description": "Luxury designer handbag, limited edition", 
            "price": 1299.99, 
            "quantity": 3, 
            "category": "Clothing"
        },
        {
            "name": "Espresso Machine", 
            "description": "Professional-grade espresso machine for home use", 
            "price": 649.99, 
            "quantity": 4, 
            "category": "Home & Kitchen"
        },
        {
            "name": "Collector's Edition Book", 
            "description": "Rare collector's edition book, signed by the author", 
            "price": 149.99, 
            "quantity": 1, 
            "category": "Books"
        },
        {
            "name": "Limited Edition Board Game", 
            "description": "Limited edition strategy board game", 
            "price": 79.99, 
            "quantity": 2, 
            "category": "Toys & Games"
        },
        {
            "name": "Professional Tennis Racket", 
            "description": "Professional-grade tennis racket used by top players", 
            "price": 199.99, 
            "quantity": 3, 
            "category": "Sports & Outdoors"
        },
        {
            "name": "Premium Perfume", 
            "description": "Luxury perfume, 100ml bottle", 
            "price": 129.99, 
            "quantity": 5, 
            "category": "Health & Beauty"
        },
        {
            "name": "Luxury Pen", 
            "description": "Premium fountain pen with gold nib", 
            "price": 89.99, 
            "quantity": 4, 
            "category": "Office Supplies"
        },
        {
            "name": "Rare Coffee Beans", 
            "description": "Single-origin rare coffee beans, 250g", 
            "price": 49.99, 
            "quantity": 2, 
            "category": "Food & Beverages"
        },
        {
            "name": "Premium Car Cover", 
            "description": "Weather-resistant premium car cover", 
            "price": 159.99, 
            "quantity": 3, 
            "category": "Automotive"
        }
    ]
    
    # Add low stock products
    for product_data in low_stock_products:
        try:
            # Check if product with same name already exists
            existing_products = manager.get_all_products()
            product_exists = False
            
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    product_exists = True
                    print(f"Product already exists: {product_data['name']}")
                    
                    # Update to low quantity if it exists
                    manager.update_product(
                        existing_product.product_id, 
                        quantity=product_data["quantity"]
                    )
                    print(f"Updated {product_data['name']} to low stock: {product_data['quantity']} units")
                    break
            
            if not product_exists:
                # Get category ID
                category_name = product_data.pop("category")
                category_id = category_ids.get(category_name)
                
                if not category_id:
                    print(f"Category not found for product {product_data['name']}")
                    continue
                
                # Add product
                product = manager.add_product(
                    **product_data,
                    category=category_id
                )
                print(f"Added low stock product: {product_data['name']} ({product_data['quantity']} units)")
        except Exception as e:
            print(f"Error adding/updating product {product_data['name']}: {str(e)}")
    
    # Get all products with low stock (5 or fewer)
    low_stock = manager.get_low_stock_products(5)
    print(f"\nLow stock loading complete! {len(low_stock)} products with 5 or fewer units in stock.")

if __name__ == "__main__":
    load_low_stock_data() 