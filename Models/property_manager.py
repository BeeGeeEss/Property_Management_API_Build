from extensions import db

class PropertyManager(db.Model):
    __tablename__ = "property_manager"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    # One-to-many: PropertyManager -> Property
    properties = db.relationship(
        "Property",
        back_populates="property_manager",
        cascade="all, delete",
        passive_deletes=True
    )
