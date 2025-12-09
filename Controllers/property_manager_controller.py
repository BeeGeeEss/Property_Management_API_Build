from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from extensions import db
from Models.property_manager import PropertyManager
from Schemas.property_manager_schema import property_manager_schema, property_managers_schema, property_managers_with_properties_schema

property_managers_bp = Blueprint(
    'property_managers', __name__, url_prefix="/property_managers"
)

# -------------------------
# GET all property managers
# -------------------------
@property_managers_bp.route("/", methods=["GET"])
def get_property_managers():
    stmt = db.select(PropertyManager)
    managers_list = db.session.scalars(stmt)
    return jsonify(property_managers_schema.dump(managers_list))

# -------------------------
# GET a single property manager by property_manager_id
# -------------------------
@property_managers_bp.route("/<int:property_manager_id>/", methods=["GET"])
def get_property_manager(property_manager_id):
    stmt = db.select(PropertyManager).filter_by(id=property_manager_id)
    property_manager_obj = db.session.scalar(stmt)
    #return an error if the competition doesn't exist
    if not property_manager_obj:
        return abort(400, description= "Property Manager does not exist")
    # Convert the competitions from the database into a JSON format and store them in result
    result = property_manager_schema.dump(property_manager_obj)
    # return the data in JSON format
    return jsonify(result)

# -------------------------
# GET Property Managers & Properties
# -------------------------
@property_managers_bp.route("/properties", methods=["GET"])
def get_property_managers_with_properties():
    stmt = db.select(PropertyManager).options(selectinload(PropertyManager.properties))
    managers = db.session.scalars(stmt).all()
    return jsonify(property_managers_with_properties_schema.dump(managers))

# -------------------------
# CREATE a new property manager
# -------------------------
@property_managers_bp.route("/", methods=["POST"])
def create_property_manager():
    manager_fields = property_manager_schema.load(request.json)

    new_manager = PropertyManager()
    new_manager.name = manager_fields["name"]
    new_manager.phone = manager_fields["phone"]
    new_manager.email = manager_fields["email"]
    # add to the database and commit
    db.session.add(new_manager)
    db.session.commit()
    # return the competition in the response
    return jsonify(property_manager_schema.dump(new_manager)), 201


# -------------------------
# DELETE a property manager by property_manager_id
# -------------------------
@property_managers_bp.route("/<int:property_manager_id>/", methods=["DELETE"])
def delete_property_manager(property_manager_id):
    stmt = db.select(PropertyManager).filter_by(id=property_manager_id)
    manager = db.session.scalar(stmt)
    if not manager:
        return abort(404, description="Property Manager not found")

    db.session.delete(manager)
    db.session.commit()
    return jsonify(property_manager_schema.dump(manager)), 200

# -------------------------
# UPDATE a property manager by property_manager_id
# -------------------------
@property_managers_bp.route("/<int:property_manager_id>/", methods=["PUT"])
def update_property_manager(property_manager_id):
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
