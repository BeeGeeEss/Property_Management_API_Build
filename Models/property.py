# Application module
from extensions import db

class Property(db.Model):
    """
    Property Model

    Represents a property in the Property Management system.

    Attributes:
        id (int): Primary key.
        address (str): Property address.
        property_manager_id (int): Foreign key linking to PropertyManager.
        property_manager (PropertyManager): One-to-many relationship to the manager.
        tenancies (list[Tenancy]): One-to-many relationship with Tenancy.

    Relationships:
        - Each Property is managed by one PropertyManager.
        - Each Property can have multiple Tenancies.
    """
    __tablename__= "property"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)

    property_manager_id = db.Column(db.Integer, db.ForeignKey("property_manager.id"), nullable=False)

    # One-to-many back reference to PropertyManager
    property_manager = db.relationship("PropertyManager", back_populates="properties")

    # One-to-many: Property -> Tenancy
    tenancies = db.relationship(
        "Tenancy",
        back_populates="property",
        cascade="all, delete",
        passive_deletes=True
    )
