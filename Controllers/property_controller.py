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

# Application modules
from extensions import db
from Models.property import Property
from Schemas.property_schema import (
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
    stmt = db.select(Property)
    properties_list = db.session.scalars(stmt)
    return jsonify(properties_schema.dump(properties_list))

# ============================================================
# GET: Single Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["GET"])
def get_property(property_id):
    """Return a single property by its ID, or 404 if not found."""
    stmt = db.select(Property).filter_by(id=property_id)
    property_obj = db.session.scalar(stmt)

    if not property_obj:
        return abort(400, description= "Property does not exist")

    result = property_schema.dump(property_obj)

    return jsonify(result)

# ============================================================
# GET: Properties with Nested Property Managers
# ============================================================
@properties_bp.route("/property_managers", methods=["GET"])
def get_properties_with_managers():
    """Return all properties including their associated property managers."""
    stmt = db.select(Property).options(selectinload(Property.property_manager))
    properties = db.session.scalars(stmt)
    return jsonify(properties_with_manager_schema.dump(properties))

# ============================================================
# POST: Create a New Property
# ============================================================
@properties_bp.route("/", methods=["POST"])
def create_property():
    """Create a new property and return it."""
    property_fields = property_schema.load(request.json)

    new_property = Property(
        address=property_fields["address"],
        property_manager_id=property_fields["property_manager_id"]
    )

    db.session.add(new_property)
    db.session.commit()

    return jsonify(property_schema.dump(new_property)), 201

# ============================================================
# DELETE: Delete Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["DELETE"])
def delete_property(property_id):
    """Delete a property by its ID and return the deleted record."""
    property_obj = db.get(Property, property_id)

    if not property_obj:
        return abort(404, description="Property not found ❌")

    db.session.delete(property_obj)
    db.session.commit()

    return jsonify(property_schema.dump(property_obj)), 200

# ============================================================
# PUT: Update Property by ID
# ============================================================
@properties_bp.route("/<int:property_id>/", methods=["PUT"])
def update_property(property_id):
    """Update an existing property with provided fields."""
    property_fields = property_schema.load(request.json, partial=True)

    stmt = db.select(Property).filter_by(id=property_id)
    property_obj = db.session.scalar(stmt)

    if not property_obj:
        return abort(400, description="Property does not exist")

    # Apply updates only if provided
    if "address" in property_fields:
        property_obj.address = property_fields["address"]

    if "property_manager_id" in property_fields:
        property_obj.property_manager_id = property_fields["property_manager_id"]

    db.session.commit()

    return jsonify(property_schema.dump(property_obj)), 200
