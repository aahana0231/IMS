#!/usr/bin/env python3
"""
Report Generator for Inventory Management System
This script generates various reports based on transaction history and inventory data.
"""

import os
import sys
from datetime import datetime, timedelta
import csv
import json
from collections import defaultdict

# Add parent directory to import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.inventory_manager import InventoryManager
from app.models import TransactionType

def generate_reports():
    """Generate inventory and transaction reports"""
    # Initialize the inventory manager
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    manager = InventoryManager(data_dir)
    
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate all reports
    generate_low_stock_report(manager, reports_dir, timestamp)
    generate_inventory_value_report(manager, reports_dir, timestamp)
    generate_transaction_report(manager, reports_dir, timestamp)
    generate_sales_trend_report(manager, reports_dir, timestamp)
    generate_category_performance_report(manager, reports_dir, timestamp)
    generate_reorder_recommendation_report(manager, reports_dir, timestamp)
    
    # Generate summary report
    generate_summary_report(manager, reports_dir, timestamp)
    
    print(f"Reports have been generated in the '{reports_dir}' directory.")

def generate_low_stock_report(manager, reports_dir, timestamp):
    """Generate a report of low stock items"""
    filename = os.path.join(reports_dir, f"low_stock_report_{timestamp}.csv")
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product ID', 'Name', 'Category', 'Current Quantity', 'Alert Threshold', 'Status'])
        
        products = manager.get_all_products()
        low_stock_threshold = 5  # Default alert threshold
        critical_threshold = 2   # Critical threshold
        
        low_stock_products = [p for p in products if p.quantity <= low_stock_threshold]
        
        # Sort by quantity (lowest first)
        low_stock_products.sort(key=lambda p: p.quantity)
        
        for product in low_stock_products:
            # Determine status
            if product.quantity <= critical_threshold:
                status = "CRITICAL"
            else:
                status = "LOW"
                
            writer.writerow([
                product.product_id,
                product.name,
                product.category,
                product.quantity,
                low_stock_threshold,
                status
            ])
    
    print(f"Low stock report generated: {filename}")
    return len(low_stock_products)

def generate_inventory_value_report(manager, reports_dir, timestamp):
    """Generate a report of inventory value by category"""
    filename = os.path.join(reports_dir, f"inventory_value_report_{timestamp}.csv")
    
    products = manager.get_all_products()
    
    # Calculate totals by category
    categories = {}
    total_value = 0
    total_items = 0
    
    for product in products:
        category = product.category
        value = product.price * product.quantity
        
        if category not in categories:
            categories[category] = {'count': 0, 'value': 0, 'items': 0}
        
        categories[category]['count'] += 1
        categories[category]['value'] += value
        categories[category]['items'] += product.quantity
        total_value += value
        total_items += product.quantity
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Product Count', 'Total Items', 'Total Value ($)', 'Average Item Value ($)'])
        
        # Sort categories by value (highest first)
        for category, data in sorted(categories.items(), key=lambda x: x[1]['value'], reverse=True):
            avg_value = data['value'] / data['items'] if data['items'] > 0 else 0
            writer.writerow([
                category,
                data['count'],
                data['items'],
                f"{data['value']:.2f}",
                f"{avg_value:.2f}"
            ])
        
        # Add summary row
        avg_total_value = total_value / total_items if total_items > 0 else 0
        writer.writerow(['', '', '', '', ''])
        writer.writerow(['Total', len(products), total_items, f"${total_value:.2f}", f"${avg_total_value:.2f}"])
    
    print(f"Inventory value report generated: {filename}")
    return total_value

