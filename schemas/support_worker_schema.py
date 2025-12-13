"""
SupportWorker Schemas

This module defines Marshmallow schemas for serializing and deserializing
SupportWorker objects. It includes:
    - SupportWorkerSchema: Basic schema for SupportWorker.
    - SupportWorkerWithTenantSchema: Nested schema including related Tenants.

Attributes:
    support_worker_schema (SupportWorkerSchema): Single SupportWorker schema instance.
    support_workers_schema (SupportWorkerSchema): Multiple SupportWorker schema instance.
    support_worker_with_tenants_schema (SupportWorkerWithTenantSchema): Single nested schema instance.
    support_workers_with_tenants_schema (SupportWorkerWithTenantSchema): Multiple nested schema instance.
"""

# Imports
from marshmallow import fields
from extensions import ma
from models.support_worker import SupportWorker

class SupportWorkerSchema(ma.SQLAlchemySchema):
    """
    Basic schema for SupportWorker.

    Fields:
        id (int): Primary key.
        name (str): Name of the support worker.
        phone (str): Phone number.
        email (str): Email address.
    """
    class Meta:
        model = SupportWorker
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class SupportWorkerWithTenantSchema(ma.SQLAlchemySchema):
    """
    Nested schema for SupportWorker including related Tenants.

    Fields:
        id (int): Primary key.
        name (str): Name of the support worker.
        phone (str): Phone number.
        email (str): Email address.
        tenants (list[TenantSchema]): List of tenants with limited fields (id, name).
    """
    class Meta:
        model = SupportWorker
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    tenants = fields.List(fields.Nested("TenantSchema", only=["id","name"]))

# Schema Instances
support_worker_schema = SupportWorkerSchema()
support_workers_schema = SupportWorkerSchema(many=True)
support_worker_with_tenants_schema = SupportWorkerWithTenantSchema()
support_workers_with_tenants_schema = SupportWorkerWithTenantSchema(many=True)
