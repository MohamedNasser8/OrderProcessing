from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name

        # Method to check if enough stock is available

    def check_stock(self, quantity):
        return self.stock >= quantity

        # Method to reduce the stock count after a successful order

    def reduce_stock(self, quantity):
        if self.check_stock(quantity):
            self.stock -= quantity
            db.session.commit()
            return True
        return False

    def __init__(self, name, stock, price):
        """
        Constructor for the Product model.

        Args:
            name (str): The name of the product.
            stock (int): The initial stock quantity for the product.
            price (int): The price of the product
        """

        self.name = name
        self.stock = stock
        self.price = price

    def serialize(self):
        """
        Serializes the product object into a dictionary.

        Returns:
            dict: A dictionary containing product information.
        """

        return {
            'id': self.id,
            'name': self.name,
            'stock': self.stock,
            'price': self.price
        }


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password_hash = db.Column(db.String(256))  # Store hashed passwords
    role = db.Column(db.String(80))
    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, name, email, role, password):
        self.name = name
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
