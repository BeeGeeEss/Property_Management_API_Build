"""
Database CLI commands for Flask app.

Provides commands to:
- drop all tables
- create all tables
- seed the database with initial data

"""
# Standard library imports
from datetime import date

# Third-party imports
from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Application module
from extensions import db
from Models.property_manager import PropertyManager
from Models.property import Property
from Models.support_worker import SupportWorker
from Models.tenancy import Tenancy
from Models.tenant import Tenant
from Models.tenant_tenancy import TenantTenancy
from Models.tenant_support_worker import TenantSupportWorker

# Blueprint for database commands
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("drop")
def drop_db():
    """Drop all tables in the database."""
    db.drop_all()
    print("Tables dropped!⬇️")

# create app's cli command named create, then run it in the terminal as "flask db create".
# it will invoke create_db function
@db_commands.cli.command("create")
def create_db():
    """Create all tables in the database."""
    db.create_all()
    print("Tables created!✅")

@db_commands.cli.command("seed")
def seed_db():
    """
    Seed the database with initial data.

    Seeds the following tables:
    - PropertyManager
    - Property
    - SupportWorker
    - Tenancy
    - Tenant
    - TenantTenancy
    - TenantSupportWorker
    """
    # SEED PROPERTY MANAGER
    property_manager1 = PropertyManager(

        name="Janice Justice",
        phone="0400001001",
        email="JJ1@CPM.org"
    )
    db.session.add(property_manager1)

    property_manager2 = PropertyManager(

        name="Rita Philbara",
        phone="0400002002",
        email="RP2@CPM.org"
    )
    db.session.add(property_manager2)

    property_manager3 = PropertyManager(

        name="Angel Custers",
        phone="0400003003",
        email="AC3@CPM.org"
    )
    try:
        db.session.add(property_manager3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    # SEED PROPERTY
    property1 = Property(
        address="42 Dandelion Road, Mildura, Vic, 3500",
        property_manager_id=property_manager1.id
    )
    db.session.add(property1)

    property2 = Property(
        address="56 Rubarb Court, Merbein, Vic, 3501",
        property_manager_id=property_manager2.id
    )
    db.session.add(property2)

    property3 = Property(
        address="100 Pterodactyl Close, Swan Hill, Vic, 3585",
        property_manager_id=property_manager3.id
    )
    try:
        db.session.add(property3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500



    # SEED SUPPORT WORKER
    support_worker1 = SupportWorker(
        name="Sue Slime",
        phone="0412345678",
        email="SS@help.org"
    )
    db.session.add(support_worker1)

    support_worker2 = SupportWorker(
        name="Janis Joplin",
        phone="0487654321",
        email="JJ@MH.org"
    )
    db.session.add(support_worker2)

    support_worker3 = SupportWorker(
        name="Peter Paulson",
        phone="0487654321",
        email="PP@AOD.org"
    )
    try:
        db.session.add(support_worker3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    # SEED TENANCY
    tenancy1 = Tenancy(
        start_date=date(2025, 12, 5),
        end_date=None,
        tenancy_status="Sign-Up",
        property_id=property3.id
    )
    db.session.add(tenancy1)

    tenancy2 = Tenancy(
        start_date=date(2006, 10, 9),
        end_date=date(2025, 11, 28),
        tenancy_status="Vacant",
        property_id=property2.id
    )
    db.session.add(tenancy2)

    tenancy3 = Tenancy(
        start_date=date(2019, 5, 1),
        end_date=None,
        tenancy_status="Tenanted",
        property_id=property1.id
    )
    try:
        db.session.add(support_worker3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    # SEED TENANT
    tenant1 = Tenant(
        name="James Arquette",
        date_of_birth=date(1973, 6, 25),
        phone="0417678900",
        email="banana-bicycle@hotmail.com"
    )
    db.session.add(tenant1)

    tenant2 = Tenant(
        name="June Harris",
        date_of_birth=date(1966, 3, 12),
        phone="0400345678",
        email="harrij@yahoo.com"
    )
    db.session.add(tenant2)

    tenant3 = Tenant(
        name="Paula Deakin",
        date_of_birth=date(1990, 7, 14),
        phone="0438987654",
        email="jupiter.sun@gmail.com"
    )
    try:
        db.session.add(tenant3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    # SEED TENANT_TENANCY
    tenant_tenancy1 = TenantTenancy(
        rank=1,
        tenant=tenant1,
        tenancy=tenancy1
    )
    db.session.add(tenant_tenancy1)

    tenant_tenancy2 = TenantTenancy(
        rank=2,
        tenant=tenant2,
        tenancy=tenancy2
    )
    db.session.add(tenant_tenancy2)

    tenant_tenancy3 = TenantTenancy(
        rank=3,
        tenant=tenant3,
        tenancy=tenancy3
    )
    try:
        db.session.add(tenant_tenancy3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    # SEED TENANT_SUPPORT_WORKER
    tenant_support_worker1 = TenantSupportWorker(
        rank=1,
        tenant=tenant1,
        support_worker=support_worker1
    )
    db.session.add(tenant_support_worker1)

    tenant_support_worker2 = TenantSupportWorker(
        rank=2,
        tenant=tenant2,
        support_worker=support_worker2
    )
    db.session.add(tenant_support_worker2)

    tenant_support_worker3 = TenantSupportWorker(
        rank=3,
        tenant=tenant3,
        support_worker=support_worker3
    )
    try:
        db.session.add(tenant_support_worker3)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    print("Table seeded!🌱")
