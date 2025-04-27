import os
import argparse
from datetime import datetime
from .inventory_manager import InventoryManager

class InventoryCLI:
    def __init__(self, data_dir):
        self.manager = InventoryManager(data_dir)
    
    def list_products(self, args):
        """List all products"""
        products = self.manager.get_all_products()
        
        if not products:
            print("No products found.")
            return
        
        print(f"\n{'ID':<40} {'Name':<20} {'Category':<20} {'Price':<10} {'Quantity':<10}")
        print("-" * 100)
        
        for product in products:
            category = self.manager.get_category(product.category)
            category_name = category.name if category else "Unknown"
            
            print(f"{product.product_id:<40} {product.name:<20} {category_name:<20} ${product.price:<9.2f} {product.quantity:<10}")
    
    def add_product(self, args):
        """Add a new product"""
        # Check if category exists
        category = self.manager.get_category(args.category)
        if not category:
            # List available categories
            categories = self.manager.get_all_categories()
            if not categories:
                print("No categories available. Please create a category first.")
                return
            
            print("\nAvailable categories:")
            for cat in categories:
                print(f"ID: {cat.category_id}, Name: {cat.name}")
            
            print(f"\nCategory with ID {args.category} not found.")
            return
        
        try:
            product = self.manager.add_product(
                name=args.name,
                description=args.description,
                price=float(args.price),
                quantity=int(args.quantity),
                category=args.category
            )
            print(f"Product '{product.name}' added with ID: {product.product_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def update_product(self, args):
        """Update an existing product"""
        product = self.manager.get_product(args.id)
        if not product:
            print(f"Product with ID {args.id} not found.")
            return
        
        update_data = {}
        if args.name:
            update_data['name'] = args.name
        if args.description:
            update_data['description'] = args.description
        if args.price:
            update_data['price'] = float(args.price)
        if args.quantity:
            update_data['quantity'] = int(args.quantity)
        if args.category:
            # Check if category exists
            category = self.manager.get_category(args.category)
            if not category:
                print(f"Category with ID {args.category} not found.")
                return
            update_data['category'] = args.category
        
        try:
            updated_product = self.manager.update_product(args.id, **update_data)
            print(f"Product '{updated_product.name}' updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def delete_product(self, args):
        """Delete a product"""
        product = self.manager.get_product(args.id)
        if not product:
            print(f"Product with ID {args.id} not found.")
            return
        
        if self.manager.delete_product(args.id):
            print(f"Product '{product.name}' deleted successfully.")
        else:
            print(f"Failed to delete product with ID {args.id}.")
    
    def list_categories(self, args):
        """List all categories"""
        categories = self.manager.get_all_categories()
        
        if not categories:
            print("No categories found.")
            return
        
        print(f"\n{'ID':<40} {'Name':<20} {'Description':<40}")
        print("-" * 100)
        
        for category in categories:
            description = category.description or "N/A"
            print(f"{category.category_id:<40} {category.name:<20} {description:<40}")
    
    def add_category(self, args):
        """Add a new category"""
        try:
            category = self.manager.add_category(
                name=args.name,
                description=args.description
            )
            print(f"Category '{category.name}' added with ID: {category.category_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def update_category(self, args):
        """Update a category"""
        category = self.manager.get_category(args.id)
        if not category:
            print(f"Category with ID {args.id} not found.")
            return
        
        update_data = {}
        if args.name:
            update_data['name'] = args.name
        if args.description:
            update_data['description'] = args.description
        
        try:
            updated_category = self.manager.update_category(args.id, **update_data)
            print(f"Category '{updated_category.name}' updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def delete_category(self, args):
        """Delete a category"""
        category = self.manager.get_category(args.id)
        if not category:
            print(f"Category with ID {args.id} not found.")
            return
        
        if self.manager.delete_category(args.id):
            print(f"Category '{category.name}' deleted successfully.")
        else:
            print(f"Failed to delete category with ID {args.id}.")
    
    def add_stock(self, args):
        """Add stock to inventory"""
        try:
            transaction = self.manager.add_stock(
                product_id=args.id,
                quantity=int(args.quantity),
                user=args.user
            )
            product = self.manager.get_product(args.id)
            print(f"Added {args.quantity} units to '{product.name}'. New quantity: {product.quantity}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def remove_stock(self, args):
        """Remove stock from inventory"""
        try:
            transaction = self.manager.remove_stock(
                product_id=args.id,
                quantity=int(args.quantity),
                user=args.user
            )
            product = self.manager.get_product(args.id)
            print(f"Removed {args.quantity} units from '{product.name}'. New quantity: {product.quantity}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_transactions(self, args):
        """View transaction history"""
        if args.id:
            product = self.manager.get_product(args.id)
            if not product:
                print(f"Product with ID {args.id} not found.")
                return
            transactions = self.manager.get_transaction_history(args.id)
            title = f"Transaction history for product: {product.name}"
        else:
            transactions = self.manager.get_transaction_history()
            title = "All transactions"
        
        if not transactions:
            print("No transactions found.")
            return
        
        print(f"\n{title}")
        print(f"\n{'ID':<40} {'Product':<20} {'Type':<10} {'Quantity':<10} {'Date':<20} {'User':<15}")
        print("-" * 115)
        
        for t in transactions:
            product = self.manager.get_product(t.product_id)
            product_name = product.name if product else "Unknown"
            user = t.user if t.user else "N/A"
            
            # Convert ISO format to readable date
            try:
                date = datetime.fromisoformat(t.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                date = t.timestamp
            
            print(f"{t.transaction_id:<40} {product_name:<20} {t.transaction_type:<10} {t.quantity:<10} {date:<20} {user:<15}")
    
    def search_products(self, args):
        """Search for products"""
        products = self.manager.search_products(args.term)
        
        if not products:
            print(f"No products found matching '{args.term}'.")
            return
        
        print(f"\nSearch results for '{args.term}':")
        print(f"\n{'ID':<40} {'Name':<20} {'Category':<20} {'Price':<10} {'Quantity':<10}")
        print("-" * 100)
        
        for product in products:
            category = self.manager.get_category(product.category)
            category_name = category.name if category else "Unknown"
            
            print(f"{product.product_id:<40} {product.name:<20} {category_name:<20} ${product.price:<9.2f} {product.quantity:<10}")
    
    def low_stock_alert(self, args):
        """Display products with low stock"""
        threshold = int(args.threshold) if args.threshold else 10
        products = self.manager.get_low_stock_products(threshold)
        
        if not products:
            print(f"No products found with stock below {threshold} units.")
            return
        
        print(f"\nProducts with stock below {threshold} units:")
        print(f"\n{'ID':<40} {'Name':<20} {'Category':<20} {'Price':<10} {'Quantity':<10}")
        print("-" * 100)
        
        for product in products:
            category = self.manager.get_category(product.category)
            category_name = category.name if category else "Unknown"
            
            print(f"{product.product_id:<40} {product.name:<20} {category_name:<20} ${product.price:<9.2f} {product.quantity:<10}")


def setup_parser():
    """Set up command-line argument parser"""
    parser = argparse.ArgumentParser(description='Inventory Management System')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Product commands
    list_products_parser = subparsers.add_parser('list-products', help='List all products')
    
    add_product_parser = subparsers.add_parser('add-product', help='Add a new product')
    add_product_parser.add_argument('name', help='Product name')
    add_product_parser.add_argument('description', help='Product description')
    add_product_parser.add_argument('price', help='Product price')
    add_product_parser.add_argument('quantity', help='Initial quantity')
    add_product_parser.add_argument('category', help='Category ID')
    
    update_product_parser = subparsers.add_parser('update-product', help='Update a product')
    update_product_parser.add_argument('id', help='Product ID')
    update_product_parser.add_argument('--name', help='New product name')
    update_product_parser.add_argument('--description', help='New product description')
    update_product_parser.add_argument('--price', help='New product price')
    update_product_parser.add_argument('--quantity', help='New quantity')
    update_product_parser.add_argument('--category', help='New category ID')
    
    delete_product_parser = subparsers.add_parser('delete-product', help='Delete a product')
    delete_product_parser.add_argument('id', help='Product ID')
    
    # Category commands
    list_categories_parser = subparsers.add_parser('list-categories', help='List all categories')
    
    add_category_parser = subparsers.add_parser('add-category', help='Add a new category')
    add_category_parser.add_argument('name', help='Category name')
    add_category_parser.add_argument('--description', help='Category description')
    
    update_category_parser = subparsers.add_parser('update-category', help='Update a category')
    update_category_parser.add_argument('id', help='Category ID')
    update_category_parser.add_argument('--name', help='New category name')
    update_category_parser.add_argument('--description', help='New category description')
    
    delete_category_parser = subparsers.add_parser('delete-category', help='Delete a category')
    delete_category_parser.add_argument('id', help='Category ID')
    
    # Stock operations
    add_stock_parser = subparsers.add_parser('add-stock', help='Add stock to inventory')
    add_stock_parser.add_argument('id', help='Product ID')
    add_stock_parser.add_argument('quantity', help='Quantity to add')
    add_stock_parser.add_argument('--user', help='User performing the operation')
    
    remove_stock_parser = subparsers.add_parser('remove-stock', help='Remove stock from inventory')
    remove_stock_parser.add_argument('id', help='Product ID')
    remove_stock_parser.add_argument('quantity', help='Quantity to remove')
    remove_stock_parser.add_argument('--user', help='User performing the operation')
    
    # Transaction history
    transactions_parser = subparsers.add_parser('transactions', help='View transaction history')
    transactions_parser.add_argument('--id', help='Filter by product ID')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Search for products')
    search_parser.add_argument('term', help='Search term')
    
    # Low stock alert
    low_stock_parser = subparsers.add_parser('low-stock', help='Display products with low stock')
    low_stock_parser.add_argument('--threshold', help='Stock threshold (default: 10)')
    
    return parser


def main():
    """Main entry point for the CLI"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Get data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    # Create CLI instance
    cli = InventoryCLI(data_dir)
    
    # Execute command
    if args.command == 'list-products':
        cli.list_products(args)
    elif args.command == 'add-product':
        cli.add_product(args)
    elif args.command == 'update-product':
        cli.update_product(args)
    elif args.command == 'delete-product':
        cli.delete_product(args)
    elif args.command == 'list-categories':
        cli.list_categories(args)
    elif args.command == 'add-category':
        cli.add_category(args)
    elif args.command == 'update-category':
        cli.update_category(args)
    elif args.command == 'delete-category':
        cli.delete_category(args)
    elif args.command == 'add-stock':
        cli.add_stock(args)
    elif args.command == 'remove-stock':
        cli.remove_stock(args)
    elif args.command == 'transactions':
        cli.view_transactions(args)
    elif args.command == 'search':
        cli.search_products(args)
    elif args.command == 'low-stock':
        cli.low_stock_alert(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main() 