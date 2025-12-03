from flask import Blueprint, jsonify, request, abort
from main import db
from Models.tenancy import Tenancy
from Models.tenant import Tenant
from Models.property import Property
from Models.tenant_tenancy import TenantTenancy
from Schemas.tenancy_schema import tenancy_schema, tenancies_schema

tenancies_bp = Blueprint(
    'tenancies', __name__, url_prefix="/tenancies"
)

# -------------------------
# GET all tenancies
# -------------------------
@tenancies_bp.route("/", methods=["GET"])
def get_tenancies():
    """Docstring"""
    stmt = db.select(Tenancy)
    tenancies_list = db.session.scalars(stmt)
    result = tenancies_schema.dump(tenancies_list)
    return jsonify(result)

# -------------------------
# GET a single tenancy by ID
# -------------------------
@tenancies_bp.route("/<int:id>/", methods=["GET"])
def get_tenancy(id):
    """Docstring"""
    tenancy = db.get(Tenancy, id)
    if not tenancy:
        return abort(404, description="Tenancy not found")
    return jsonify(tenancy_schema.dump(tenancy))

# -------------------------
# CREATE a new tenancy
# -------------------------
@tenancies_bp.route("/", methods=["POST"])
def create_tenancy():
    """Docstring"""
    tenancy_fields = tenancy_schema.load(request.json)

    # Validate property if property_id is provided
    property_obj = None
    if "property_id" in tenancy_fields:
        property_obj = db.get(Property, tenancy_fields["property_id"])
        if not property_obj:
            return abort(404, description="Property not found")

    new_tenancy = Tenancy(
        property_id=tenancy_fields.get("property_id"),
        start_date=tenancy_fields["start_date"],
        end_date=tenancy_fields.get("end_date"),
        tenancy_status=tenancy_fields["tenancy_status"]
    )

    db.session.add(new_tenancy)
    db.session.commit()
    return jsonify(tenancy_schema.dump(new_tenancy)), 201

# -------------------------
# DELETE a tenancy by ID
# -------------------------
@tenancies_bp.route("/<int:id>/", methods=["DELETE"])
def delete_tenancy(id):
    """Docstring"""
    tenancy = db.get(Tenancy, id)
    if not tenancy:
        return abort(404, description="Tenancy not found")

    db.session.delete(tenancy)
    db.session.commit()
    return jsonify(tenancy_schema.dump(tenancy)), 200

# -------------------------
# UPDATE a tenancy by ID
# -------------------------
@tenancies_bp.route("/<int:id>/", methods=["PUT"])
def update_tenancy(id):
    """Docstring"""
    tenancy = db.get(Tenancy, id)
    if not tenancy:
        return abort(404, description="Tenancy not found")

    tenancy_fields = tenancy_schema.load(request.json, partial=True)

    if "property_id" in tenancy_fields:
        property_obj = db.get(Property, tenancy_fields["property_id"])
        if not property_obj:
            return abort(404, description="Property not found")
        tenancy.property_id = tenancy_fields["property_id"]

    if "start_date" in tenancy_fields:
        tenancy.start_date = tenancy_fields["start_date"]
    if "end_date" in tenancy_fields:
        tenancy.end_date = tenancy_fields["end_date"]
    if "tenancy_status" in tenancy_fields:
        tenancy.tenancy_status = tenancy_fields["tenancy_status"]

    db.session.commit()
    return jsonify(tenancy_schema.dump(tenancy)), 200

# -------------------------
# LINK a tenant to a tenancy
# -------------------------
@tenancies_bp.route("/<int:tenancy_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(tenancy_id, tenant_id):
    """Docstring"""
    tenancy = db.get(Tenancy, tenancy_id)
    tenant = db.get(Tenant, tenant_id)

    if not tenancy or not tenant:
        return abort(404, description="Tenancy or Tenant not found")

    # Prevent duplicate links
    existing_link = db.session.scalar(
        db.select(TenantTenancy)
        .filter_by(tenancy_id=tenancy_id, tenant_id=tenant_id)
    )
    if existing_link:
        return abort(400, description="Tenant already linked to this tenancy")

    new_link = TenantTenancy(
        tenancy_id=tenancy_id,
        tenant_id=tenant_id
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": f"Tenant {tenant_id} linked to Tenancy {tenancy_id}"}), 201
