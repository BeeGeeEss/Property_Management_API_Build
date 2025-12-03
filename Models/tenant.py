from extensions import db

class Tenant(db.Model):
    # define the table name for the db
    __tablename__= "tenant"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))
