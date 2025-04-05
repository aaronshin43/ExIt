from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, DataRequired
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_wtf.file import MultipleFileField
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exit.db'
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('ItemImage', backref='item', lazy=True)

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200))
    items = db.relationship('Item', backref='seller', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw=({"placeholder": "Username"}))
    email = StringField(validators=[InputRequired()], render_kw=({"placeholder": "Email"}))
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw=({"placeholder": "Password"}))
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords must match")], render_kw=({"placeholder": "Confirm Password"}))
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        
        if existing_username:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        if not email.data.endswith('dickinson.edu'):
            raise ValidationError('Please use your Dickinson email address')
        
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already registered')

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired()], render_kw=({"placeholder": "Email"}))
    password = PasswordField(validators=[InputRequired()], render_kw=({"placeholder": "Password"}))
    submit = SubmitField("Login")

class ItemForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw=({"placeholder": "Item Name"}))
    description = TextAreaField(validators=[InputRequired()], render_kw=({"placeholder": "Description"}))
    price = IntegerField(validators=[InputRequired()], render_kw=({"placeholder": "Price"}))
    category = SelectField('Category', choices=[
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('furniture', 'Furniture'),
        ('mensclothing', 'Men\'s Clothing'),
        ('womensclothing', 'Women\'s Clothing'),
        ('others', 'Others')
    ], validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Upload Item')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    if request.method == 'GET':
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user: 
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('marketplace'))
            else:
                flash('Invalid email or password', 'error')
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    form = ItemForm()  # Create an instance of the form

    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            user_id=current_user.id,
        )
        db.session.add(new_item)
        db.session.commit()

        # Handle image uploads
        if form.images.data:
            for image in form.images.data:
                if image:
                    filename = f"{new_item.id}_{image.filename}"
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    item_image = ItemImage(
                        item_id=new_item.id,
                        image_path=filename
                    )
                    db.session.add(item_image)
            db.session.commit()
            print("Images saved successfully" + filename + " to " + image_path)
        flash('Item created successfully!', 'success')
        return redirect(url_for('marketplace'))

    return render_template('sell.html', form=form)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get_or_404(item_id) 
    return render_template('itemdetails.html', item=item, images=item.images)

if __name__ == "__main__":
    app.run(debug=True)