from datetime import date, datetime,timedelta
import json
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)

db = SQLAlchemy(app)


#--------------------------------------------------------Models------------------------------------------------------------- 

# Model for the books 
class Book(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    book_author = db.Column(db.String(50))
    book_year = db.Column(db.String(10))
    book_type = db.Column(db.String(200))
    loans = db.relationship('Loan', backref='book', cascade='all, delete')

    def __init__(self, book_name, book_author, book_year, book_type):
        self.book_name = book_name
        self.book_author = book_author
        self.book_year = book_year
        self.book_type = book_type

    def to_dict(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'book_author': self.book_author,
            'book_year': self.book_year,
            'book_type': self.book_type
        }

# Model for the customers 
class Customer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cust_name = db.Column(db.String(100))
    cust_city = db.Column(db.String(50))
    cust_age = db.Column(db.Integer)
    loans = db.relationship('Loan', backref='customer', cascade='all, delete')

    def __init__(self, cust_name, cust_city, cust_age):
        self.cust_name = cust_name
        self.cust_city = cust_city
        self.cust_age = cust_age

    def to_dict(self):
        return {
            'id': self.id,
            'cust_name': self.cust_name,
            'cust_city': self.cust_city,
            'cust_age': self.cust_age
        }

# Model for the loans 
class Loan(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loanDate = db.Column(db.String(20))
    returnDate = db.Column(db.String(20))

    def __init__(self, cust_id, book_id, loanDate, returnDate):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loanDate = loanDate
        self.returnDate = returnDate

    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'loanDate': self.loanDate,
            'returnDate': self.returnDate
        }
        

#-----------------------------------------------Routes-------------------------------------------------------



# home page
@app.route('/')
def index():
    return render_template('index.html')

# get all books
@app.route("/books", methods=['GET'])
def get_books():
    books_list = [book.to_dict() for book in Book.query.all()]
    json_data = json.dumps(books_list)
    return json_data

# get books by ID
@app.route("/books/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return {'error': 'Book not found'}, 404

    return book.to_dict()

# get all customers
@app.route("/customers", methods=['GET'])
def get_customers():
    customers_list = [customer.to_dict() for customer in Customer.query.all()]
    json_data = json.dumps(customers_list)
    return json_data

# get all loans
@app.route("/loans", methods=['GET'])
def get_loans():
    loans_list = [loan.to_dict() for loan in Loan.query.all()]
    json_data = json.dumps(loans_list)
    return json_data

# delete a book by ID
@app.route("/books/del/<id>", methods=['DELETE'])
def del_book(id=-1):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return {"delete": "success"}

# delete a customer by ID
@app.route("/customers/del/<id>", methods=['DELETE'])
def del_customer(id=-1):
    customer = Customer.query.get_or_404(id)

    # check if the customer has any loans
    if customer.loans:
        return {"error": "Cannot delete customer, since they have books loaned."}, 400

    # if the customer has no loans, delete them
    db.session.delete(customer)
    db.session.commit()
    return {"delete": "success"}

# delete a loan by ID
@app.route("/loans/del/<id>", methods=['DELETE'])
def del_loan(id=-1):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return {"delete": "success"}

# update a book by ID
@app.route("/books/upd/<id>", methods=['PUT'])
def upd_book(id=-1):
    book = Book.query.get(id)
    data = request.get_json()
    book.book_author = data['book_author']
    book.book_name = data['book_name']
    book.book_year = data['book_year']
    book.book_type = data['book_type']
    db.session.commit()
    return {"update": "success"}

# update a customer by ID
@app.route("/customers/upd/<id>", methods=['PUT'])
def upd_customer(id=-1):
    customer = Customer.query.get(id)
    data = request.get_json()
    customer.cust_name = data['cust_name']
    customer.cust_city = data['cust_city']
    customer.cust_age = data['cust_age']
    db.session.commit()
    return {"update": "success"}

# create a new book record
@app.route('/books/new', methods=['POST'])
def new_book():
    data = request.get_json()
    book_name = data['book_name']
    book_author = data['book_author']
    book_year = data['book_year']
    book_type = data['book_type']

    new_book = Book(book_name, book_author, book_year, book_type)
    db.session.add(new_book)
    db.session.commit()
    return "A new book record was created."

# create a new customer record
@app.route('/customers/new', methods=['POST'])
def new_customer():
    data = request.get_json()
    cust_name = data['cust_name']
    cust_city = data['cust_city']
    cust_age = data['cust_age']

    new_customer = Customer(cust_name, cust_city, cust_age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new customer record was created."

# create a new loan record
@app.route('/loans/new', methods=['POST'])
def new_loan():
    data = request.get_json()
    cust_id = data['cust_id']
    book_id = data['book_id']
    book_type = str(data['book_type'])

    # Check if the book and customer exists
    book = Book.query.get(book_id)
    customer = Customer.query.get(cust_id)
    if customer is None:
        return {'error': 'Invalid ID'}, 400
    elif book is None: 
        return {'error': 'Invalid ID'}, 400
    

    # Check if the book is already loaned
    loaned_book = Loan.query.filter_by(book_id=book_id).first()
    if loaned_book is not None:
        return {'error': 'The book is already loaned'}, 400

    # Perform loan creation
    loanDate = datetime.now().strftime('%Y-%m-%d')
    if book_type == '1':
        returnDate = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    elif book_type == '2':
        returnDate = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    elif book_type == '3':
        returnDate = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    else:
        return {'error': 'Invalid book type'}, 400

    new_loan = Loan(cust_id, book_id, loanDate, returnDate)
    db.session.add(new_loan)
    db.session.commit()
    return "A new loan record was created."

# search for books by book name or author
@app.route('/books/search/<string:query>', methods=['GET'])
def search_books(query):
    # Convert the query to lowercase and add wildcards
    search_query = f'%{query.lower()}%'
    books_list = [book.to_dict() for book in Book.query.filter(func.lower(Book.book_name).like(search_query)).all()]
    json_data = json.dumps(books_list)
    return json_data

# search for customers by name
@app.route("/customers/search/<string:query>", methods=['GET'])
def search_customers(query):
    # Convert the query to lowercase and add wildcards
    search_query = f'%{query.lower()}%'
    customers_list = [customer.to_dict() for customer in Customer.query.filter(func.lower(Customer.cust_name).like(search_query)).all()]
    json_data = json.dumps(customers_list)
    return json_data

# get all overdue books based on return date
@app.route('/books-overdue', methods=['GET'])
def get_books_overdue():
    today = date.today().strftime('%Y-%m-%d')
    overdue_books = db.session.query(Book, Loan.returnDate, Loan.cust_id)\
                    .join(Loan, Book.id == Loan.book_id)\
                    .join(Customer, Loan.cust_id == Customer.id)\
                    .filter(Loan.returnDate < today)\
                    .all()

    books_list = []
    for book, returnDate, cust_id in overdue_books:
        book_dict = book.to_dict()
        book_dict['returnDate'] = returnDate
        book_dict['cust_id'] = cust_id
        book_dict['book_id'] = book.id    
        books_list.append(book_dict)

    json_data = json.dumps(books_list)
    return json_data

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
