from extensions import db

class TenantTenancy(db.Model):
    # define the table name for the db
    __tablename__= "tenant_tenancy"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id"))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))
