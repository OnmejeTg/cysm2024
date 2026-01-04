from django.contrib import admin
from . models import Attendee, Registrar
# Register your models here.
admin.site.register(Attendee)
admin.site.register(Registrar)

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')  
    search_fields = ('first_name', 'last_name', 'email', 'phone','cys_code')
    list_filter = ('created_at',)

@admin.register(Registrar)
class RegistrarAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')  
    search_fields = ('first_name', 'last_name', 'email', 'phone','cys_code')
    list_filter = ('created_at',)   