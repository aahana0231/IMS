import uuid
from datetime import datetime
from .database import Database
from .models import Product, Category, Transaction

class InventoryManager:
    def __init__(self, data_dir):
        self.db = Database(data_dir)
    
    # Product management
    def add_product(self, name, description, price, quantity, category):
        """Add a new product to inventory"""
        # Generate unique ID
        product_id = str(uuid.uuid4())
        
        # Create and add product
        product = Product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category
        )
        
        return self.db.add_product(product)
    
    def update_product(self, product_id, **kwargs):
        """Update product details"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Update product attributes
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        return self.db.update_product(product)
    
    def get_product(self, product_id):
        """Get product by ID"""
        return self.db.get_product_by_id(product_id)
    
    def get_all_products(self):
        """Get all products"""
        return self.db.get_all_products()
    
    def delete_product(self, product_id):
        """Delete a product"""
        return self.db.delete_product(product_id)
    
    def search_products(self, search_term):
        """Search products by name or description"""
        products = self.db.get_all_products()
        search_term = search_term.lower()
        
        return [p for p in products if 
                search_term in p.name.lower() or 
                search_term in p.description.lower()]
    
    def get_products_by_category(self, category_id):
        """Get all products in a specific category"""
        products = self.db.get_all_products()
        return [p for p in products if p.category == category_id]
    
    def get_low_stock_products(self, threshold=10):
        """Get products with stock below threshold"""
        products = self.db.get_all_products()
        return [p for p in products if p.quantity <= threshold]
    
    # Category management
    def add_category(self, name, description=None):
        """Add a new category"""
        # Generate unique ID
        category_id = str(uuid.uuid4())
        
        # Create and add category
        category = Category(
            category_id=category_id,
            name=name,
            description=description
        )
        
        return self.db.add_category(category)
    
    def update_category(self, category_id, **kwargs):
        """Update category details"""
        category = self.db.get_category_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        
        # Update category attributes
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        
        return self.db.update_category(category)
    
    def get_category(self, category_id):
        """Get category by ID"""
        return self.db.get_category_by_id(category_id)
    
    def get_all_categories(self):
        """Get all categories"""
        return self.db.get_all_categories()
    
    def delete_category(self, category_id):
        """Delete a category"""
        return self.db.delete_category(category_id)
    
    # Inventory transactions
    def add_stock(self, product_id, quantity, user=None):
        """Add stock to inventory (stock in)"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Create transaction record
        transaction = Transaction(
            transaction_id=transaction_id,
            product_id=product_id,
            quantity=quantity,
            transaction_type="IN",
            timestamp=datetime.now().isoformat(),
            user=user
        )
        
        return self.db.add_transaction(transaction)
    
    def remove_stock(self, product_id, quantity, user=None):
        """Remove stock from inventory (stock out)"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        if product.quantity < quantity:
            raise ValueError(f"Insufficient stock for product {product.name}")
        
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Create transaction record
        transaction = Transaction(
            transaction_id=transaction_id,
            product_id=product_id,
            quantity=quantity,
            transaction_type="OUT",
            timestamp=datetime.now().isoformat(),
            user=user
        )
        
        return self.db.add_transaction(transaction)
    
    def get_transaction_history(self, product_id=None):
        """Get transaction history, optionally filtered by product ID"""
        transactions = self.db.get_all_transactions()
        
        if product_id:
            return [t for t in transactions if t.product_id == product_id]
        
        return transactions
        
    def get_transactions(self, product_id=None):
        """Alias for get_transaction_history for compatibility"""
        return self.get_transaction_history(product_id)
        
    def add_transaction(self, product_id, quantity, transaction_type, note=None, user=None, timestamp=None):
        """Add a transaction record directly"""
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Use current time if no timestamp provided
        if timestamp is None:
            timestamp = datetime.now()
            
        # Create transaction record
        transaction = Transaction(
            transaction_id=transaction_id,
            product_id=product_id,
            quantity=quantity,
            transaction_type=transaction_type,
            timestamp=timestamp,
            user=user,
            note=note
        )
        
        return self.db.add_transaction(transaction) 