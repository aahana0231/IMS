#!/usr/bin/env python3
"""
Transaction Sample Data Loader for Inventory Management System
This script adds sample transactions to demonstrate the transaction history feature.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.inventory_manager import InventoryManager
from app.models import TransactionType
from load_sample_data import load_sample_data

def load_transaction_data():
    """Load sample transactions for demonstration"""
    # First ensure we have regular sample data
    load_sample_data()
    
    # Initialize the inventory manager
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    manager = InventoryManager(data_dir)
    
    # Get all products
    products = manager.get_all_products()
    if not products:
        print("No products found. Please run load_sample_data.py first.")
        return
    
    # Sample transactions
    # We'll create a mix of ADDITION and REMOVAL transactions over the past 30 days
    print("Creating sample transactions...")
    
    transaction_count = 0
    now = datetime.now()
    
    for i in range(30):  # For the past 30 days
        transaction_date = now - timedelta(days=i)
        
        # Random number of transactions per day (1-5)
        daily_transactions = random.randint(1, 5)
        
        for j in range(daily_transactions):
            # Select a random product
            product = random.choice(products)
            
            # Determine transaction type (60% additions, 40% removals)
            transaction_type = TransactionType.ADDITION if random.random() < 0.6 else TransactionType.REMOVAL
            
            # Determine quantity (1-10 for additions, 1-3 for removals)
            if transaction_type == TransactionType.ADDITION:
                quantity = random.randint(1, 10)
                note = f"Restocked {product.name}"
            else:
                quantity = random.randint(1, 3)
                note = f"Sold {product.name}"
            
            # Create transaction with the specific date
            manager.add_transaction(
                product_id=product.product_id,
                quantity=quantity,
                transaction_type=transaction_type,
                note=note,
                timestamp=transaction_date
            )
            
            transaction_count += 1
    
    print(f"Transaction loading complete! Added {transaction_count} sample transactions.")

if __name__ == "__main__":
    load_transaction_data() 