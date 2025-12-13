"""
Support Worker Controller

Handles all routes related to Support Worker resources, including:
- Retrieving all support workers
- Retrieving a single support worker
- Retrieving support workers with nested tenants
- Creating, updating, and deleting support workers

"""

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

# Application modules
from extensions import db
from models.support_worker import SupportWorker
from models.tenant import Tenant
from models.tenant_support_worker import TenantSupportWorker
from schemas.support_worker_schema import (
    support_worker_schema,
    support_workers_schema,
    support_workers_with_tenants_schema
)

# Blueprint setup
support_workers_bp = Blueprint(
    'support_workers', __name__, url_prefix="/support_workers"
)

# ============================================================
# GET: All Support Workers
# ============================================================
@support_workers_bp.route("/", methods=["GET"])
def get_support_workers():
    """Return a list of all support workers."""
    try:
        stmt = db.select(SupportWorker)
        workers_list = db.session.scalars(stmt).all()
        return jsonify(support_workers_schema.dump(workers_list)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Single Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["GET"])
def get_support_worker(support_worker_id):
    """Return a single support worker by ID, or 404 if not found."""
    try:
        worker = db.get(SupportWorker, support_worker_id)
        if not worker:
            return abort(404, description="Support Worker does not exist")
        return jsonify(support_worker_schema.dump(worker)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GET: Support Workers with Nested Tenants
# ============================================================
@support_workers_bp.route("/tenants", methods=["GET"])
def get_support_workers_tenants():
    """Return all support workers including their assigned tenants."""
    try:
        stmt = db.select(SupportWorker).options(selectinload(SupportWorker.tenants))
        workers = db.session.scalars(stmt).all()
        return jsonify(support_workers_with_tenants_schema.dump(workers)), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Create a New Support Worker
# ============================================================
@support_workers_bp.route("/", methods=["POST"])
def create_support_worker():
    """Create a new support worker and return it."""
    try:
        worker_fields = support_worker_schema.load(request.json)
        new_worker = SupportWorker(
            name=worker_fields["name"],
            phone=worker_fields.get("phone"),
            email=worker_fields.get("email")
        )
        db.session.add(new_worker)
        db.session.commit()
        return jsonify(support_worker_schema.dump(new_worker)), 201
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# PUT: Update Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["PUT"])
def update_support_worker(support_worker_id):
    """Update an existing support worker with provided fields."""
    try:
        worker_fields = support_worker_schema.load(request.json, partial=True)
        worker_obj = db.get(SupportWorker, support_worker_id)

        if not worker_obj:
            return abort(404, description="Support Worker does not exist")

        for key in ["name", "phone", "email"]:
            if key in worker_fields:
                setattr(worker_obj, key, worker_fields[key])

        db.session.commit()
        return jsonify(support_worker_schema.dump(worker_obj)), 200
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# DELETE: Delete Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["DELETE"])
def delete_support_worker(support_worker_id):
    """Delete a support worker by ID and return the deleted record."""
    try:
        worker = db.get(SupportWorker, support_worker_id)
        if not worker:
            return abort(404, description="Support Worker not found")
        db.session.delete(worker)
        db.session.commit()
        return jsonify(support_worker_schema.dump(worker)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================
# POST: Link Support Worker to Tenant
# ============================================================
@support_workers_bp.route("/<int:worker_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(worker_id, tenant_id):
    """Link a support worker to a tenant, preventing duplicates."""
    try:
        worker = db.get(SupportWorker, worker_id)
        tenant = db.get(Tenant, tenant_id)

        if not worker or not tenant:
            return abort(404, description="Support Worker or Tenant not found")

        existing_link = db.session.scalar(
            db.select(TenantSupportWorker).filter_by(
                tenant_id=tenant_id, support_worker_id=worker_id
            )
        )
        if existing_link:
            return abort(400, description="Tenant already linked to this support worker")

        new_link = TenantSupportWorker(
            tenant_id=tenant_id,
            support_worker_id=worker_id
        )
        db.session.add(new_link)
        db.session.commit()
        return jsonify({"message": f"Support Worker {worker_id} linked to Tenant {tenant_id}"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
