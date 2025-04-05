from app import app, db
from app import Item

def init_db():
    with app.app_context():
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Sample items
        sample_items = [
            Item(
                name='iPhone 13 Pro',
                description='Excellent condition',
                price=699.99,
                category='electronics',
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Calculus Textbook',
                description='Calculus: Early Transcendentals, 8th Edition',
                price=45.00,
                category='books',
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Desk Chair',
                description='Ergonomic office chair',
                price=75.00,
                category='furniture',
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Nike Hoodie',
                description='Black Nike hoodie, size M, like new',
                price=35.00,
                category='mensclothing',
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Leather Bag',
                description='perfect condition',
                price=85.00,
                category='womensclothing',
                image_url='/static/images/placeholder.jpg'
            )
        ]
            
        # Add items to database
        for item in sample_items:
            db.session.add(item)
        
        # Commit the changes
        db.session.commit()

if __name__ == "__main__":
    init_db()