# Inventory Management System

A complete inventory management solution with both command-line and web interfaces, built with Python.

## Features

- **Product Management**: Add, update, delete, and list products
- **Category Management**: Organize products into categories
- **Stock Management**: Track stock levels with transaction history
- **Search**: Find products by name or description
- **Low Stock Alerts**: Identify products that need restocking
- **Dual Interface**: Use either CLI or web interface based on your preference

## Requirements

- Python 3.6 or higher
- Flask (for web interface)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system
```

Install dependencies:

```bash
pip install flask
```

## Usage

### Launcher

The easiest way to start is to use the launcher script:

```bash
python run.py
```

This will present a menu where you can choose to launch either the web interface or the command-line interface.

### Web Interface

To directly launch the web interface:

```bash
python run.py web
```

Additional options:
- `--host`: Specify the host (default: 127.0.0.1)
- `--port`: Specify the port (default: 5000)
- `--no-browser`: Don't open the browser automatically

The web interface offers an intuitive, user-friendly way to:
- View dashboard with system overview
- Manage products and categories
- Process stock additions and removals
- Track transaction history
- Monitor low stock items

### Command-Line Interface

To directly launch the CLI:

```bash
python run.py cli [command] [options]
```

Or use the main.py script directly:

```bash
python main.py [command] [options]
```

#### Available CLI Commands

##### Product Management

- List all products:
  ```
  python main.py list-products
  ```

- Add a new product:
  ```
  python main.py add-product "Product Name" "Product Description" 99.99 100 category_id
  ```

- Update a product:
  ```
  python main.py update-product product_id --name "New Name" --price 89.99
  ```

- Delete a product:
  ```
  python main.py delete-product product_id
  ```

##### Category Management

- List all categories:
  ```
  python main.py list-categories
  ```

- Add a new category:
  ```
  python main.py add-category "Category Name" --description "Category Description"
  ```

- Update a category:
  ```
  python main.py update-category category_id --name "New Name"
  ```

- Delete a category:
  ```
  python main.py delete-category category_id
  ```

##### Inventory Operations

- Add stock:
  ```
  python main.py add-stock product_id 50 --user "John Doe"
  ```

- Remove stock:
  ```
  python main.py remove-stock product_id 20 --user "John Doe"
  ```

- View transaction history:
  ```
  python main.py transactions
  ```
  
- View transaction history for a specific product:
  ```
  python main.py transactions --id product_id
  ```

##### Other Commands

- Search for products:
  ```
  python main.py search "search term"
  ```

- View low stock products:
  ```
  python main.py low-stock --threshold 15
  ```

## Data Storage

The application stores data in JSON files in the `data` directory:
- `products.json`: Product information
- `categories.json`: Category information
- `transactions.json`: Transaction history

## Project Structure

```
inventory_management_system/
├── app/                  # CLI application core
│   ├── __init__.py
│   ├── models.py         # Data models
│   ├── database.py       # Data storage
│   ├── inventory_manager.py  # Business logic
│   └── cli.py            # Command-line interface
├── web/                  # Web interface
│   ├── app.py            # Flask web application
│   ├── static/           # Static assets
│   │   ├── css/          # CSS styles
│   │   └── js/           # JavaScript
│   └── templates/        # HTML templates
│       ├── layout.html   # Base template
│       ├── index.html    # Dashboard
│       └── ...           # Other templates
├── data/                 # Data storage
│   ├── products.json
│   ├── categories.json
│   └── transactions.json
├── main.py               # CLI entry point
├── run.py                # Launcher script
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 