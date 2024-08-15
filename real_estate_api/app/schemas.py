# app/schemas.py

from app import ma
from app.models import User, Property, Application, Wishlist

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        load_instance = True

class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
    # Optionally, you can add custom fields or validation here if needed

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
        load_instance = True
