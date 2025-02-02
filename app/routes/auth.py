from flask import Blueprint, jsonify, request
from app import db
from app.models import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

# 📝 REGISTER USER
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'pharmacist')  # Default role

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

# 🔐 LOGIN USER
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
    return jsonify({'message': 'Login successful', 'access_token': access_token}), 200

# 🚪 LOGOUT (Optional: JWT is stateless)
@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'}), 200
