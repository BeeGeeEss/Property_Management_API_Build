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
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Application modules
from extensions import db
from models.tenancy import Tenancy
from models.tenant import Tenant
from models.tenant_tenancy import TenantTenancy
from schemas.tenancy_schema import (
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
    try:
        stmt = db.select(Tenancy)
        tenancies_list = db.session.scalars(stmt).all()
        return jsonify(tenancies_schema.dump(tenancies_list)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Single Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["GET"])
def get_tenancy(tenancy_id):
    """Return a single tenancy by ID, or 404 if not found."""
    try:
        tenancy_obj = db.get(Tenancy, tenancy_id)
        if not tenancy_obj:
            return abort(404, description="Tenancy does not exist")
        return jsonify(tenancy_schema.dump(tenancy_obj)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

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
    try:
        stmt = db.select(Tenancy).options(selectinload(Tenancy.property))
        tenancies = db.session.scalars(stmt).all()
        return jsonify(tenancies_with_property_schema.dump(tenancies)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Tenancies with Tenants
# ============================================================
@tenancies_bp.route("/tenants", methods=["GET"])
def get_tenancies_with_tenants():
    """Return all tenancies including their associated tenants."""
    try:
        stmt = db.select(Tenancy).options(selectinload(Tenancy.tenants))
        tenancies = db.session.scalars(stmt).all()
        return jsonify(tenancies_with_tenants_schema.dump(tenancies)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Create a New Tenancy
# ============================================================
@tenancies_bp.route("/", methods=["POST"])
def create_tenancy():
    """Create a new tenancy and return it."""
    try:
        tenancy_fields = tenancy_schema.load(request.json)
        new_tenancy = Tenancy(
            start_date=tenancy_fields["start_date"],
            end_date=tenancy_fields.get("end_date"),
            tenancy_status=tenancy_fields["tenancy_status"],
            property_id=tenancy_fields.get("property_id")
        )
        db.session.add(new_tenancy)
        db.session.commit()
        return jsonify(tenancy_schema.dump(new_tenancy)), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# PUT: Update Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["PUT"])
def update_tenancy(tenancy_id):
    """Update an existing tenancy with provided fields."""
    try:
        tenancy_fields = tenancy_schema.load(request.json, partial=True)
        tenancy_obj = db.get(Tenancy, tenancy_id)

        if not tenancy_obj:
            return abort(404, description="Tenancy does not exist")

        for key in ["start_date", "end_date", "tenancy_status", "property_id"]:
            if key in tenancy_fields:
                setattr(tenancy_obj, key, tenancy_fields[key])

        db.session.commit()
        return jsonify(tenancy_schema.dump(tenancy_obj)), 200
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# DELETE: Delete Tenancy by ID
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/", methods=["DELETE"])
def delete_tenancy(tenancy_id):
    """Delete a tenancy by ID and return the deleted record."""
    try:
        tenancy = db.get(Tenancy, tenancy_id)
        if not tenancy:
            return abort(404, description="Tenancy not found")
        db.session.delete(tenancy)
        db.session.commit()
        return jsonify(tenancy_schema.dump(tenancy)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Link a Tenant to a Tenancy
# ============================================================
@tenancies_bp.route("/<int:tenancy_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(tenancy_id, tenant_id):
    """
    Link a tenant to a tenancy. Prevents duplicate links.

    Returns a success message if link is created, otherwise an error.
    """
    try:
        tenancy = db.get(Tenancy, tenancy_id)
        tenant = db.get(Tenant, tenant_id)

        if not tenancy or not tenant:
            return abort(404, description="Tenancy or Tenant not found")

        existing_link = db.session.scalar(
            db.select(TenantTenancy).filter_by(
                tenant_id=tenant_id, tenancy_id=tenancy_id
            )
        )
        if existing_link:
            return abort(400, description="Tenant already linked to this tenancy")

        new_link = TenantTenancy(tenant_id=tenant_id, tenancy_id=tenancy_id)
        db.session.add(new_link)
        db.session.commit()
        return jsonify({"message": f"Tenancy {tenancy_id} linked to Tenant {tenant_id}"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
