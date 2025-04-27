#!/usr/bin/env python3
"""
Sample Data Loader for Inventory Management System
This script populates the system with sample categories and products.
"""

import os
import sys
from datetime import datetime

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.inventory_manager import InventoryManager

def load_sample_data():
    """Load sample categories and products into the inventory system"""
    # Initialize the inventory manager
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    manager = InventoryManager(data_dir)
    
    # Sample categories
    categories = [
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Clothing", "description": "Apparel and fashion items"},
        {"name": "Home & Kitchen", "description": "Household items and kitchen appliances"},
        {"name": "Books", "description": "Books, magazines, and publications"},
        {"name": "Toys & Games", "description": "Toys, games, and entertainment items"},
        {"name": "Sports & Outdoors", "description": "Sporting goods and outdoor equipment"},
        {"name": "Health & Beauty", "description": "Personal care and beauty products"},
        {"name": "Office Supplies", "description": "Stationery and office equipment"},
        {"name": "Food & Beverages", "description": "Edible items and drinks"},
        {"name": "Automotive", "description": "Car parts and accessories"}
    ]
    
    # Add categories and store their IDs
    category_ids = {}
    for category_data in categories:
        try:
            # Check if category already exists
            existing_categories = manager.get_all_categories()
            category_exists = False
            
            for existing_category in existing_categories:
                if existing_category.name == category_data["name"]:
                    category_exists = True
                    category_ids[category_data["name"]] = existing_category.category_id
                    print(f"Category already exists: {category_data['name']}")
                    break
            
            if not category_exists:
                category = manager.add_category(
                    name=category_data["name"],
                    description=category_data["description"]
                )
                category_ids[category_data["name"]] = category.category_id
                print(f"Added category: {category_data['name']}")
        except Exception as e:
            print(f"Error adding category {category_data['name']}: {str(e)}")
    
    # Sample products for each category
    products = [
        # Electronics
        {
            "name": "Smartphone", 
            "description": "Latest model smartphone with 128GB storage", 
            "price": 699.99, 
            "quantity": 25, 
            "category": "Electronics"
        },
        {
            "name": "Laptop", 
            "description": "15-inch laptop with 8GB RAM and 512GB SSD", 
            "price": 1099.99, 
            "quantity": 15, 
            "category": "Electronics"
        },
        {
            "name": "Wireless Earbuds", 
            "description": "Bluetooth earbuds with noise cancellation", 
            "price": 129.99, 
            "quantity": 30, 
            "category": "Electronics"
        },
        {
            "name": "Smart Watch", 
            "description": "Fitness tracking smartwatch with heart rate monitor", 
            "price": 199.99, 
            "quantity": 20, 
            "category": "Electronics"
        },
        
        # Clothing
        {
            "name": "T-Shirt", 
            "description": "100% cotton t-shirt, available in multiple colors", 
            "price": 19.99, 
            "quantity": 50, 
            "category": "Clothing"
        },
        {
            "name": "Jeans", 
            "description": "Classic fit denim jeans", 
            "price": 49.99, 
            "quantity": 40, 
            "category": "Clothing"
        },
        {
            "name": "Sweater", 
            "description": "Warm winter sweater made of wool blend", 
            "price": 59.99, 
            "quantity": 30, 
            "category": "Clothing"
        },
        
        # Home & Kitchen
        {
            "name": "Coffee Maker", 
            "description": "Programmable coffee maker with 12-cup capacity", 
            "price": 79.99, 
            "quantity": 15, 
            "category": "Home & Kitchen"
        },
        {
            "name": "Blender", 
            "description": "High-speed blender for smoothies and food processing", 
            "price": 89.99, 
            "quantity": 12, 
            "category": "Home & Kitchen"
        },
        {
            "name": "Bedding Set", 
            "description": "Queen size bedding set with duvet cover and pillowcases", 
            "price": 129.99, 
            "quantity": 20, 
            "category": "Home & Kitchen"
        },
        
        # Books
        {
            "name": "Python Programming", 
            "description": "Comprehensive guide to Python programming", 
            "price": 39.99, 
            "quantity": 25, 
            "category": "Books"
        },
        {
            "name": "Cooking Basics", 
            "description": "Cookbook for beginners with simple recipes", 
            "price": 29.99, 
            "quantity": 20, 
            "category": "Books"
        },
        {
            "name": "Science Fiction Anthology", 
            "description": "Collection of award-winning science fiction stories", 
            "price": 24.99, 
            "quantity": 15, 
            "category": "Books"
        },
        
        # Toys & Games
        {
            "name": "Board Game", 
            "description": "Family-friendly strategy board game", 
            "price": 34.99, 
            "quantity": 18, 
            "category": "Toys & Games"
        },
        {
            "name": "Action Figure", 
            "description": "Collectible superhero action figure", 
            "price": 19.99, 
            "quantity": 30, 
            "category": "Toys & Games"
        },
        {
            "name": "Building Blocks", 
            "description": "Educational building blocks set for children", 
            "price": 49.99, 
            "quantity": 25, 
            "category": "Toys & Games"
        },
        
        # Sports & Outdoors
        {
            "name": "Yoga Mat", 
            "description": "Non-slip yoga mat with carrying strap", 
            "price": 29.99, 
            "quantity": 35, 
            "category": "Sports & Outdoors"
        },
        {
            "name": "Dumbbell Set", 
            "description": "Adjustable dumbbell set with various weights", 
            "price": 149.99, 
            "quantity": 10, 
            "category": "Sports & Outdoors"
        },
        {
            "name": "Camping Tent", 
            "description": "4-person waterproof tent for camping", 
            "price": 199.99, 
            "quantity": 8, 
            "category": "Sports & Outdoors"
        },
        
        # Health & Beauty
        {
            "name": "Facial Cleanser", 
            "description": "Gentle facial cleanser for all skin types", 
            "price": 14.99, 
            "quantity": 40, 
            "category": "Health & Beauty"
        },
        {
            "name": "Hair Dryer", 
            "description": "Professional hair dryer with multiple heat settings", 
            "price": 59.99, 
            "quantity": 15, 
            "category": "Health & Beauty"
        },
        {
            "name": "Vitamin Supplement", 
            "description": "Daily multivitamin supplement, 90 tablets", 
            "price": 19.99, 
            "quantity": 30, 
            "category": "Health & Beauty"
        },
        
        # Office Supplies
        {
            "name": "Notebook", 
            "description": "Spiral-bound notebook with lined pages", 
            "price": 4.99, 
            "quantity": 100, 
            "category": "Office Supplies"
        },
        {
            "name": "Desk Organizer", 
            "description": "Desktop organizer with multiple compartments", 
            "price": 24.99, 
            "quantity": 20, 
            "category": "Office Supplies"
        },
        {
            "name": "Pen Set", 
            "description": "Set of 10 ballpoint pens in various colors", 
            "price": 12.99, 
            "quantity": 50, 
            "category": "Office Supplies"
        },
        
        # Food & Beverages
        {
            "name": "Coffee Beans", 
            "description": "Premium arabica coffee beans, 1lb bag", 
            "price": 14.99, 
            "quantity": 40, 
            "category": "Food & Beverages"
        },
        {
            "name": "Chocolate Assortment", 
            "description": "Assorted chocolate gift box, 24 pieces", 
            "price": 29.99, 
            "quantity": 25, 
            "category": "Food & Beverages"
        },
        {
            "name": "Herbal Tea", 
            "description": "Organic herbal tea variety pack, 48 tea bags", 
            "price": 18.99, 
            "quantity": 35, 
            "category": "Food & Beverages"
        },
        
        # Automotive
        {
            "name": "Car Phone Mount", 
            "description": "Universal car phone mount for dashboard", 
            "price": 19.99, 
            "quantity": 30, 
            "category": "Automotive"
        },
        {
            "name": "Car Vacuum", 
            "description": "Portable car vacuum cleaner with attachments", 
            "price": 49.99, 
            "quantity": 15, 
            "category": "Automotive"
        },
        {
            "name": "Windshield Wipers", 
            "description": "All-season windshield wiper blades, pair", 
            "price": 29.99, 
            "quantity": 25, 
            "category": "Automotive"
        }
    ]
    
    # Add products
    for product_data in products:
        try:
            # Check if product with same name already exists
            existing_products = manager.get_all_products()
            product_exists = False
            
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    product_exists = True
                    print(f"Product already exists: {product_data['name']}")
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
                print(f"Added product: {product_data['name']}")
        except Exception as e:
            print(f"Error adding product {product_data['name']}: {str(e)}")
    
    print("\nSample data loading complete!")
    print(f"{len(category_ids)} categories available")
    print(f"{len(manager.get_all_products())} products available")

if __name__ == "__main__":
    load_sample_data() 