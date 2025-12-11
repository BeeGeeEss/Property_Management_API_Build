"""
Tenancy Controller

Handles all routes related to Tenancy resources, including:
- Retrieving all tenancies
- Retrieving a single tenancy
- Searching tenancies by query parameters
- Retrieving tenancies with nested properties or tenants
- Creating, updating, and deleting tenancies
- Linking tenants to tenancies

"""

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload

# Application modules
from extensions import db
from Models.tenancy import Tenancy
from Models.tenant import Tenant
from Models.property import Property
from Models.tenant_tenancy import TenantTenancy
from Schemas.tenancy_schema import (
    tenancy_schema,
    tenancies_schema,
    tenancies_with_property_schema,
    tenancies_with_tenants_schema
)

# Blueprint setup
tenancies_bp = Blueprint(
    'tenancies', __name__, url_prefix="/tenancies"
)

# ============================================================
# GET: All Tenancies
# ============================================================
@tenancies_bp.route("/", methods=["GET"])
def get_tenancies():
    """Return a list of all tenancies."""
    stmt = db.select(Tenancy)
    tenancies_list = db.session.scalars(stmt)
    return jsonify(tenancies_schema.dump(tenancies_list))

# ============================================================
# GET: Single Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["GET"])
def get_tenancy(tenancy_id):
    """Return a single tenancy by ID, or 404 if not found."""
    stmt = db.select(Tenancy).filter_by(id=tenancy_id)
    tenancy_obj = db.session.scalar(stmt)

    if not tenancy_obj:
        return abort(400, description= "Tenancy does not exist")

    result = tenancy_schema.dump(tenancy_obj)

    return jsonify(result)

# ============================================================
# GET: Search Tenancies
# ============================================================

@tenancies_bp.route("/search", methods=["GET"])
def search_tenancies():
    """Return tenancies matching optional query parameters: status, start_date, end_date."""
    stmt = db.select(Tenancy)

    status = request.args.get("status")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if status:
        stmt = stmt.filter(Tenancy.tenancy_status == status)

    if start_date:
        stmt = stmt.filter(Tenancy.start_date >= start_date)

    if end_date:
        stmt = stmt.filter(Tenancy.end_date <= end_date)

    tenancies = db.session.scalars(stmt).all()


    result = tenancies_schema.dump(tenancies)
    return jsonify(result), 200

# ============================================================
# GET: Tenancies with Properties
# ============================================================
@tenancies_bp.route("/properties", methods=["GET"])
def get_tenancies_with_properties():
    """Return all tenancies including their associated properties."""
    stmt = db.select(Tenancy).options(selectinload(Tenancy.property))
    tenancies = db.session.scalars(stmt)
    return jsonify(tenancies_with_property_schema.dump(tenancies))

# ============================================================
# GET: Tenancies with Tenants
# ============================================================
@tenancies_bp.route("/tenants", methods=["GET"])
def get_tenancies_with_tenants():
    """Return all tenancies including their associated tenants."""
    stmt = db.select(Tenancy).options(selectinload(Tenancy.tenants))
    tenancies = db.session.scalars(stmt).all()
    return jsonify(tenancies_with_tenants_schema.dump(tenancies))

# ============================================================
# POST: Create a New Tenancy
# ============================================================
@tenancies_bp.route("/", methods=["POST"])
def create_tenancy():
    """Create a new tenancy and return it."""
    tenancy_fields = tenancy_schema.load(request.json)

    # Validate property if provided
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

# ============================================================
# DELETE: Delete Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["DELETE"])
def delete_tenancy(tenancy_id):
    """Delete a tenancy by ID and return the deleted record."""
    tenancy = db.get(Tenancy, tenancy_id)

    if not tenancy:
        return abort(404, description="Tenancy not found")

    db.session.delete(tenancy)
    db.session.commit()
    return jsonify(tenancy_schema.dump(tenancy)), 200

# ============================================================
# PUT: Update Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["PUT"])
def update_tenancy(tenancy_id):
    """Update an existing tenancy with provided fields."""
    tenancy_fields = tenancy_schema.load(request.json, partial=True)

    stmt = db.select(Tenancy).filter_by(id=tenancy_id)
    tenancy_obj = db.session.scalar(stmt)

    if not tenancy_obj:
        return abort(404, description="Tenancy does not exist")

    if "start_date" in tenancy_fields:
        tenancy_obj.start_date = tenancy_fields["start_date"]

    if "end_date" in tenancy_fields:
        tenancy_obj.end_date = tenancy_fields["end_date"]

    if "property_id" in tenancy_fields:
        tenancy_obj.property_id = tenancy_fields["property_id"]

    db.session.commit()

    return jsonify(tenancy_schema.dump(tenancy_obj)), 200

# ============================================================
# POST: Link a Tenant to a Tenancy
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(tenancy_id, tenant_id):
    """
    Link a tenant to a tenancy. Prevents duplicate links.

    Returns a success message if link is created, otherwise an error.
    """
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
