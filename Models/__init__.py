"""
Models Package

This module aggregates all SQLAlchemy ORM models for the Property Management API.
Importing this package ensures all models are registered with SQLAlchemy and
available for database operations.

Models Included:
    - Property
    - PropertyManager
    - Tenancy
    - SupportWorker
    - Tenant
    - TenantTenancy (junction table for Tenant ↔ Tenancy many-to-many)
    - TenantSupportWorker (junction table for Tenant ↔ SupportWorker many-to-many)

Usage:
    from Models import Property, Tenant, Tenancy, ...
"""

# Core domain models
from .property import Property
from .property_manager import PropertyManager
from .tenancy import Tenancy
from .support_worker import SupportWorker
from .tenant import Tenant

# Association / junction tables for many-to-many relationships
from .tenant_tenancy import TenantTenancy
from .tenant_support_worker import TenantSupportWorker
