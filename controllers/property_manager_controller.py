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
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Application modules
from extensions import db
from models.property_manager import PropertyManager
from schemas.property_manager_schema import (
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
    try:
        stmt = db.select(PropertyManager)
        managers_list = db.session.scalars(stmt).all()
        return jsonify(property_managers_schema.dump(managers_list)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Single Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["GET"])
def get_property_manager(property_manager_id):
    """Return a single property manager by ID, or 404 if not found."""
    try:
        manager = db.get(PropertyManager, property_manager_id)
        if not manager:
            return abort(404, description="Property Manager does not exist")
        return jsonify(property_manager_schema.dump(manager)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Property Managers with Nested Properties
# ============================================================
@property_managers_bp.route("/properties", methods=["GET"])
def get_property_managers_with_properties():
    """Return all property managers including their associated properties."""
    try:
        stmt = db.select(PropertyManager).options(selectinload(PropertyManager.properties))
        managers = db.session.scalars(stmt).all()
        return jsonify(property_managers_with_properties_schema.dump(managers)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Create a New Property Manager
# ============================================================
@property_managers_bp.route("/", methods=["POST"])
def create_property_manager():
    """Create a new property manager and return it."""
    try:
        manager_fields = property_manager_schema.load(request.json)
        new_manager = PropertyManager(
            name=manager_fields["name"],
            phone=manager_fields.get("phone"),
            email=manager_fields.get("email")
        )
        db.session.add(new_manager)
        db.session.commit()
        return jsonify(property_manager_schema.dump(new_manager)), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# PUT: Update Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["PUT"])
def update_property_manager(property_manager_id):
    """Update an existing property manager with provided fields."""
    try:
        manager_fields = property_manager_schema.load(request.json, partial=True)
        manager_obj = db.get(PropertyManager, property_manager_id)

        if not manager_obj:
            return abort(404, description="Property Manager does not exist")

        for key in ["name", "phone", "email"]:
            if key in manager_fields:
                setattr(manager_obj, key, manager_fields[key])

        db.session.commit()
        return jsonify(property_manager_schema.dump(manager_obj)), 200
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# DELETE: Delete Property Manager by ID
# ============================================================
@property_managers_bp.route("/<int:property_manager_id>/", methods=["DELETE"])
def delete_property_manager(property_manager_id):
    """Delete a property manager by ID and return the deleted record."""
    try:
        manager = db.get(PropertyManager, property_manager_id)
        if not manager:
            return abort(404, description="Property Manager not found")
        db.session.delete(manager)
        db.session.commit()
        return jsonify(property_manager_schema.dump(manager)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
