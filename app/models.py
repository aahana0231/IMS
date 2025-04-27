class Product:
    def __init__(self, product_id, name, description, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity'],
            category=data['category']
        )


class Category:
    def __init__(self, category_id, name, description=None):
        self.category_id = category_id
        self.name = name
        self.description = description
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            category_id=data['category_id'],
            name=data['name'],
            description=data.get('description')
        )


# Define TransactionType enum
class TransactionType:
    ADDITION = "IN"
    REMOVAL = "OUT"


class Transaction:
    def __init__(self, transaction_id, product_id, quantity, transaction_type, timestamp, user=None, note=None):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.transaction_type = transaction_type  # "IN" or "OUT"
        self.timestamp = timestamp
        self.user = user
        self.note = note
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'transaction_type': self.transaction_type,
            'timestamp': self.timestamp,
            'user': self.user,
            'note': self.note
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_id=data['transaction_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            transaction_type=data['transaction_type'],
            timestamp=data['timestamp'],
            user=data.get('user'),
            note=data.get('note')
        ) 