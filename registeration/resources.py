from import_export import resources
from .models import Attendee, Registrar

class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = ('surname', 'other_name', 'email', 'phone', 'cys_code','church') 
        export_order = ('surname', 'other_name', 'email', 'phone', 'cys_code')  

class RegistrarResource(resources.ModelResource):
    class Meta:
        model = Registrar
        fields = ('surname', 'other_name', 'email', 'phone')
        export_order = ('surname', 'other_name', 'email', 'phone')