def generate_transaction_report(manager, reports_dir, timestamp, days=30):
    """Generate a report of transactions from the specified number of days"""
    filename = os.path.join(reports_dir, f"transaction_report_{timestamp}.csv")
    
    # Get time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    transactions = manager.get_transaction_history()
    
    # Filter transactions to specified date range
    if isinstance(transactions[0].timestamp, str):
        # Convert string timestamps to datetime objects
        for t in transactions:
            if isinstance(t.timestamp, str):
                t.timestamp = datetime.fromisoformat(t.timestamp)
    
    recent_transactions = [t for t in transactions 
                          if start_date <= t.timestamp <= end_date]
    
    # Count additions and removals
    additions = sum(1 for t in recent_transactions if t.transaction_type == "IN" or t.transaction_type == TransactionType.ADDITION)
    removals = sum(1 for t in recent_transactions if t.transaction_type == "OUT" or t.transaction_type == TransactionType.REMOVAL)
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Product ID', 'Product Name', 'Type', 'Quantity', 'Note'])
        
        # Dictionary to store product names by ID
        product_names = {}
        
        # Sort transactions by timestamp (newest first)
        for transaction in sorted(recent_transactions, 
                                 key=lambda t: t.timestamp, 
                                 reverse=True):
            # Get product name if we haven't retrieved it already
            if transaction.product_id not in product_names:
                product = manager.get_product(transaction.product_id)
                product_names[transaction.product_id] = product.name if product else "Unknown"
            
            # Determine transaction type string
            if transaction.transaction_type == "IN" or transaction.transaction_type == TransactionType.ADDITION:
                type_str = "Addition"
            else:
                type_str = "Removal"
            
            writer.writerow([
                transaction.timestamp.strftime("%Y-%m-%d %H:%M"),
                transaction.product_id,
                product_names[transaction.product_id],
                type_str,
                transaction.quantity,
                transaction.note if hasattr(transaction, 'note') else ""
            ])
    
    print(f"Transaction report generated: {filename}")
    return len(recent_transactions), additions, removals

def generate_sales_trend_report(manager, reports_dir, timestamp, days=30):
    """Generate a report showing sales trends over the specified period"""
    filename = os.path.join(reports_dir, f"sales_trend_report_{timestamp}.csv")
    
    # Get time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    transactions = manager.get_transaction_history()
    
    # Filter transactions to removals (sales) in the specified date range
    if isinstance(transactions[0].timestamp, str):
        # Convert string timestamps to datetime objects
        for t in transactions:
            if isinstance(t.timestamp, str):
                t.timestamp = datetime.fromisoformat(t.timestamp)
    
    sales_transactions = [t for t in transactions 
                         if (start_date <= t.timestamp <= end_date) and 
                         (t.transaction_type == "OUT" or t.transaction_type == TransactionType.REMOVAL)]
    
    # Group by day
    daily_sales = defaultdict(lambda: defaultdict(int))
    product_names = {}
    
    for transaction in sales_transactions:
        day = transaction.timestamp.strftime("%Y-%m-%d")
        
        # Get product name if we haven't retrieved it already
        if transaction.product_id not in product_names:
            product = manager.get_product(transaction.product_id)
            product_names[transaction.product_id] = product.name if product else "Unknown"
        
        # Aggregate quantities by day and product
        daily_sales[day][product_names[transaction.product_id]] += transaction.quantity
    
    # Sort days
    sorted_days = sorted(daily_sales.keys())
    
    # Get all unique product names across all days
    all_products = set()
    for day_data in daily_sales.values():
        all_products.update(day_data.keys())
    
    sorted_products = sorted(all_products)
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ['Date'] + sorted_products
        writer.writerow(header)
        
        # Write data for each day
        for day in sorted_days:
            row = [day]
            for product in sorted_products:
                row.append(daily_sales[day][product])
            writer.writerow(row)
    
    print(f"Sales trend report generated: {filename}")
    return len(sorted_days), len(all_products)

