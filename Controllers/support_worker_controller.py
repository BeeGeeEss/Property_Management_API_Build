from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from extensions import db
from Models.support_worker import SupportWorker
from Schemas.support_worker_schema import support_worker_schema, support_workers_schema, support_workers_with_tenants_schema

# Blueprint definition
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
# GET a support workers & tenants
# -------------------------
@support_workers_bp.route("/tenants", methods=["GET"])
def get_support_workers_tenants():
    stmt = db.select(SupportWorker).options(
        selectinload(SupportWorker.tenants)
    )
    workers = db.session.execute(stmt).scalars().all()
    return support_workers_with_tenants_schema.dump(workers), 200

# -------------------------
# CREATE a new support worker
# -------------------------
@support_workers_bp.route("/", methods=["POST"])
def create_support_worker():
    worker_fields = support_worker_schema.load(request.json)

    new_worker = SupportWorker()
    new_worker.name = worker_fields["name"]
    new_worker.phone = worker_fields["phone"]
    new_worker.email = worker_fields["email"]
    # add to the database and commit
    db.session.add(new_worker)
    db.session.commit()
    # return the competition in the response
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

    worker_fields = support_worker_schema.load(request.json, partial=True)

    stmt = db.select(SupportWorker).filter_by(id=support_worker_id)
    worker_obj = db.session.scalar(stmt)

    if not worker_obj:
        return abort(400, description="Support Worker does not exist")

    if "name" in worker_fields:
        worker_obj.name = worker_fields["name"]

    if "email" in worker_fields:
        worker_obj.email = worker_fields["email"]

    if "phone" in worker_fields:
        worker_obj.phone = worker_fields["phone"]

    db.session.commit()

    return jsonify(support_worker_schema.dump(worker_obj)), 200

