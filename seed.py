from app import app
from models import db, ProductDescription, CartItem, Contact

with app.app_context():

    # Clear existing data
    ProductDescription.query.delete()
    CartItem.query.delete()
    Contact.query.delete()

    # Create instances of ProductDescription
    products = [
        ProductDescription(name='Lipstick', price=15.0, description='Long-lasting matte lipstick'),
        ProductDescription(name='Facial Mask', price=25.0, description='Hydrating and rejuvenating mask'),
        ProductDescription(name='Perfume', price=50.0, description='Elegant floral scent')
    ]

    # Create instances of CartItem
    cart_items = [
        CartItem(name='Hairbrush', price=10.0, quantity=2),
        CartItem(name='Nail Polish', price=8.0, quantity=3),
        CartItem(name='Makeup Palette', price=45.0, quantity=1)
    ]

    # Create instances of Contact
    contacts = [
        Contact(name='John Doe', email='john@example.com', message='Hello, world!'),
        Contact(name='Jane Doe', email='jane@example.com', message='Nice to meet you!')
    ]

    # Add instances to the database
    db.session.add_all(products)
    db.session.add_all(cart_items)
    db.session.add_all(contacts)

    db.session.commit()
