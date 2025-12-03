from extensions import ma
from Models.tenant import Tenant

class TenantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenant
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    date_of_birth = ma.auto_field()
    phone = ma.auto_field()
    email = ma.auto_field()

tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class TenantSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "date_of_birth", "name", "phone", "email")

# # single competition schema, when one competition needs to be retrieved
# tenant_schema = TenantSchema()
# # multiple competition schema, when many competitions need to be retrieved
# tenants_schema = TenantSchema(many=True)