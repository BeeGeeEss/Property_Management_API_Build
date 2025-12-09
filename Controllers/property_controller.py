from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from extensions import db
from Models.property import Property
from Schemas.property_schema import property_schema, properties_schema, properties_with_manager_schema


# Blueprint definition
properties_bp = Blueprint('properties', __name__, url_prefix="/properties")

# -------------------------
# GET all properties
# -------------------------
@properties_bp.route("/", methods=["GET"])
def get_properties():
    stmt = db.select(Property)
    properties_list = db.session.scalars(stmt)
    return jsonify(properties_schema.dump(properties_list))

# -------------------------
# GET a single property by property_id
# -------------------------
@properties_bp.route("/<int:property_id>/", methods=["GET"])
def get_property(property_id):
    stmt = db.select(Property).filter_by(id=property_id)
    property_obj = db.session.scalar(stmt)
    #return an error if the competition doesn't exist
    if not property_obj:
        return abort(400, description= "Property does not exist")
    # Convert the competitions from the database into a JSON format and store them in result
    result = property_schema.dump(property_obj)
    # return the data in JSON format
    return jsonify(result)

# -------------------------
# GET properties & Property Managers Nested
# -------------------------
@properties_bp.route("/property_managers", methods=["GET"])
def get_properties_with_managers():
    stmt = db.select(Property).options(selectinload(Property.property_manager))
    properties = db.session.scalars(stmt)
    return jsonify(properties_with_manager_schema.dump(properties))

# -------------------------
# CREATE a new property
# -------------------------
@properties_bp.route("/", methods=["POST"])
def create_property():
    property_fields = property_schema.load(request.json)
    # Create a new property
    new_property = Property()
    new_property.address = property_fields["address"]
    # add category's id
    new_property.property_manager_id = property_fields["property_manager_id"]
    # add to the database and commit
    db.session.add(new_property)
    db.session.commit()
    # return the competition in the response
    return jsonify(property_schema.dump(new_property)), 201

# -------------------------
# DELETE a property by property_id
# -------------------------
@properties_bp.route("/<int:property_id>/", methods=["DELETE"])
def delete_property(property_id):
    property_obj = db.get(Property, property_id)
    if not property_obj:
        return abort(404, description="Property not found ❌")
    db.session.delete(property_obj)
    db.session.commit()
    return jsonify(property_schema.dump(property_obj)), 200

# -------------------------
# UPDATE a property by property_id
# -------------------------
@properties_bp.route("/<int:property_id>/", methods=["PUT"])
def update_property(property_id):

    # Load and validate incoming JSON
    property_fields = property_schema.load(request.json, partial=True)

    # Retrieve the property
    stmt = db.select(Property).filter_by(id=property_id)
    property_obj = db.session.scalar(stmt)

    # Handle missing record
    if not property_obj:
        return abort(400, description="Property does not exist")
    
    # Update fields if they were provided
    if "address" in property_fields:
        property_obj.address = property_fields["address"]

    if "property_manager_id" in property_fields:
        property_obj.property_manager_id = property_fields["property_manager_id"]

    # Commit updates
    db.session.commit()

    # Return updated property
    return jsonify(property_schema.dump(property_obj)), 200
