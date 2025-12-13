"""
Property Controller

Handles all routes related to Property resources, including:
- Retrieving all properties
- Retrieving a single property
- Getting properties with nested property managers
- Creating, updating, and deleting properties

"""

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Application modules
from extensions import db
from models.property import Property
from schemas.property_schema import (
    property_schema,
    properties_schema,
    properties_with_manager_schema
)


# # Blueprint setup
properties_bp = Blueprint('properties', __name__, url_prefix="/properties")

# ============================================================
# GET: All Properties
# ============================================================
@properties_bp.route("/", methods=["GET"])
def get_properties():
    """Return a list of all properties."""
    try:
        stmt = db.select(Property)
        properties_list = db.session.scalars(stmt).all()
        return jsonify(properties_schema.dump(properties_list)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Single Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["GET"])
def get_property(property_id):
    """Return a single property by its ID, or 404 if not found."""
    try:
        prop = db.get(Property, property_id)
        if not prop:
            return abort(404, description="Property does not exist")
        return jsonify(property_schema.dump(prop)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Properties with Nested Property Managers
# ============================================================
@properties_bp.route("/property_managers", methods=["GET"])
def get_properties_with_managers():
    """Return all properties including their associated property managers."""
    try:
        stmt = db.select(Property).options(selectinload(Property.managers))
        properties_list = db.session.scalars(stmt).all()
        return jsonify(properties_with_manager_schema.dump(properties_list)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Create a New Property
# ============================================================
@properties_bp.route("/", methods=["POST"])
def create_property():
    """Create a new property and return it."""
    try:
        property_fields = property_schema.load(request.json)
        new_property = Property(
            name=property_fields["name"],
            address=property_fields.get("address"),
            type=property_fields.get("type")
        )
        db.session.add(new_property)
        db.session.commit()
        return jsonify(property_schema.dump(new_property)), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# PUT: Update Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["PUT"])
def update_property(property_id):
    """Update an existing property with provided fields."""
    try:
        property_fields = property_schema.load(request.json, partial=True)
        prop = db.get(Property, property_id)

        if not prop:
            return abort(404, description="Property does not exist")

        for key in ["name", "address", "type"]:
            if key in property_fields:
                setattr(prop, key, property_fields[key])

        db.session.commit()
        return jsonify(property_schema.dump(prop)), 200
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# DELETE: Delete Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["DELETE"])
def delete_property(property_id):
    """Delete a property by its ID and return the deleted record."""
    try:
        prop = db.get(Property, property_id)
        if not prop:
            return abort(404, description="Property not found")
        db.session.delete(prop)
        db.session.commit()
        return jsonify(property_schema.dump(prop)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
