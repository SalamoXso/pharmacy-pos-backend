from flask import Blueprint, jsonify, request
from app import db
from app.models import User, Medicine, Sale, SaleItem
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'quantity': m.quantity,
        'price': m.price,
        'expiry_date': m.expiry_date.isoformat(),
        'category': m.category
    } for m in medicines])

@main_bp.route('/api/medicines', methods=['POST'])
def add_medicine():
    data = request.get_json()
    new_medicine = Medicine(
        name=data['name'],
        description=data.get('description', ''),
        quantity=data['quantity'],
        price=data['price'],
        expiry_date=data['expiry_date'],
        category=data.get('category', '')
    )
    db.session.add(new_medicine)
    db.session.commit()
    return jsonify({'message': 'Medicine added successfully!'}), 201

@main_bp.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    user_id = data['user_id']
    items = data['items']

    total_amount = sum(item['quantity'] * item['price'] for item in items)

    new_sale = Sale(user_id=user_id, total_amount=total_amount, date=datetime.utcnow())
    db.session.add(new_sale)
    db.session.commit()

    for item in items:
        sale_item = SaleItem(
            sale_id=new_sale.id,
            medicine_id=item['medicine_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(sale_item)
        db.session.commit()

    return jsonify({'message': 'Sale created successfully!', 'sale_id': new_sale.id}), 201