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

# Application modules
from extensions import db
from Models.support_worker import SupportWorker
from Schemas.support_worker_schema import (
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
    stmt = db.select(SupportWorker)
    workers_list = db.session.scalars(stmt)
    return jsonify(support_workers_schema.dump(workers_list))

# ============================================================
# GET: Single Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["GET"])
def get_support_worker(support_worker_id):
    """Return a single support worker by ID, or 404 if not found."""
    stmt = db.select(SupportWorker).filter_by(id=support_worker_id)
    support_worker_obj = db.session.scalar(stmt)

    if not support_worker_obj:
        return abort(400, description= "Support Worker does not exist")

    result = support_worker_schema.dump(support_worker_obj)

    return jsonify(result)

# ============================================================
# GET: Support Workers with Nested Tenants
# ============================================================
@support_workers_bp.route("/tenants", methods=["GET"])
def get_support_workers_tenants():
    """Return all support workers including their assigned tenants."""
    stmt = db.select(SupportWorker).options(
        selectinload(SupportWorker.tenants)
    )
    workers = db.session.execute(stmt).scalars().all()
    return support_workers_with_tenants_schema.dump(workers), 200

# ============================================================
# POST: Create a New Support Worker
# ============================================================
@support_workers_bp.route("/", methods=["POST"])
def create_support_worker():
    """Create a new support worker and return it."""
    worker_fields = support_worker_schema.load(request.json)

    new_worker = SupportWorker(
        name=worker_fields["name"],
        phone=worker_fields["phone"],
        email=worker_fields["email"]
    )

    db.session.add(new_worker)
    db.session.commit()

    return jsonify(support_worker_schema.dump(new_worker)), 201

# ============================================================
# DELETE: Delete Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["DELETE"])
def delete_support_worker(support_worker_id):
    """Delete a support worker by ID and return the deleted record."""
    worker = db.get(SupportWorker, support_worker_id)

    if not worker:
        return abort(404, description="Support Worker not found")

    db.session.delete(worker)
    db.session.commit()

    return jsonify(support_worker_schema.dump(worker)), 200

# ============================================================
# PUT: Update Support Worker by ID
# ============================================================
@support_workers_bp.route("/<int:support_worker_id>/", methods=["PUT"])
def update_support_worker(support_worker_id):
    """Update an existing support worker with provided fields."""

    worker_fields = support_worker_schema.load(request.json, partial=True)

    stmt = db.select(SupportWorker).filter_by(id=support_worker_id)
    worker_obj = db.session.scalar(stmt)

    # Apply updates if provided
    if not worker_obj:
        return abort(404, description="Support Worker does not exist")

    if "name" in worker_fields:
        worker_obj.name = worker_fields["name"]
    if "email" in worker_fields:
        worker_obj.email = worker_fields["email"]
    if "phone" in worker_fields:
        worker_obj.phone = worker_fields["phone"]

    db.session.commit()

    return jsonify(support_worker_schema.dump(worker_obj)), 200
