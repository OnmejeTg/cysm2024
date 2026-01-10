from django.contrib import admin
from datetime import datetime   
from . models import Attendee, Registrar
from .resources import AttendeeResource, RegistrarResource  
from import_export.admin import ImportExportModelAdmin



class RegistrationDateFilter(admin.SimpleListFilter):
    title = 'Specific Registration Date'
    parameter_name = 'reg_date'
    
    def lookups(self, request, model_admin):
        dates = Attendee.objects.dates('created_at','day',order='DESC')
        return [(date.strftime('%Y-%m-%d'), date.strftime('%d %b, %Y')) for date in dates]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__date=self.value())
        return queryset



@admin.register(Attendee)
class AttendeeAdmin(ImportExportModelAdmin):
    list_display = ('surname', 'other_name', 'email', 'phone', 'created_at')  
    search_fields = ('surname', 'other_name', 'email', 'phone', 'cys_code')
    list_filter = (RegistrationDateFilter,)
    resource_class = AttendeeResource

@admin.register(Registrar)
class RegistrarAdmin(ImportExportModelAdmin):
    list_display = ('get_surname', 'get_other_name', 'get_email', 'get_phone', 'get_created_at')  
    search_fields = ('attendee__surname', 'attendee__other_name', 'attendee__email', 'attendee__phone', 'attendee__cys_code')
    resource_class = RegistrarResource
    
    def get_surname(self, obj):
        return obj.attendee.surname
    get_surname.short_description = 'Surname'
    
    def get_other_name(self, obj):
        return obj.attendee.other_name
    get_other_name.short_description = 'Other Name'

    def get_email(self, obj):
        return obj.attendee.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.attendee.phone
    get_phone.short_description = 'Phone'

    def get_created_at(self, obj):
        return obj.attendee.created_at
    get_created_at.short_description = 'Registered At'