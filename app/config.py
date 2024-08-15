import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///real_estate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')
