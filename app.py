from flask import Flask, jsonify, make_response,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, ProductDescription, CartItem, Contact

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///product_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


# route for Product Description

@app.route('/products')
def products():

    products = []
    for product in ProductDescription.query.all():
        product_dict = {
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }
        products.append(product_dict)

    response = make_response(
        jsonify(products),
        200
    )

    return response


# Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    output = []
    for contact in contacts:
        contact_data = {'id': contact.id, 'name': contact.name, 'email': contact.email, 'message': contact.message}
        output.append(contact_data)
    return jsonify({'contacts': output,})



# Create a new contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.json
    new_contact = Contact(name=data['name'], email=data['email'], message=data['message'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact created successfully'})

# Update a contact
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    data = request.json
    contact.name = data['name']
    contact.email = data['email']
    contact.message = data['message']
    db.session.commit()
    return jsonify({'message': 'Contact updated successfully'})

# Delete a contact
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})

#Route for Cart
@app.route('/cart_items', methods=['GET'])
def get_cart_items():
    cart_items = []
    for item in CartItem.query.all():
        item_dict = {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity,
        }
        cart_items.append(item_dict)

    return jsonify(cart_items)

@app.route('/cart_items', methods=['POST'])
def add_to_cart():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    if not name or not price or not quantity:
        return jsonify({'error': 'Missing data!'}), 400

    new_item = CartItem(name=name, price=price, quantity=quantity)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added to cart successfully!'}), 201

@app.route('/cart_items/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    item = CartItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted from cart successfully!'})
    else:
        return jsonify({'error': 'Item not found!'}), 404

@app.route('/cart_items/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found!'}), 404

    data = request.json
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    if name:
        item.name = name
    if price:
        item.price = price
    if quantity:
        item.quantity = quantity

    db.session.commit()
    
    return jsonify({'message': 'Item updated successfully!'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)