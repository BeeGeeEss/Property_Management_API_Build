from flask import Blueprint, jsonify, request, abort
from main import db
from Models.property import Property
from Models.property_manager import PropertyManager
from Schemas.property_schema import property_schema, properties_schema

properties_bp = Blueprint(
    'properties', __name__, url_prefix="/properties"
)

# -------------------------
# GET all properties
# -------------------------
@properties_bp.route("/", methods=["GET"])
def get_properties():
    """Docstring"""
    stmt = db.select(Property)
    properties_list = db.session.scalars(stmt)
    result = properties_schema.dump(properties_list)
    return jsonify(result)

# -------------------------
# GET a single property by ID
# -------------------------
@properties_bp.route("/<int:id>/", methods=["GET"])
def get_property(id):
    """Docstring"""
    stmt = db.select(Property).filter_by(id=id)
    prop = db.session.scalar(stmt)
    if not prop:
        return abort(404, description="Property not found")
    return jsonify(property_schema.dump(prop))

# -------------------------
# CREATE a new property
# -------------------------
@properties_bp.route("/", methods=["POST"])
def create_property():
    """Docstring"""
    prop_fields = property_schema.load(request.json)

    # If property_manager_id is provided, ensure it exists
    manager = None
    if "property_manager_id" in prop_fields:
        manager = db.get(PropertyManager, prop_fields["property_manager_id"])
        if not manager:
            return abort(404, description="Property Manager not found")

    new_property = Property(
        address=prop_fields["address"],
        property_manager=manager  # set via relationship
    )

    db.session.add(new_property)
    db.session.commit()
    return jsonify(property_schema.dump(new_property)), 201

# -------------------------
# DELETE a property by ID
# -------------------------
@properties_bp.route("/<int:id>/", methods=["DELETE"])
def delete_property(id):
    """Docstring"""
    prop = db.get(Property, id)
    if not prop:
        return abort(404, description="Property not found")

    db.session.delete(prop)
    db.session.commit()
    return jsonify(property_schema.dump(prop)), 200

# -------------------------
# UPDATE a property by ID
# -------------------------
@properties_bp.route("/<int:id>/", methods=["PUT"])
def update_property(id):
    """Docstring"""
    prop = db.get(Property, id)
    if not prop:
        return abort(404, description="Property not found")

    prop_fields = property_schema.load(request.json, partial=True)

    if "address" in prop_fields:
        prop.address = prop_fields["address"]

    if "property_manager_id" in prop_fields:
        manager = db.get(PropertyManager, prop_fields["property_manager_id"])
        if not manager:
            return abort(404, description="Property Manager not found")
        prop.property_manager = manager

    db.session.commit()
    return jsonify(property_schema.dump(prop)), 200
