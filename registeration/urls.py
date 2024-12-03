from django.urls import path
from .views import Registration, ViewAttendance, ViewAttendee, AttendeeUpdate, Login, GetUserTag, CreateRegistrar,ListRegistrar

urlpatterns = [
    path("new-registration", Registration.as_view()),
    path("update/<pk>", AttendeeUpdate.as_view()),
    path("attendance", ViewAttendance.as_view(), name="attendance"),
    path("view-attendee/<pk>", ViewAttendee.as_view(), name="view"),
    path("login", Login.as_view()),
    path("get-user-tag", GetUserTag.as_view()),
    path("registrar-all", ListRegistrar.as_view()),
    path("create-registrar", CreateRegistrar.as_view())
]
