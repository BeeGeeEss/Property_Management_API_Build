from extensions import ma
from Models.tenancy import Tenancy

class TenancySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tenancy
        load_instance = False

    id = ma.auto_field()
    property_id = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    tenancy_status = ma.auto_field()

tenancy_schema = TenancySchema()
tenancies_schema = TenancySchema(many=True)
