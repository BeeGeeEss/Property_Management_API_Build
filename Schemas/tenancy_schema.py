"""
Tenancy Schemas

This module defines Marshmallow schemas for serializing and deserializing
Tenancy objects. It includes:
    - TenancySchema: Basic schema for Tenancy.
    - TenancyWithPropertySchema: Nested schema including the related Property.
    - TenancyWithTenantsSchema: Nested schema including related Tenants.

Attributes:
    tenancy_schema (TenancySchema): Single Tenancy schema instance.
    tenancies_schema (TenancySchema): Multiple Tenancy schema instance.
    tenancy_with_property_schema (TenancyWithPropertySchema): Single nested schema with Property.
    tenancies_with_property_schema (TenancyWithPropertySchema): Multiple nested schema with Property.
    tenancy_with_tenants_schema (TenancyWithTenantsSchema): Single nested schema with Tenants.
    tenancies_with_tenants_schema (TenancyWithTenantsSchema): Multiple nested schema with Tenants.
"""

# Imports
from marshmallow import fields
from extensions import ma
from Models.tenancy import Tenancy

class TenancySchema(ma.SQLAlchemySchema):
    """
    Basic schema for Tenancy.

    Fields:
        id (int): Primary key.
        start_date (date): Start date of the tenancy.
        end_date (date): End date of the tenancy (optional).
        tenancy_status (str): Status of the tenancy.
        property_id (int, load_only): Foreign key to Property (load only).
    """
    class Meta:
        model = Tenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()
    property_id = ma.auto_field(load_only=True)

class TenancyWithPropertySchema(TenancySchema):
    """
    Nested schema for Tenancy including related Property.

    Fields:
        id (int): Primary key.
        property (PropertySchema): Nested Property schema (limited fields: id, address).
    """
    class Meta:
        model = Tenancy
        load_instance = True
        ordered = True

    id = ma.auto_field()
    property = fields.Nested("PropertySchema", only=["id", "address"])


class TenancyWithTenantsSchema(ma.SQLAlchemySchema):
    """
    Nested schema for Tenancy including related Tenants.

    Fields:
        id (int): Primary key.
        start_date (date): Start date of the tenancy.
        end_date (date): End date of the tenancy.
        tenancy_status (str): Status of the tenancy.
        tenants (list[TenantSchema]): List of tenants (limited fields: id, name).
    """
    class Meta:
        model = Tenancy
        load_instance = False
        ordered = True

    id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()
    tenants = fields.List(fields.Nested("TenantSchema", only=["id", "name"]))

# Schema Instances
tenancy_schema = TenancySchema()
tenancies_schema = TenancySchema(many=True)
tenancy_with_property_schema = TenancyWithPropertySchema()
tenancies_with_property_schema = TenancyWithPropertySchema(many=True)
tenancy_with_tenants_schema = TenancyWithTenantsSchema()
tenancies_with_tenants_schema =TenancyWithTenantsSchema(many=True)
