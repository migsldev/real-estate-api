from app import db
from datetime import datetime
from sqlalchemy.orm import backref

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('agent', 'property_owner', 'buyer', name='user_roles'), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True, cascade="all, delete-orphan")
    applications = db.relationship('Application', backref='applicant', lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship('Wishlist', backref='user', lazy=True, cascade="all, delete-orphan")

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    listed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applications = db.relationship('Application', backref=backref('property', passive_deletes=True), lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship('Wishlist', backref=backref('property', passive_deletes=True), lazy=True, cascade="all, delete-orphan")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='application_status'), nullable=False, default='pending')
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
