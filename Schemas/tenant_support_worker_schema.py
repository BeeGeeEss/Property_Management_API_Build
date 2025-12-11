"""
Tenant-SupportWorker Schema

This module defines Marshmallow schemas for serializing and deserializing
TenantSupportWorker objects, representing the many-to-many relationship
between Tenants and Support Workers.

Schemas:
    - TenantSupportWorkerSchema: Basic schema with optional nested Tenant and SupportWorker info.

Schema Instances:
    - tenant_support_worker_schema: Single instance.
    - tenants_support_worker_schema: Multiple instances.

"""

# Imports
from marshmallow import fields
from extensions import ma
from Models.tenant_support_worker import TenantSupportWorker

class TenantSupportWorkerSchema(ma.SQLAlchemySchema):
    """
    Schema for TenantSupportWorker relationship.

    Fields:
        id (int): Primary key of the relationship.
        tenant_id (int, load_only): Foreign key for the tenant.
        support_worker_id (int, load_only): Foreign key for the support worker.
        tenant (TenantSchema): Nested tenant info (id and name only).
        support_worker (SupportWorkerSchema): Nested support worker info (id and name only).
    """
    class Meta:
        model = TenantSupportWorker
        load_instance = False
        ordered = True

    id = ma.auto_field()
    tenant_id = ma.auto_field(load_only=True)
    support_worker_id = ma.auto_field(load_only=True)

    tenant = fields.Nested("TenantSchema", only=["id", "name"])
    support_worker = fields.Nested("SupportWorkerSchema", only=["id", "name"])

# Schema Instances
tenant_support_worker_schema = TenantSupportWorkerSchema()
tenants_support_worker_schema = TenantSupportWorkerSchema(many=True)
