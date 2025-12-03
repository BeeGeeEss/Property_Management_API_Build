from main import db
from sqlalchemy.sql import func

class Property(db.Model):
    __tablename__= "property"

    id = db.Column(db.Integer, primary_key=True)
    property_manager_id = db.Column(db.Integer, db.ForeignKey("property_manager.id"))
    address = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # RELATIONSHIP
    property_manager = db.relationship("PropertyManager", back_populates="properties")

    # One property → many tenancies
    tenancies = db.relationship("Tenancy", back_populates="property")