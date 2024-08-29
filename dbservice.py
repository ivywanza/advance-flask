# from sqlalchemy import create_engine,Column,Integer,String,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/my-duka'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


class BaseModel(db.Model):
    __abstract__ = True

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)

class Product(BaseModel):
    __tablename__ = 'products'
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # relationships
    sales=relationship('Sale', backref='product_sales')

class Sale(BaseModel):
    __tablename__='sales'

    pid = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    amount_sold = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
class User(BaseModel):
    __tablename__='users'

    username = db.Column(db.String(80), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(80), nullable=False, unique=True)

    # relationship
    product=relationship('Product', backref='products')
    sale=relationship('Sale', backref='user_sales')

# db.create_all()