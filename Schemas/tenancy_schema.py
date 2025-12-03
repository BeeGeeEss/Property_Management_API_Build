from extensions import ma
from Models.tenancy import Tenancy

class TenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenancy
        load_instance = True

    id = ma.auto_field()
    property_id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()

tenancy_schema = TenancySchema()
tenancies_schema = TenancySchema(many=True)


# # create the Competition Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
# class TenancySchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "start_date", "end_date", "tenancy_status", "property_id")

# # single competition schema, when one competition needs to be retrieved
# tenancy_schema = TenancySchema()
# # multiple competition schema, when many competitions need to be retrieved
# tenancies_schema = TenancySchema(many=True)