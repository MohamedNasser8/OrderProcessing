from flask import Blueprint, request, jsonify, current_app
from flask_principal import identity_changed, Identity

from Models.models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import my_logger

user = Blueprint('users', __name__)


@user.route('/register', methods=['POST'])
def register():
    my_logger.info("Register user ")
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = 'user'

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        my_logger.error("Logger already exists")
        return jsonify({'message': 'Email already exists'}), 409

    new_user = User(name=name, email=email, role=role, password=password)

    db.session.add(new_user)
    db.session.commit()
    my_logger.info("User created successfully")
    return jsonify({'message': 'User created successfully'}), 201


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=email)
        # Assign roles based on the user's role field
        if user.role == 'admin':
            my_logger.info("login as admin")
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id, ['admin']))
        else:
            my_logger.info('login as user')
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id, ['user']))

        return jsonify(access_token=access_token), 200
    else:
        my_logger.error('Invalid username or password')
        return jsonify({'message': 'Invalid username or password'}), 401

@user.route('/')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as=current_user), 200


