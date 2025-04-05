from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exit.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(200), default='/static/images/placeholder.jpg')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search', '')
    if query:
        # Search in both name and description, case-insensitive
        items = Item.query.filter(
            or_(
                Item.name.ilike(f'%{query}%'),
                Item.description.ilike(f'%{query}%')
            )
        ).all()
    else:
        items = Item.query.all()
    return render_template('marketplace.html', items=items, search_query=query)

@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        image_url = request.form['image_url']
        new_item = Item(name=name, description=description, price=price, category=category, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/marketplace')
    elif request.method == 'GET':
        # Get filter parameters from request
        categories = request.args.getlist('categories')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search_query = request.args.get('search', '')

        # Start with base query
        query = Item.query

        # Apply category filters if selected
        if categories:
            query = query.filter(Item.category.in_(categories))

        # Apply price range filters
        if min_price is not None:
            query = query.filter(Item.price >= min_price)
        if max_price is not None:
            query = query.filter(Item.price <= max_price)

        # Apply search filter if query exists
        if search_query:
            query = query.filter(
                or_(
                    Item.name.ilike(f'%{search_query}%'),
                    Item.description.ilike(f'%{search_query}%')
                )
            )

        # Execute query
        items = query.all()

        return render_template('marketplace.html', items=items, search_query=search_query)

    else:
        items = Item.query.all()
        return render_template('marketplace.html', items=items)

if __name__ == "__main__":
    app.run(debug=True)