# Application module
from sqlalchemy.orm import validates
from marshmallow import ValidationError
from extensions import db

class SupportWorker(db.Model):
    """
    SupportWorker Model

    Represents a support worker in the Property Management system.

    Attributes:
        id (int): Primary key.
        name (str): Full name of the support worker.
        phone (str): Contact phone number (optional).
        email (str): Contact email address.
        tenant_support_worker (list[TenantSupportWorker]): Association table for many-to-many with tenants.
        tenants (list[Tenant]): Many-to-many relationship to Tenant.

    Relationships:
        - Each SupportWorker can be linked to multiple Tenants via TenantSupportWorker.
    """

    __tablename__= "support_worker"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50), nullable=False)

    @validates("email")
    def validate_email(self, value):
        """
    Validates the email field for the model.

    Ensures the provided value contains an "@" symbol, indicating a minimally
    valid email format. Raises a ValidationError if validation fails.
    
    """
        if "@" not in value:
            raise ValidationError("Invalid email address")

    # Many-to-many: SupportWorker <-> Tenant through TenantSupportWorker
    tenant_support_worker = db.relationship(
        "TenantSupportWorker",
        back_populates="support_worker",
        cascade="all, delete-orphan"
    )

    tenants = db.relationship(
        "Tenant",
        secondary="tenant_support_worker",
        back_populates="support_workers",
        overlaps="tenant_support_worker"
    )
