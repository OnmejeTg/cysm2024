from django.contrib import admin
from .models import Program, ProgramRegistration, ProgramAuthentication
# Register your models here.

admin.site.register(Program)
admin.site.register(ProgramRegistration)
admin.site.register(ProgramAuthentication)

