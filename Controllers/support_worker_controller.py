from flask import Blueprint, jsonify, request, abort
from extensions import db
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
    stmt = db.select(SupportWorker)
    workers_list = db.session.scalars(stmt)
    return jsonify(support_workers_schema.dump(workers_list))

# -------------------------
# GET a single support worker by support_worker_id
# -------------------------
@support_workers_bp.route("/<int:support_worker_id>/", methods=["GET"])
def get_support_worker(support_worker_id):
    stmt = db.select(SupportWorker).filter_by(id=support_worker_id)
    support_worker_obj = db.session.scalar(stmt)
    #return an error if the competition doesn't exist
    if not support_worker_obj:
        return abort(400, description= "Support Worker does not exist")
    # Convert the competitions from the database into a JSON format and store them in result
    result = support_worker_schema.dump(support_worker_obj)
    # return the data in JSON format
    return jsonify(result)

# -------------------------
# CREATE a new support worker
# -------------------------
@support_workers_bp.route("/", methods=["POST"])
def create_support_worker():
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
# DELETE a support worker by support_worker_id
# -------------------------
@support_workers_bp.route("/<int:support_worker_id>/", methods=["DELETE"])
def delete_support_worker(support_worker_id):
    worker = db.get(SupportWorker, support_worker_id)
    if not worker:
        return abort(404, description="Support Worker not found")

    db.session.delete(worker)
    db.session.commit()
    return jsonify(support_worker_schema.dump(worker)), 200

# -------------------------
# UPDATE a support worker by support_worker_id
# -------------------------
@support_workers_bp.route("/<int:support_worker_id>/", methods=["PUT"])
def update_support_worker(support_worker_id):
    worker = db.get(SupportWorker, support_worker_id)
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
@support_workers_bp.route("/<int:support_worker_id>/link_tenant/<int:tenant_id>/", methods=["POST"])
def link_tenant(support_worker_id, tenant_id):
    worker = db.get(SupportWorker, support_worker_id)
    if not worker:
        return abort(404, description="Support Worker not found")

    # Check if link already exists
    existing_link = db.session.scalar(
        db.select(TenantSupportWorker)
        .filter_by(support_worker_id=support_worker_id, tenant_id=tenant_id)
    )
    if existing_link:
        return abort(400, description="Tenant already linked to this support worker")

    new_link = TenantSupportWorker(
        support_worker_id=support_worker_id,
        tenant_id=tenant_id
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": f"Tenant {tenant_id} linked to Support Worker {support_worker_id}"}), 201
