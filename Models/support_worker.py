from extensions import db

class SupportWorker(db.Model):
    # define the table name for the db
    __tablename__= "support_worker"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    support_worker_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50), nullable=False)
