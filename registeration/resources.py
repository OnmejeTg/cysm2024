from import_export import resources, fields
from .models import Attendee, Registrar

class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = ('surname', 'other_name', 'email', 'phone', 'cys_code', 'church') 
        export_order = ('surname', 'other_name', 'email', 'phone', 'cys_code', 'church')  

class RegistrarResource(resources.ModelResource):
    surname = fields.Field(attribute='attendee__surname', column_name='Surname')
    other_name = fields.Field(attribute='attendee__other_name', column_name='Other Name')
    email = fields.Field(attribute='attendee__email', column_name='Email')
    phone = fields.Field(attribute='attendee__phone', column_name='Phone')

    class Meta:
        model = Registrar
        fields = ('surname', 'other_name', 'email', 'phone', 'reg_id')
        export_order = ('surname', 'other_name', 'email', 'phone', 'reg_id')
