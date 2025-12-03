from extensions import db

class Property(db.Model):
    __tablename__= "property"

    id = db.Column(db.Integer, primary_key=True)
    property_manager_id = db.Column(db.Integer, db.ForeignKey("property_manager.id"))
    address = db.Column(db.String(50), nullable=False)
