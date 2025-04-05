from app import app, db, User, Item, bcrypt
from flask_login import UserMixin

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create sample users
        user1 = User(
            username='john_doe',
            email='test@dickinson.edu',
            password=bcrypt.generate_password_hash('12341234').decode('utf-8')
        )
        
        user2 = User(
            username='jane_smith',
            email='test2@dickinson.edu',
            password=bcrypt.generate_password_hash('12341234').decode('utf-8')
        )
        
        # Add users to database
        db.session.add(user1)
        db.session.add(user2)
        
        # Create sample items
        items = [
            Item(
                name='iPhone 13 Pro',
                description='Excellent condition, comes with original box and accessories',
                price=699.99,
                category='Electronics',
                user_id=1,
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Calculus Textbook',
                description='Calculus: Early Transcendentals, 8th Edition, barely used',
                price=45.00,
                category='Books',
                user_id=1,
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Desk Chair',
                description='Ergonomic office chair, adjustable height',
                price=75.00,
                category='Furniture',
                user_id=2,
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Nike Hoodie',
                description='Black Nike hoodie, size M, like new',
                price=35.00,
                category='Mensclothing',
                user_id=2,
                image_url='/static/images/placeholder.jpg'
            ),
            Item(
                name='Leather Bag',
                description='Genuine leather tote bag, perfect condition',
                price=85.00,
                category='Womensclothing',
                user_id=1,
                image_url='/static/images/placeholder.jpg'
            )
        ]
        
        # Add items to database
        for item in items:
            db.session.add(item)
        
        # Commit all changes
        db.session.commit()
        print("Database reset successfully!")

if __name__ == '__main__':
    reset_database()