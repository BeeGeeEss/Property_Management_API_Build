from main import db
from sqlalchemy.sql import func

class PropertyManager(db.Model):
    __tablename__ = "property_manager"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # RELATIONSHIPS
    properties = db.relationship("Property", back_populates="property_manager")