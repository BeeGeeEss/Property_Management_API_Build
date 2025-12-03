from main import db

class Property(db.Model):
    # define the table name for the db
    __tablename__= "property"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    property_manager_id = db.Column(db.Integer, db.ForeignKey("property_manager.id"))
    address = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    property_manager = db.relationship("property_manager", back_populates="property")