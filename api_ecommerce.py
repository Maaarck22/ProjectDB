from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uroot:123@localhost:3306/TEST'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/e_commerce'

db = SQLAlchemy(app)

# >>>> curl -v http://localhost:5000/customer/1  

# Model for Customers  
class Customers(db.Model):
    CustomerID =  db.Column(db.Integer, primary_key = True)
    Customer_first_name = db.Column(db.String(20))
    Customer_last_name = db.Column(db.String(20))
    Customer_phone_number = db.Column(db.String(10))
    Customer_email = db.Column(db.String(30))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, Customer_first_name, Customer_last_name,Customer_phone_number,Customer_email):
        self.Customer_first_name = Customer_first_name
        self.Customer_last_name = Customer_last_name
        self.Customer_phone_number = Customer_phone_number
        self.Customer_email = Customer_email
    
    def __repr__(self):
        return '<Customers %d>' % self.CustomerID

# Model for Products
class Products(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    Product_name = db.Column(db.String(50))
    Description = db.Column(db.String(200))
    Category = db.Column(db.String(20))
    Price = db.Column(db.Float)
    Availability = db.Column(db.String(20))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, Product_name, Description, Category,Price, Availability):
        self.Product_name = Product_name
        self.Description = Description
        self.Category = Category
        self.Price = Price
        self.Availability = Availability

    def __repr__(self):
        return '<Products %d>' % self.ProductID


# Model for Sellers
class Sellers(db.Model):
    SellerID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    Product = db.relationship('Products', backref=db.backref('sellers', lazy=True))
    Seller_first_name = db.Column(db.String(20))
    Seller_last_name = db.Column(db.String(20))
    Seller_phone_number = db.Column(db.String(20))
    Seller_rating = db.Column(db.Float)
    

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, ProductID, Description, Seller_first_name, Seller_last_name, Seller_phone_number, Seller_rating):
        self.ProductID = ProductID
        self.Description = Description
        self.Seller_first_name = Seller_first_name
        self.Seller_last_name = Seller_last_name
        self.Seller_phone_number = Seller_phone_number
        self.Seller_rating = Seller_rating
 
    def __repr__(self):
        return '<Sellers %d>' % self.SellerID

# Model for Sellers
class Reviews(db.Model):
    ReviewID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=False)
    Product = db.relationship('Products', backref=db.backref('sellers', lazy=True))
    Seller_first_name = db.Column(db.String(20))
    Seller_last_name = db.Column(db.String(20))
    Seller_phone_number = db.Column(db.String(20))
    Seller_rating = db.Column(db.Float)
    

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, ProductID, Description, Seller_first_name, Seller_last_name, Seller_phone_number, Seller_rating):
        self.ProductID = ProductID
        self.Description = Description
        self.Seller_first_name = Seller_first_name
        self.Seller_last_name = Seller_last_name
        self.Seller_phone_number = Seller_phone_number
        self.Seller_rating = Seller_rating
 
    def __repr__(self):
        return '<Sellers %d>' % self.SellerID

with app.app_context():
    db.create_all()

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Customers
        sqla_session = db.session
        
    CustomerID = fields.Number(dump_only = True)
    Customer_first_name = fields.String(required = True)
    Customer_last_name = fields.String(required = True)
    Customer_phone_number = fields.String(required = True)
    Customer_email= fields.String(required = True)

@app.route('/customers', methods = ['GET'])
def get_customers():
    get_customers_list = Customers.query.all()
    customer_schema =CustomerSchema(many = True)
    customers = customer_schema.dump(get_customers_list)
    return make_response(jsonify({"customers": customers}))

# Route to retrieve an author by ID
@app.route('/customer/<int:CustomerID>', methods = ['GET'])
def get_customer(CustomerID):
    customer = Customers.query.get(CustomerID)
    if customer:
        customer_schema =CustomerSchema()
        customer_json = customer_schema.dump(customer)
        return jsonify(customer_json),200
    else:
        return jsonify({'message': 'Customer not found'}), 404

# >>> curl -X POST -H "Content-Type:application/json" -d "{\"Customer_first_name\":\"Marck\", \"Customer_last_name\":\"Chiza\", \"Customer_phone_numer\":\"0932456432\", \"Customer_email\":\"marck@gmail.com\"}" http://127.0.0.1:5000/Customers.0.1:5000/customers

@app.route('/customers', methods = ['POST', 'POST'])
def create_customer():
    #Parse JSON data from the request
    customer_data = request.json
    
    #Validate and deserialize JSON data using AuthorSchema
    try:
        new_customer_data = CustomerSchema().load(customer_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Create a new Author instance using the deserialized data 
    new_customer = Customers(**new_customer_data)
    
    # Add the new customer to the database
    try:
        db.session.add(new_customer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    # Serialize the created author and return the response
    customer_schema = CustomerSchema()
    customer_json = customer_schema.dump(new_customer)
    return jsonify(customer_json), 201

# Route to UPDATE an author by ID
# curl -X PUT -H "Content-Type:application/json" -d "{\"name\":\"Author A-Update\", \"specialisation\":\"Java\"}" http://127.0.0.1:5000/author/1

@app.route('/customer/<int:CustomerID>', methods=['PUT'])
def update_customer(CustomerID):
    customer = customer.query.get(CustomerID) 
    if customer:
        data = request.get_json()
        customer.customer_first_name = data.get('Customer first name', customer.customer_first_name)
        customer.customer_last_name = data.get('Customer last name', customer.customer_last_name)
        customer.customer_phone_number = data.get('Customer phone number', customer.customer_phone_number)
        customer.customer_email = data.get('Customer email', customer.customer_email)
        db.session.commit()
        return jsonify({'message': 'Customer update succesfully'}), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Route to DELETE an author by ID
# >>>> curl -X DELETE -H "Content-Type:application/json" -d "{\"name\":\"Author A-Update\", \"specialisation\":\"Java\"}" http://127.0.0.1:5000/author/1

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(CustomerID):
    customer = Customers.query.get(CustomerID)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer delete successfully'})
    else:
        return jsonify({'message': 'Customer not found'})

if __name__ == "__main__":
    app.run(debug=True)