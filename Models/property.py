from extensions import db

class Property(db.Model):
    __tablename__= "property"

    id = db.Column(db.Integer, primary_key=True)
    property_manager_id = db.Column(db.Integer, db.ForeignKey("property_manager.id"), nullable=False)
    address = db.Column(db.String(50), nullable=False)
   
 # One-to-many backref
    manager = db.relationship("PropertyManager", back_populates="properties")
    
    # One-to-many: Property -> Tenancy
    tenancies = db.relationship(
        "Tenancy",
        back_populates="property",
        cascade="all, delete",
        passive_deletes=True
    )