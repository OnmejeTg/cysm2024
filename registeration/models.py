from django.db import models
from django.contrib.auth.models import User


class Attendee(models.Model):


    AGE_BRACKET_CHOICES = [
         ('1977-1923', '1977-1923'),
        ('1987-1978', '1987-1978'),
        ('2003-1988', '2003-1988'),
        ('2010-2004', '2010-2004'),
        ('2023-2011', '2023-2011'),
    ]

    attendee_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cys_code = models.CharField(max_length=100, unique=True)
    surname = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    dob = models.CharField(max_length=2, null=True, blank=True)
    mob = models.CharField(max_length=2, null=True, blank=True)
    age_bracket = models.CharField(max_length=50, choices=AGE_BRACKET_CHOICES, null=True)
    state = models.CharField(max_length=100)
    lga_of_residence = models.CharField(max_length=100)
    town_of_residence = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    place_of_work = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    sch_fellowship = models.CharField(max_length=100, null=True, blank=True)
    church = models.CharField(max_length=100, null=False, blank=False)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.surname} {self.other_name}"

class Registrar(models.Model):
    
    # Additional fields for Registrars
    reg_id = models.CharField(max_length=50)
    attendee = models.OneToOneField(Attendee, on_delete=models.CASCADE)
    is_registrar = models.BooleanField(default=True)
    # Add any additional fields or methods specific to Registrars
    # ...
    def __str__(self):
        return f"{self.attendee.surname} {self.attendee.other_name} (Registrar)"
