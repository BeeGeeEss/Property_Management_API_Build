"""
Property Manager Controller

Handles all routes related to Property Manager resources, including:
- Retrieving all property managers
- Retrieving a single property manager
- Retrieving property managers with nested properties
- Creating, updating, and deleting property managers

"""

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload

# Application modules
from extensions import db
from Models.property_manager import PropertyManager
from Schemas.property_manager_schema import (
    property_manager_schema,
    property_managers_schema,
    property_managers_with_properties_schema
)

# Blueprint setup
property_managers_bp = Blueprint(
    'property_managers', __name__, url_prefix="/property_managers"
)

# ============================================================
# GET: All Property Managers
# ============================================================
@property_managers_bp.route("/", methods=["GET"])
def get_property_managers():
    """Return a list of all property managers."""
    stmt = db.select(PropertyManager)
    managers_list = db.session.scalars(stmt)
    return jsonify(property_managers_schema.dump(managers_list))

# ============================================================
# GET: Single Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["GET"])
def get_property_manager(property_manager_id):
    """Return a single property manager by ID, or 404 if not found."""
    stmt = db.select(PropertyManager).filter_by(id=property_manager_id)
    property_manager_obj = db.session.scalar(stmt)

    if not property_manager_obj:
        return abort(400, description= "Property Manager does not exist")

    result = property_manager_schema.dump(property_manager_obj)

    return jsonify(result)

# ============================================================
# GET: Property Managers with Nested Properties
# ============================================================
@property_managers_bp.route("/properties", methods=["GET"])
def get_property_managers_with_properties():
    """Return all property managers including their associated properties."""
    stmt = db.select(PropertyManager).options(selectinload(PropertyManager.properties))
    managers = db.session.scalars(stmt)
    return jsonify(property_managers_with_properties_schema.dump(managers))

# ============================================================
# POST: Create a New Property Manager
# ============================================================
@property_managers_bp.route("/", methods=["POST"])
def create_property_manager():
    """Create a new property manager and return it."""
    manager_fields = property_manager_schema.load(request.json)

    new_manager = PropertyManager(
        name=manager_fields["name"],
        phone=manager_fields["phone"],
        email=manager_fields["email"]
    )

    db.session.add(new_manager)
    db.session.commit()

    return jsonify(property_manager_schema.dump(new_manager)), 201

# ============================================================
# DELETE: Delete Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["DELETE"])
def delete_property_manager(property_manager_id):
    """Delete a property manager by ID and return the deleted record."""
    stmt = db.select(PropertyManager).filter_by(id=property_manager_id)
    manager = db.session.scalar(stmt)

    if not manager:
        return abort(404, description="Property Manager not found")

    db.session.delete(manager)
    db.session.commit()
    return jsonify(property_manager_schema.dump(manager)), 200

# ============================================================
# PUT: Update Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["PUT"])
def update_property_manager(property_manager_id):
    """Update an existing property manager with provided fields."""
    stmt = db.select(PropertyManager).filter_by(id=property_manager_id)
    manager = db.session.scalar(stmt)

    if not manager:
        return abort(404, description="Property Manager not found")

    manager_fields = property_manager_schema.load(request.json, partial=True)

    if "name" in manager_fields:
        manager.name = manager_fields["name"]
    if "phone" in manager_fields:
        manager.phone = manager_fields["phone"]
    if "email" in manager_fields:
        manager.email = manager_fields["email"]

    db.session.commit()

    return jsonify(property_manager_schema.dump(manager)), 200
