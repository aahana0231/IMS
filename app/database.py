import json
import os
from datetime import datetime
from .models import Product, Category, Transaction

class Database:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.products_file = os.path.join(data_dir, 'products.json')
        self.categories_file = os.path.join(data_dir, 'categories.json')
        self.transactions_file = os.path.join(data_dir, 'transactions.json')
        
        # Initialize data files if they don't exist
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize empty data files if they don't exist"""
        for file_path in [self.products_file, self.categories_file, self.transactions_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def _load_data(self, file_path):
        """Load data from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, file_path, data):
        """Save data to a JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Product operations
    def get_all_products(self):
        """Get all products"""
        products_data = self._load_data(self.products_file)
        return [Product.from_dict(p) for p in products_data]
    
    def get_product_by_id(self, product_id):
        """Get a product by ID"""
        products_data = self._load_data(self.products_file)
        for product_data in products_data:
            if product_data['product_id'] == product_id:
                return Product.from_dict(product_data)
        return None
    
    def add_product(self, product):
        """Add a new product"""
        products_data = self._load_data(self.products_file)
        
        # Check if product ID already exists
        for p in products_data:
            if p['product_id'] == product.product_id:
                raise ValueError(f"Product with ID {product.product_id} already exists")
        
        products_data.append(product.to_dict())
        self._save_data(self.products_file, products_data)
        return product
    
    def update_product(self, product):
        """Update an existing product"""
        products_data = self._load_data(self.products_file)
        
        for i, p in enumerate(products_data):
            if p['product_id'] == product.product_id:
                products_data[i] = product.to_dict()
                self._save_data(self.products_file, products_data)
                return product
        
        raise ValueError(f"Product with ID {product.product_id} not found")
    
    def delete_product(self, product_id):
        """Delete a product by ID"""
        products_data = self._load_data(self.products_file)
        
        for i, p in enumerate(products_data):
            if p['product_id'] == product_id:
                del products_data[i]
                self._save_data(self.products_file, products_data)
                return True
        
        return False
    
    # Category operations
    def get_all_categories(self):
        """Get all categories"""
        categories_data = self._load_data(self.categories_file)
        return [Category.from_dict(c) for c in categories_data]
    
    def get_category_by_id(self, category_id):
        """Get a category by ID"""
        categories_data = self._load_data(self.categories_file)
        for category_data in categories_data:
            if category_data['category_id'] == category_id:
                return Category.from_dict(category_data)
        return None
    
    def add_category(self, category):
        """Add a new category"""
        categories_data = self._load_data(self.categories_file)
        
        # Check if category ID already exists
        for c in categories_data:
            if c['category_id'] == category.category_id:
                raise ValueError(f"Category with ID {category.category_id} already exists")
        
        categories_data.append(category.to_dict())
        self._save_data(self.categories_file, categories_data)
        return category
    
    def update_category(self, category):
        """Update an existing category"""
        categories_data = self._load_data(self.categories_file)
        
        for i, c in enumerate(categories_data):
            if c['category_id'] == category.category_id:
                categories_data[i] = category.to_dict()
                self._save_data(self.categories_file, categories_data)
                return category
        
        raise ValueError(f"Category with ID {category.category_id} not found")
    
    def delete_category(self, category_id):
        """Delete a category by ID"""
        categories_data = self._load_data(self.categories_file)
        
        for i, c in enumerate(categories_data):
            if c['category_id'] == category_id:
                del categories_data[i]
                self._save_data(self.categories_file, categories_data)
                return True
        
        return False
    
    # Transaction operations
    def get_all_transactions(self):
        """Get all transactions"""
        transactions_data = self._load_data(self.transactions_file)
        return [Transaction.from_dict(t) for t in transactions_data]
    
    def add_transaction(self, transaction):
        """Add a new transaction and update product quantity"""
        transactions_data = self._load_data(self.transactions_file)
        
        # Update product quantity
        product = self.get_product_by_id(transaction.product_id)
        if not product:
            raise ValueError(f"Product with ID {transaction.product_id} not found")
        
        if transaction.transaction_type == "IN":
            product.quantity += transaction.quantity
        elif transaction.transaction_type == "OUT":
            if product.quantity < transaction.quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")
            product.quantity -= transaction.quantity
        
        # Update product in database
        self.update_product(product)
        
        # Add transaction
        transactions_data.append(transaction.to_dict())
        self._save_data(self.transactions_file, transactions_data)
        
        return transaction 