"""
Controllers Package

This module aggregates all individual controller blueprints for the
Property Management API. It allows the main application to register
all controllers easily without importing them individually.

"""

from Controllers.property_controller import properties_bp
from Controllers.property_manager_controller import property_managers_bp
from Controllers.support_worker_controller import support_workers_bp
from Controllers.tenancy_controller import tenancies_bp
from Controllers.tenant_controller import tenants_bp

registerable_controllers = [
    properties_bp,
    property_managers_bp,
    support_workers_bp,
    tenancies_bp,
    tenants_bp
]
