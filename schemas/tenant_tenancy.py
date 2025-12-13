"""
Tenant-Tenancy Schema

This module defines Marshmallow schemas for serializing and deserializing
TenantTenancy objects, representing the many-to-many relationship between
Tenants and Tenancies.

Schemas:
    - TenantTenancySchema: Basic schema with optional nested Tenant and Tenancy info.

Schema Instances:
    - tenant_tenancy_schema: Single instance.
    - tenant_tenancies_schema: Multiple instances.

"""

# Imports
from marshmallow import fields
from extensions import ma
from models.tenant_tenancy import TenantTenancy

class TenantTenancySchema(ma.SQLAlchemySchema):
    """
    Schema for TenantTenancy relationship.

    Fields:
        id (int): Primary key of the relationship.
        tenant_id (int, load_only): Foreign key for the tenant.
        tenancy_id (int, load_only): Foreign key for the tenancy.
        tenant (TenantSchema): Nested tenant info (id and name only).
        tenancy (TenancySchema): Nested tenancy info (id and tenancy_status only).
    """
    class Meta:
        model = TenantTenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    tenant_id = ma.auto_field(load_only=True)
    tenancy_id = ma.auto_field(load_only=True)

    tenant = fields.Nested("TenantSchema", only=["id", "name"])
    tenancy = fields.Nested("TenancySchema", only=["id", "tenancy_status"])

# Schema Instances
tenant_tenancy_schema = TenantTenancySchema()
tenant_tenancies_schema = TenantTenancySchema(many=True)
