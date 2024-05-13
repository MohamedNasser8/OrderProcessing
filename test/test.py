import pytest
from Models.models import db, User, Product
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create schema for testing
            test_product = Product(name="Product test", stock=10, price=19)

            # Add the product to the database session
            db.session.add(test_product)

            # Commit the changes to the database
            db.session.commit()
        yield client


def test_register_user(client):
    response = client.post('/user/register', json={
        'name': 'testuser',
        'email': 'mohamed1@gmail.com',
        'password': 'testpass'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'


def test_login_user(client):
    response = client.post('/user/login', json={
        'email': 'mohamed1@gmail.com',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert response.json['access_token']


def test_buy(client):
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTYwODI0NSwianRpIjoiNjNlYjQ2Y2YtNzg3Zi00ZmY4LTk4MGUtNGRkZGMyMjNjNzQyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InFAZ21haWwuY29tIiwibmJmIjoxNzE1NjA4MjQ1LCJjc3JmIjoiOWQ4NTQ2YmMtNGI5Yi00NGM2LTkwMDctMjMzYTNjMWZkMjU4IiwiZXhwIjoxNzE1NjEwMDQ1fQ.idBtR44AT1uI3vhVC6ljRWvPOvoPcvekL0T03rgWJmM'
    }

    response = client.post('products/order', json={
        "items": [
            {
                "id": 1,
                "quantity": 2
            }
        ],
        "stripeToken": "tok_visa",
        "email": "nassermohamed3222@gmail.com"
    }, headers=headers)

    assert response.status_code == 200
