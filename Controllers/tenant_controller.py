from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import selectinload
from extensions import db
from Models.tenant import Tenant
from Models.tenancy import Tenancy
from Models.support_worker import SupportWorker
from Models.tenant_tenancy import TenantTenancy
from Models.tenant_support_worker import TenantSupportWorker
from Schemas.tenant_schema import tenant_schema, tenants_schema, tenants_with_tenancies_schema, tenants_with_support_worker_schema

# Blueprint definition
tenants_bp = Blueprint(
    'tenants', __name__, url_prefix="/tenants"
)

# -------------------------
# GET all tenants
# -------------------------
@tenants_bp.route("/", methods=["GET"])
def get_tenants():
    stmt = db.select(Tenant)
    tenants_list = db.session.scalars(stmt)
    return jsonify(tenants_schema.dump(tenants_list))

# -------------------------
# GET a single tenant by tenant_id
# -------------------------
@tenants_bp.route("/<int:tenant_id>/", methods=["GET"])
def get_tenant(tenant_id):
    stmt = db.select(Tenant).filter_by(id=tenant_id)
    tenant_obj = db.session.scalar(stmt)
    #return an error if the competition doesn't exist
    if not tenant_obj:
        return abort(400, description= "Tenant does not exist")
    # Convert the competitions from the database into a JSON format and store them in result
    result = tenant_schema.dump(tenant_obj)
    # return the data in JSON format
    return jsonify(result)

# -------------------------
# GET tenants & tenancies
# -------------------------
@tenants_bp.route("/tenancies", methods=["GET"])
def get_tenants_with_tenancies():
    stmt = db.select(Tenant).options(selectinload(Tenant.tenancies))
    tenants = db.session.scalars(stmt).all()
    return jsonify(tenants_with_tenancies_schema.dump(tenants))

# -------------------------
# GET tenants & support workers
# -------------------------
@tenants_bp.route("/support_workers", methods=["GET"])
def get_tenants_support_workers():
    stmt = db.select(Tenant).options(
        selectinload(Tenant.support_workers)
    )
    tenants = db.session.execute(stmt).scalars().all()
    return tenants_with_support_worker_schema.dump(tenants), 200

# -------------------------
# CREATE a new tenant
# -------------------------
@tenants_bp.route("/", methods=["POST"])
def create_tenant():
    tenant_fields = tenant_schema.load(request.json)
    new_tenant = Tenant(
        name=tenant_fields["name"],
        date_of_birth=tenant_fields["date_of_birth"],
        phone=tenant_fields.get("phone"),
        email=tenant_fields.get("email")
    )

    db.session.add(new_tenant)
    db.session.commit()
    return jsonify(tenant_schema.dump(new_tenant)), 201

# -------------------------
# DELETE a tenant by tenant_id
# -------------------------
@tenants_bp.route("/<int:tenant_id>/", methods=["DELETE"])
def delete_tenant(tenant_id):
    tenant = db.get(Tenant, tenant_id)
    if not tenant:
        return abort(404, description="Tenant not found")

    db.session.delete(tenant)
    db.session.commit()
    return jsonify(tenant_schema.dump(tenant)), 200

# -------------------------
# UPDATE a tenant by tenant_id
# -------------------------
@tenants_bp.route("/<int:tenant_id>/", methods=["PUT"])
def update_tenant(tenant_id):

    tenant_fields = tenant_schema.load(request.json, partial=True)

    stmt = db.select(Tenant).filter_by(id=tenant_id)
    tenant_obj = db.session.scalar(stmt)

    if not tenant_obj:
        return abort(400, description="Tenant does not exist")

    if "name" in tenant_fields:
        tenant_obj.name = tenant_fields["name"]

    if "email" in tenant_fields:
        tenant_obj.email = tenant_fields["email"]

    if "phone" in tenant_fields:
        tenant_obj.phone = tenant_fields["phone"]

    if "support_worker_id" in tenant_fields:
        tenant_obj.support_worker_id = tenant_fields["support_worker_id"]

    db.session.commit()

    return jsonify(tenant_schema.dump(tenant_obj)), 200

# -------------------------
# LINK tenant to tenancy
# -------------------------
@tenants_bp.route("/<int:tenant_id>/link_tenancy/<int:tenancy_id>/", methods=["POST"])
def link_tenancy(tenant_id, tenancy_id):
    tenant = db.get(Tenant, tenant_id)
    tenancy = db.get(Tenancy, tenancy_id)

    if not tenant or not tenancy:
        return abort(404, description="Tenant or Tenancy not found")

    # Prevent duplicate links
    existing_link = db.session.scalar(
        db.select(TenantTenancy)
        .filter_by(tenant_id=tenant_id, tenancy_id=tenancy_id)
    )
    if existing_link:
        return abort(400, description="Tenant already linked to this tenancy")

    new_link = TenantTenancy(
        tenant_id=tenant_id,
        tenancy_id=tenancy_id
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": f"Tenant {tenant_id} linked to Tenancy {tenancy_id}"}), 201

# -------------------------
# LINK tenant to support worker
# -------------------------
@tenants_bp.route("/<int:tenant_id>/link_support_worker/<int:worker_id>/", methods=["POST"])
def link_support_worker(tenant_id, worker_id):
    tenant = db.get(Tenant, tenant_id)
    worker = db.get(SupportWorker, worker_id)

    if not tenant or not worker:
        return abort(404, description="Tenant or Support Worker not found")

    # Prevent duplicate links
    existing_link = db.session.scalar(
        db.select(TenantSupportWorker)
        .filter_by(tenant_id=tenant_id, support_worker_id=worker_id)
    )
    if existing_link:
        return abort(400, description="Tenant already linked to this support worker")

    new_link = TenantSupportWorker(
        tenant_id=tenant_id,
        support_worker_id=worker_id
    )
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": f"Tenant {tenant_id} linked to Support Worker {worker_id}"}), 201