def generate_category_performance_report(manager, reports_dir, timestamp, days=30):
    """Generate a report showing performance by category"""
    filename = os.path.join(reports_dir, f"category_performance_report_{timestamp}.csv")
    
    # Get time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    transactions = manager.get_transaction_history()
    products = {p.product_id: p for p in manager.get_all_products()}
    categories = {c.category_id: c for c in manager.get_all_categories()}
    
    # Filter transactions to removals (sales) in the specified date range
    if transactions and isinstance(transactions[0].timestamp, str):
        # Convert string timestamps to datetime objects
        for t in transactions:
            if isinstance(t.timestamp, str):
                t.timestamp = datetime.fromisoformat(t.timestamp)
    
    sales_transactions = [t for t in transactions 
                         if (start_date <= t.timestamp <= end_date) and 
                         (t.transaction_type == "OUT" or t.transaction_type == TransactionType.REMOVAL)]
    
    # Aggregate by category
    category_sales = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
    
    for transaction in sales_transactions:
        product = products.get(transaction.product_id)
        if not product:
            continue
            
        category_id = product.category
        category_name = categories.get(category_id, Category(category_id, "Unknown")).name
        
        category_sales[category_name]['quantity'] += transaction.quantity
        category_sales[category_name]['revenue'] += transaction.quantity * product.price
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Units Sold', 'Revenue', 'Average Price'])
        
        # Sort categories by revenue (highest first)
        total_quantity = 0
        total_revenue = 0
        
        for category, data in sorted(category_sales.items(), key=lambda x: x[1]['revenue'], reverse=True):
            avg_price = data['revenue'] / data['quantity'] if data['quantity'] > 0 else 0
            writer.writerow([
                category,
                data['quantity'],
                f"${data['revenue']:.2f}",
                f"${avg_price:.2f}"
            ])
            
            total_quantity += data['quantity']
            total_revenue += data['revenue']
        
        # Add summary row
        avg_total_price = total_revenue / total_quantity if total_quantity > 0 else 0
        writer.writerow(['', '', '', ''])
        writer.writerow(['Total', total_quantity, f"${total_revenue:.2f}", f"${avg_total_price:.2f}"])
    
    print(f"Category performance report generated: {filename}")
    return total_revenue

def generate_reorder_recommendation_report(manager, reports_dir, timestamp):
    """Generate recommendations for products that need to be reordered"""
    filename = os.path.join(reports_dir, f"reorder_recommendation_report_{timestamp}.csv")
    
    products = manager.get_all_products()
    low_stock_threshold = 5
    
    # Get low stock products
    low_stock_products = [p for p in products if p.quantity <= low_stock_threshold]
    
    # Get transaction history to analyze usage patterns
    transactions = manager.get_transaction_history()
    
    # Convert string timestamps to datetime objects if needed
    if transactions and isinstance(transactions[0].timestamp, str):
        for t in transactions:
            if isinstance(t.timestamp, str):
                t.timestamp = datetime.fromisoformat(t.timestamp)
    
    # Analyze past 30 days to determine usage rate
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Calculate usage rate for each product
    usage_rates = {}
    
    for product in low_stock_products:
        # Get removals for this product in the last 30 days
        product_transactions = [t for t in transactions 
                              if t.product_id == product.product_id and
                              start_date <= t.timestamp <= end_date and
                              (t.transaction_type == "OUT" or t.transaction_type == TransactionType.REMOVAL)]
        
        total_removed = sum(t.quantity for t in product_transactions)
        daily_usage = total_removed / 30  # Average daily usage
        
        # Recommend order quantity based on 30 days of future usage
        recommended_order = max(int(daily_usage * 30) - product.quantity, 0)
        
        # Days until stockout at current rate
        days_to_stockout = int(product.quantity / daily_usage) if daily_usage > 0 else 999
        
        usage_rates[product.product_id] = {
            'daily_usage': daily_usage,
            'recommended_order': recommended_order,
            'days_to_stockout': days_to_stockout
        }
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product ID', 'Name', 'Current Quantity', 'Daily Usage', 
                        'Days to Stockout', 'Recommended Order Quantity', 'Priority'])
        
        # Sort by days to stockout (lowest first)
        sorted_products = sorted(low_stock_products, 
                               key=lambda p: usage_rates[p.product_id]['days_to_stockout'])
        
        for product in sorted_products:
            usage_data = usage_rates[product.product_id]
            
            # Determine priority
            if usage_data['days_to_stockout'] <= 7:
                priority = "HIGH"
            elif usage_data['days_to_stockout'] <= 14:
                priority = "MEDIUM"
            else:
                priority = "LOW"
            
            writer.writerow([
                product.product_id,
                product.name,
                product.quantity,
                f"{usage_data['daily_usage']:.2f}",
                usage_data['days_to_stockout'],
                usage_data['recommended_order'],
                priority
            ])
    
    print(f"Reorder recommendation report generated: {filename}")
    return len(low_stock_products)

