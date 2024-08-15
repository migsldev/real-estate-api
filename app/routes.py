from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Property, Application, Wishlist
from app.schemas import UserSchema, PropertySchema, ApplicationSchema, WishlistSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

user_schema = UserSchema()
property_schema = PropertySchema()
application_schema = ApplicationSchema()
wishlist_schema = WishlistSchema()

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    role = data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

# User Login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
    return jsonify({"access_token": access_token}), 200

# Get User by ID
@main.route('/register/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user = get_jwt_identity()

    # Ensure that only the user themselves or an admin can view the user information
    if current_user['role'] != 'admin' and current_user['id'] != id:
        return jsonify({"message": "Unauthorized"}), 403

    user = User.query.get_or_404(id)
    return user_schema.jsonify(user), 200

# Update User Information
@main.route('/register/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity()
    
    # Ensure that only the user themselves or an admin can update the user information
    if current_user['role'] != 'admin' and current_user['id'] != id:
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get_or_404(id)
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if username:
        user.username = username
    if email:
        if User.query.filter_by(email=email).first() and email != user.email:
            return jsonify({"message": "Email already in use"}), 400
        user.email = email
    if password:
        user.password = generate_password_hash(password)
    if role:
        user.role = role

    db.session.commit()

    return user_schema.jsonify(user), 200

