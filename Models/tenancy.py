# Application module
from extensions import db

class Tenancy(db.Model):
    """
    Tenancy Model

    Represents a tenancy in the Property Management system.

    Attributes:
        id (int): Primary key.
        property_id (int): Foreign key linking to Property.
        start_date (date): Start date of the tenancy.
        end_date (date, optional): End date of the tenancy.
        tenancy_status (str): Status of the tenancy (e.g., active, terminated).
        property (Property): One-to-many relationship to Property.
        tenant_tenancy (list[TenantTenancy]): Association table for many-to-many with Tenant.
        tenants (list[Tenant]): Many-to-many relationship to Tenant.

    Relationships:
        - Each Tenancy belongs to one Property.
        - Each Tenancy can have multiple Tenants through TenantTenancy.
    """
    __tablename__= "tenancy"

    id = db.Column(db.Integer,primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    tenancy_status = db.Column(db.String(50), nullable=False)

    # One-to-many back reference to Property
    property = db.relationship("Property", back_populates="tenancies")

    # Many-to-many: Tenancy <-> Tenant through TenantTenancy
    tenant_tenancy = db.relationship(
        "TenantTenancy",
        back_populates="tenancy",
        cascade="all, delete-orphan"
    )

    tenants = db.relationship(
        "Tenant",
        secondary="tenant_tenancy",
        back_populates="tenancies",
        overlaps="tenant_tenancy"
    )
