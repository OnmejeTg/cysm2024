from django.urls import path
from .views import Createprogram, Register, GetAttendee, AllPrograme

urlpatterns = [
    path("create", Createprogram.as_view()),
    path("register", Register.as_view()),
    path("get-attendees", GetAttendee.as_view()),
    path("all", AllPrograme.as_view()),
]