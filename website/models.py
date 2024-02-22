# This is the file to store all my database models
from flask_login import UserMixin  
from sqlalchemy.sql import func # using on the date
from . import db # importing from __init__(like importing from website)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    income_entries = db.relationship('Income', backref='user', lazy=True)
    expense_entries = db.relationship('Expense', backref='user', lazy=True)
    budget_entries = db.relationship('Budget', backref='user', lazy=True)

    def __init__(self, email, first_name, password):
        self.email = email
        self.first_name = first_name
        self.password = password

    
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   
    #initialize income parameters
    def __init__(self, amount, date, category, user_id):
        self.amount = amount
        self.date = date
        self.category = category
        self.user_id = user_id

    # serializing to json format
        
    def to_dict(self):
         return {
              'id': self.id,
            'amount': self.amount,
            'date': self.date.strftime('%Y-%m-%d'),  # format the date as a string
            'category': self.category,
            'user_id': self.user_id
         }

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    #initilize expense parameters
    def __init__(self, amount, date, category, user_id):
            self.amount = amount
            self.date = date
            self.category = category
            self.user_id = user_id

    # serializing to json format
    def to_dict(self):
         return {
              
         'id': self.id,
            'amount': self.amount,
            'date': self.date.strftime('%Y-%m-%d'),  # format the date as a string
            'category': self.category,
            'user_id': self.user_id
         }


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self, user_id, category, amount):
        self.user_id = user_id
        self.category = category
        self.amount = amount
    # serializing to json format
    def to_dict(self):
         return {
              'id': self.id,
              'category': self.category,
              'amount': self.amount,
              'user_id':self.user_id
         }
                                                                                  