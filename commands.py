from main import db
from flask import Blueprint
from Models.property_manager import PropertyManager
from Models.property import Property
from Models.support_worker import SupportWorker
from Models.tenancy import Tenancy
from Models.tenant_support_worker import TenantSupportWorker
from Models.tenant_tenancy import TenantTenancy
from Models.tenant import Tenant

db_commands = Blueprint("db", __name__)

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped!")

# create app's cli command named create, then run it in the terminal as "flask db create", 
# it will invoke create_db function
@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands .cli.command("seed")
def seed_db():
    # SEED PROPERTY MANAGER
    # create the PropertyManager object
    property_manager1 = PropertyManager(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name="Rachael Ruhs",
        phone="0400001001",
        email="RR1@CPM.org"
    )
    # Add the object as a new row to the table
    db.session.add(property_manager1)

    property_manager2 = PropertyManager(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name="Justine Gait",
        phone="0400002002",
        email="JG2@CPM.org"
    )
    # Add the object as a new row to the table
    db.session.add(property_manager2)

    property_manager3 = PropertyManager(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        name="Ange Clegg",
        phone="0400003003",
        email="AC3@CPM.org"
    )
    # Add the object as a new row to the table
    db.session.add(property_manager3)

    # SEED PROPERTY

    property1 = Property(
        address="42 Dandelion Road, Mildura, Vic, 3500"
    )
    # Add the object as a new row to the table
    db.session.add(property1)

    property2 = Property(
        address="56 Rubarb Court, Merbein, Vic, 3501"
    )
    db.session.add(property2)
    
    property3 = Property(
        address="100 Pterodactyl Close, Swan Hill, Vic, 3585"
    )
    db.session.add(property3)

    
    # SEED SUPPORT WORKER

    support_worker1 = SupportWorker(
        name="Sue Slime",
        phone="0412345678",
        email="SS@help.org"
    )
    # Add the object as a new row to the table
    db.session.add(support_worker1)

    support_worker2 = SupportWorker(
        name="Janis Joplin",
        phone="0487654321",
        address="JJ@MH.org"
    )
    db.session.add(support_worker2)
    
    support_worker3 = SupportWorker(
        name="Peter Paulson",
        phone="0487654321",
        address="PP@AOD.org"
    )
    db.session.add(support_worker3)


# SEED TENANCY

    tenancy1 = Tenancy(
        start_date="2025-12-05",
        tenancy_status="Sign-Up"
    )
    # Add the object as a new row to the table
    db.session.add(tenancy1)

    tenancy2 = Tenancy(
        start_date="2006-10-09",
        end_date="2025-11-28",
        tenancy_status="Vacant"
    )
    db.session.add(tenancy2)
    
    tenancy3 = Tenancy(
        start_date="2019-05-01",
        tenancy_status="Tenanted"
    )
    db.session.add(tenancy3)


    # SEED TENANT

    tenant1 = Tenant(
        name="James Arquette",
        date_of_birth="1973-06-25",
        phone="0417678900",
        address="1 Banana Grove, Mildura, Vic, 3500"
    )
    # Add the object as a new row to the table
    db.session.add(tenant1)

    tenant2 = Tenant(
        name="June Harris",
        date_of_birth="1966-03-12",
        phone="0400345678",
        address="55 Happy Lane, Irymple, Vic, 3498"
    )
    db.session.add(tenant2)
    
    tenant3 = Tenant(
        name="Paula Deakin",
        date_of_birth="1990-07-14",
        phone="0438987654",
        address="789 Jupiter Way, Red Cliffs, Vic, 3496"
    )
    db.session.add(tenant3)
    
    # commit the changes
    db.session.commit()
    print("Table seeded")


# @db_commands .cli.command("drop")
# def drop_db():
#     db.drop_all()
#     print("Tables dropped!")