from django.urls import path
from userauth.views import AttendeeLogin

urlpatterns =[
    path("login", AttendeeLogin.as_view())
]