def generate_summary_report(manager, reports_dir, timestamp):
    """Generate a summary report with key metrics"""
    filename = os.path.join(reports_dir, f"summary_report_{timestamp}.txt")
    
    # Get key metrics
    total_products = len(manager.get_all_products())
    total_categories = len(manager.get_all_categories())
    low_stock_count = len(manager.get_low_stock_products(5))
    
    # Calculate inventory value
    products = manager.get_all_products()
    total_inventory_value = sum(p.price * p.quantity for p in products)
    
    # Transaction statistics (last 30 days)
    transactions = manager.get_transaction_history()
    
    # Convert string timestamps to datetime objects if needed
    if transactions and isinstance(transactions[0].timestamp, str):
        for t in transactions:
            if isinstance(t.timestamp, str):
                t.timestamp = datetime.fromisoformat(t.timestamp)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    recent_transactions = [t for t in transactions 
                          if start_date <= t.timestamp <= end_date]
    
    additions = [t for t in recent_transactions 
                if t.transaction_type == "IN" or t.transaction_type == TransactionType.ADDITION]
    removals = [t for t in recent_transactions 
               if t.transaction_type == "OUT" or t.transaction_type == TransactionType.REMOVAL]
    
    total_added = sum(t.quantity for t in additions)
    total_removed = sum(t.quantity for t in removals)
    
    # Calculate sales value
    sales_value = 0
    for transaction in removals:
        product = manager.get_product(transaction.product_id)
        if product:
            sales_value += transaction.quantity * product.price
    
    with open(filename, 'w') as file:
        file.write("=== INVENTORY MANAGEMENT SYSTEM SUMMARY REPORT ===\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        file.write("--- INVENTORY OVERVIEW ---\n")
        file.write(f"Total Products: {total_products}\n")
        file.write(f"Total Categories: {total_categories}\n")
        file.write(f"Total Inventory Value: ${total_inventory_value:.2f}\n")
        file.write(f"Low Stock Items: {low_stock_count}\n\n")
        
        file.write("--- 30-DAY TRANSACTION SUMMARY ---\n")
        file.write(f"Total Transactions: {len(recent_transactions)}\n")
        file.write(f"Items Added to Inventory: {total_added}\n")
        file.write(f"Items Removed from Inventory: {total_removed}\n")
        file.write(f"Sales Value: ${sales_value:.2f}\n\n")
        
        # Top categories by sales
        file.write("--- TOP CATEGORIES BY SALES ---\n")
        category_sales = defaultdict(float)
        
        for transaction in removals:
            product = manager.get_product(transaction.product_id)
            if not product:
                continue
                
            category_name = product.category
            category_sales[category_name] += transaction.quantity * product.price
        
        for i, (category, value) in enumerate(sorted(category_sales.items(), 
                                                  key=lambda x: x[1], 
                                                  reverse=True)[:5], 1):
            file.write(f"{i}. {category}: ${value:.2f}\n")
        
        file.write("\n--- REPORT COMPLETION ---\n")
        file.write("All reports have been generated successfully.\n")
    
    print(f"Summary report generated: {filename}")

if __name__ == "__main__":
    generate_reports() 