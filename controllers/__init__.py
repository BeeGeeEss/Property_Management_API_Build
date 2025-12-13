"""
Controllers Package

This module aggregates all individual controller blueprints for the
Property Management API. It allows the main application to register
all controllers easily without importing them individually.

"""

from controllers.property_controller import properties_bp
from controllers.property_manager_controller import property_managers_bp
from controllers.support_worker_controller import support_workers_bp
from controllers.tenancy_controller import tenancies_bp
from controllers.tenant_controller import tenants_bp

registerable_controllers = [
    properties_bp,
    property_managers_bp,
    support_workers_bp,
    tenancies_bp,
    tenants_bp
]
