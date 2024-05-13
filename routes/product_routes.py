from flask import jsonify, Blueprint, request, render_template
from flask_mail import Message
from flask_jwt_extended import jwt_required

from Models.models import Product, db
from Models.roles import admin_permission
from app import mail, my_logger
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')
products = Blueprint('views', __name__)


@products.route('/')
def getAll():
    # Use the model to query the database
    products = Product.query.all()
    # Convert the product objects to a list of dictionaries
    product_list = [{'id': product.id, 'name': product.name, 'stock': product.stock, 'price': product.price} for product
                    in products]
    return jsonify({'products': product_list})


@products.route('/add', methods=['POST'])
@jwt_required()
@admin_permission.require(http_exception=403)
def create_product():
    try:
        # 1. Get JSON data from request (assuming it's JSON)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing product data'}), 400  # Bad Request

        # 2. Extract product information with validation
        name = data.get('name')
        if not name or not isinstance(name, str):
            return jsonify({'error': 'Invalid product name'}), 400  # Bad Request

        stock = data.get('stock')
        if not stock or not isinstance(stock, int) or stock <= 0:
            return jsonify({'error': 'Invalid product stock'}), 400  # Bad Request

        price = data.get('price')
        if not stock or not isinstance(price, int) or price <= 0:
            return jsonify({'error': 'Invalid product price'}), 400  # Bad Request

        new_product = Product(name=name, stock=stock, price=price)

        # 4. Add product to database
        db.session.add(new_product)
        db.session.commit()

        # 5. Return success response with product details (optional)
        return jsonify({'message': 'Product created successfully', 'product': new_product.serialize()}), 201  # Created

    except Exception as e:
        # 6. Handle unexpected errors
        db.session.rollback()  # Rollback changes in case of errors
        return jsonify({'error': f'Internal server error: {e}'}), 500  # Internal Server Error


@products.route('/order', methods=['POST'])
@jwt_required()
def purchase():
    my_logger.info('Order processing started')
    try:
        data = request.json
        total_amount = 0
        products_to_update = []
        order_details = []

        for item in data['items']:
            product_id = item['id']
            quantity = item['quantity']
            product = Product.query.get(product_id)
            order_details.append(f"{product.name}: {quantity} x ${product.price}")

            if product and product.check_stock(quantity):
                total_amount += product.price * quantity
                products_to_update.append((product, quantity))
            else:
                return jsonify({'error': 'Insufficient stock for product id {}'.format(product_id)}), 400

        # Create a charge
        try:
            charge = stripe.Charge.create(
                amount=int(total_amount * 100),  # Amount in cents
                currency='usd',
                source=data['stripeToken'],  # Obtained from the frontend
                description='Charge for purchase'
            )
            # Reduce stock if the charge is successful
            for product, quantity in products_to_update:
                product.reduce_stock(quantity)

                # If the charge is successful, send a confirmation email
            if charge:
                email_html = render_template('purchase_confirmation.html', order_details=order_details,
                                             total_amount=total_amount)
                message = Message('Purchase Confirmation', sender='mohammednasser8800@gmail.com',
                                  recipients=[data['email']])
                message.html = email_html
                mail.send(message)

            return jsonify({'status': 'success', 'charge': charge}), 200
        except stripe.error.StripeError as e:
            my_logger.error("Order processing failed")
            return jsonify({'error': str(e)}), 400
    except:
        my_logger.error('An error occurred')
        return jsonify({"Internal Server Error"}), 500
