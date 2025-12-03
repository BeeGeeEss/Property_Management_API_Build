from flask import Blueprint, jsonify, request, abort
from main import db
from Models.support_worker import SupportWorker
from Models.tenant_support_worker import TenantSupportWorker
from Schemas.support_worker_schema import support_worker_schema, support_workers_schema

support_workers_bp = Blueprint(
    'support_workers', __name__, url_prefix="/support_workers"
)

# -------------------------
# GET all support workers
# -------------------------
@support_workers_bp.route("/", methods=["GET"])
def get_support_workers():
    """Docstring"""
    stmt = db.select(SupportWorker)
    workers_list = db.session.scalars(stmt)
    result = support_workers_schema.dump(workers_list)
    return jsonify(result)

# -------------------------
# GET a single support worker by ID
# -------------------------
@support_workers_bp.route("/<int:id>/", methods=["GET"])
def get_support_worker(id):
    """Docstring"""
    worker = db.get(SupportWorker, id)
    if not worker:
        return abort(404, description="Support Worker not found")
    return jsonify(support_worker_schema.dump(worker))

# -------------------------
# CREATE a new support worker
# -------------------------
@support_workers_bp.route("/", methods=["POST"])
def create_support_worker():
    """Docstring"""
    worker_fields = support_worker_schema.load(request.json)

    new_worker = SupportWorker(
        name=worker_fields["name"],
        phone=worker_fields.get("phone"),
        email=worker_fields["email"]
    )

    db.session.add(new_worker)
    db.session.commit()
    return jsonify(support_worker_schema.dump(new_worker)), 201

# -------------------------
# DELETE a support worker by ID
# -------------------------
@support_workers_bp.route("/<int:id>/", methods=["DELETE"])
def delete_support_worker(id):
    """Docstring"""
    worker = db.get(SupportWorker, id)
    if not worker:
        return abort(404, description="Support Worker not found")

    db.session.delete(worker)
    db.session.commit()
    return jsonify(support_worker_schema.dump(worker)), 200

# -------------------------
# UPDATE a support worker by ID
# -------------------------
@support_workers_bp.route("/<int:id>/", methods=["PUT"])
def update_support_worker(id):
    """Docstring"""
    worker = db.get(SupportWorker, id)
    if not worker:
        return abort(404, description="Support Worker not found")

    worker_fields = support_worker_schema.load(request.json, partial=True)

    if "name" in worker_fields:
        worker.name = worker_fields["name"]
    if "phone" in worker_fields:
        worker.phone = worker_fields["phone"]
    if "email" in worker_fields:
        worker.email = worker_fields["email"]

    db.session.commit()
    return jsonify(support_worker_schema.dump(worker)), 200

# -------------------------
# OPTIONAL: Link a tenant to a support worker
# -------------------------
@support_workers_bp.route("/<int:worker_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(worker_id, tenant_id):
    """Docstring"""
    worker = db.get(SupportWorker, worker_id)
    if not worker:
        return abort(404, description="Support Worker not found")

    # Check if link already exists
    existing_link = db.session.scalar(
        db.select(TenantSupportWorker)
        .filter_by(support_worker_id=worker_id, tenant_id=tenant_id)
    )
    if existing_link:
        return abort(400, description="Tenant already linked to this support worker")

    new_link = TenantSupportWorker(
        support_worker_id=worker_id,
        tenant_id=tenant_id
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": f"Tenant {tenant_id} linked to Support Worker {worker_id}"}), 201
