from flask import Flask,jsonify,request
from flask_cors import CORS
from sqlalchemy import func
from dbservice import *
# from flask_sqlalchemy import SQLAlchemy


# creating a flask instance
# app=Flask(__name__)

# enabling cross-origin resource sharing
CORS(app)

# creating a database connection

# db=SQLAlchemy(app)

@app.route('/products', methods=['GET','POST'])
def products():
    if request.method=='POST':
        try:
            data=request.json

            existing_product=db.session.query(Product).filter(Product.product_name==data['product_name'],
                                                      Product.product_price==data['product_price'],
                                                      Product.uid==data['uid']).first()
            
            if existing_product:
                return jsonify({'error': 'product already exists!'}),409
            
            new_product=Product(
                uid=data['uid'],
                product_name=data['product_name'],
                product_price=data['product_price'],
                stock_quantity=data['stock_quantity']
            )
            db.session.add(new_product)
            db.session.commit()
            db.session.refresh(new_product)
            
            return jsonify({'product added succesfully!':new_product.id}),201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error adding product': str(e)}),500
        
    elif request.method=='GET':
        try:
            products=db.session.query(Product).all()
            prods=[]
            for product in products:
                prods.append({
                "id":product.id,
                "uid":product.uid,
                "product_name":product.product_name,
                "product_price":product.product_price,
                "stock_quantity":product.stock_quantity
            })
            return jsonify({"products": prods}),200
        
        except Exception as e:
            return jsonify({'error fetching products': str(e)}),500
        
@app.route('/sales', methods=['POST','GET'])
def sales():
    if request.method=='POST':
        try:
            data=request.json

            # created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
            existing_sale=db.session.query(Sale).filter(Sale.pid==data['pid'], Sale.amount_sold==data['amount_sold']).first()

            if existing_sale:
                return jsonify({'error':'sale already exists!'}),409

            new_sale=Sale(
                pid=data['pid'],
                uid=data['uid'],
                amount_sold=data['amount_sold']
            )
            db.session.add(new_sale)
            db.session.commit()
            db.session.refresh(new_sale)

            return jsonify({'sale created succesfully !,Sale id': new_sale.id }) ,201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error creating sale': str(e)}) ,500
        
    elif request.method=='GET':
        try:
            sales=db.session.query(Sale).all()
            salelist=[]
            for sale in sales:
                salelist.append({
                    "id":sale.id,
                    "pid": sale.pid,
                    "uid":sale.uid,
                    "created_at":sale.created_at,
                    "amount_sold":sale.amount_sold
                })
            return jsonify({'sales ': salelist}),200
        
        except Exception as e:
            return jsonify({'error fetching sales': str(e) }), 500
        

@app.route('/users', methods=['POST','GET'])
def users():
    if request.method=='POST':
        try:
            data=request.json
            existing_user=db.session.query(User).filter(User.user_email==data['user_email']).first()

            if existing_user:
                return jsonify({'error adding user': 'user already exists'}),409
            
            new_user=User(
                username=data['username'],
                user_email=data['user_email'],
                user_password=data['user_password']
            )
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            
            return jsonify({'user added succesfully !': new_user.id}) ,201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error registering user': str(e)}),500


    if request.method=='GET':
        try:
            users=db.session.query(User).all()
            userlist=[]
            for i in users:
                userlist.append({
                    "id": i.id,
                    "username": i.username,
                    "user_password": i.user_password ,
                    "user_email": i.user_email
                    })
            
            return jsonify(userlist), 200
            # return jsonify(users) ,200

        except Exception as e:
            return jsonify({'error fetching users ': str(e)}),500
        
@app.route('/dashboard')
def dashboard():
    # sales per day...it returns a list of tuples...each tuple contains two values,date and total_sales
    sales_per_day= db.session.query(
        func.date(Sale.created_at).label('date'),
        func.sum(Sale.amount_sold * Product.product_price).label("total_sales")
        ).join(Product).group_by(
            func.date(Sale.created_at)
        ).all()
    
    sales_data= [ {'date':str(day),"total_sales": sales } for day, sales in sales_per_day]
    
    
    return jsonify({'sales_data':sales_data})

















# current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(current_timestamp)

if __name__=='__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)

    
    
