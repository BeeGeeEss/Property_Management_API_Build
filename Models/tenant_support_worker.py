# Application module
from extensions import db

class TenantSupportWorker(db.Model):
    """
    TenantSupportWorker Model

    Association (junction) table representing the many-to-many relationship
    between Tenants and SupportWorkers in the Property Management system.

    Attributes:
        id (int): Primary key.
        rank (int, optional): Optional ranking or priority for the support worker assignment.
        support_worker_id (int): Foreign key linking to SupportWorker.
        tenant_id (int): Foreign key linking to Tenant.
        tenant (Tenant): Relationship to the Tenant model.
        support_worker (SupportWorker): Relationship to the SupportWorker model.

    Relationships:
        - Many-to-many relationship between Tenant and SupportWorker through this table.
        - Uses back_populates and overlaps to maintain ORM consistency.
    """

    __tablename__= "tenant_support_worker"

    id = db.Column(db.Integer,primary_key=True)
    rank = db.Column(db.Integer)
    support_worker_id = db.Column(db.Integer, db.ForeignKey("support_worker.id", ondelete="CASCADE"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False)

    tenant = db.relationship(
        "Tenant",
        back_populates="tenant_support_worker",
        overlaps="tenants, support_workers"
    )
    support_worker = db.relationship(
        "SupportWorker",
        back_populates="tenant_support_worker",
        overlaps="tenants, support_workers"
    )
