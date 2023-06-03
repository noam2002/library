# Library Management System

Welcome to the Library Management System! Our platform is built using SQLAlchemy, Flask, and JSON to offer a seamless experience for managing books, customers, and loans.

## Features

Our Library Management System offers the following features:

- Add new books, customers, and loans
- Search books and customers by name
- View loans data
- Show overdue books

## Installation

To install the Library Management System on your local machine, follow these steps:

1. Clone this repository to your local machine
2. Create a virtual environment using virtualenv or conda using `py -3 -m venv env`      
3. Activate the virtual environment `.\env\Scripts\activate`
4. Install the required dependencies using `pip install -r requirements.txt`
5. Start the Flask server using `python app.py`
6. Access the application in your web browser at [http://localhost:5000]

## Usage

Once the application is running, you can use the following endpoints to access its features:

- `/books`: Add new books, search books by name
- `/customers`: Add new customers, search customers by name
- `/loans`: View loans data, add new loans, show overdue books

## Credits

The Library Management System was created by Noam Tyberg as a project for FS Python.

