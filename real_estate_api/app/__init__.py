from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Add this import
from app.config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()  # Initialize the migrate variable

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with your app and db

    with app.app_context():
        db.create_all()

    from app.routes import main
    app.register_blueprint(main)

    return app
