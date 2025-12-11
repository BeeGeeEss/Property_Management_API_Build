"""
Tenant Schemas

This module defines Marshmallow schemas for serializing and deserializing
Tenant objects. It includes:
    - TenantSchema: Basic schema for Tenant.
    - TenantWithTenanciesSchema: Nested schema including related Tenancies.
    - TenantWithSupportWorkerSchema: Nested schema including related Support Workers.

Attributes:
    tenant_schema (TenantSchema): Single Tenant schema instance.
    tenants_schema (TenantSchema): Multiple Tenant schema instance.
    tenant_with_tenancies_schema (TenantWithTenanciesSchema): Single nested schema with Tenancies.
    tenants_with_tenancies_schema (TenantWithTenanciesSchema): Multiple nested schema with Tenancies.
    tenant_with_support_worker_schema (TenantWithSupportWorkerSchema): Single nested schema with Support Workers.
    tenants_with_support_worker_schema (TenantWithSupportWorkerSchema): Multiple nested schema with Support Workers.

"""

# Imports
from marshmallow import fields
from extensions import ma
from Models.tenant import Tenant

class TenantSchema(ma.SQLAlchemySchema):
    """
    Basic schema for Tenant.

    Fields:
        id (int): Primary key.
        name (str): Name of the tenant.
        date_of_birth (date): Tenant's date of birth.
        phone (str, optional): Contact phone number.
        email (str, optional): Email address.
    """
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    date_of_birth = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

class TenantWithTenanciesSchema(ma.SQLAlchemySchema):
    """
    Nested schema for Tenant including related Tenancies.

    Fields:
        id (int): Primary key.
        name (str): Name of the tenant.
        phone (str, optional): Contact phone number.
        email (str, optional): Email address.
        tenancies (list[TenancySchema]): List of related tenancies (limited fields: id, start_date, end_date, tenancy_status).
    """
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    tenancies = fields.List(fields.Nested("TenancySchema", only=["id","start_date","end_date","tenancy_status"]))


class TenantWithSupportWorkerSchema(ma.SQLAlchemySchema):
    """
    Nested schema for Tenant including related Support Workers.

    Fields:
        id (int): Primary key.
        name (str): Name of the tenant.
        phone (str, optional): Contact phone number.
        email (str, optional): Email address.
        support_workers (list[SupportWorkerSchema]): List of related support workers (limited fields: id, name).
    """
    class Meta:
        model = Tenant
        load_instance = False
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()
    support_workers = fields.List(fields.Nested("SupportWorkerSchema", only=["id","name"]))

# Schema Instances
tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)
tenant_with_tenancies_schema = TenantWithTenanciesSchema()
tenants_with_tenancies_schema = TenantWithTenanciesSchema(many=True)
tenant_with_support_worker_schema = TenantWithSupportWorkerSchema()
tenants_with_support_worker_schema = TenantWithSupportWorkerSchema(many=True)
