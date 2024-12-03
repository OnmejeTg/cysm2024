from django.db import models

from registeration.models import Attendee, Registrar

# Create your models here.


class Program(models.Model):
    name = models.CharField(max_length=255)
    start_datetime = models.DateField()
    end_datetime = models.DateField()
    theme = models.TextField(max_length=500, blank=True, null=True)
    flyer = models.ImageField(upload_to="program_images/", null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added for tracking updates

    def __str__(self):
        return self.name
    
class ProgramRegistration(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(Registrar, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added for tracking updates

    def __str__(self):
        return self.attendee.cys_code

class ProgramAuthentication(models.Model):
    '''
    this model is for tracking attendee that attendded the programe by getting 
    their tags on site, once tag is printed on site this model will be populated 
    there by we keep track of those who attended
    '''
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.attendee.cys_code} {self.program.name}"
    