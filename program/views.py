from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status

from registeration.models import Attendee, Registrar
from registeration.serializers import AttendeeSerializer
from .serializers import (
    GetAttendeeSerializer,
    ProgramSerializer,
    ProgramRegisterSerializer,
)
from .models import Program, ProgramRegistration
from rest_framework.response import Response
from django_filters import rest_framework as filters

# Create your views here.
class Createprogram(generics.CreateAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()


class Register(generics.CreateAPIView):
    serializer_class = ProgramRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        program_id = serializer.validated_data.get("programe_id")
        user_cys_code = serializer.validated_data.get("user_cys_code")
        registrar_cys_code = serializer.validated_data.get("registrar_cys_code")

        program = get_object_or_404(Program, id=program_id)
        attendee = get_object_or_404(Attendee, cys_code=user_cys_code)

        if ProgramRegistration.objects.filter(attendee=attendee, program=program).exists():
            return Response({"Warning": "You have already registered for this program"}, status=status.HTTP_208_ALREADY_REPORTED)
        
        program_reg = ProgramRegistration.objects.create(attendee=attendee, program=program)

        if registrar_cys_code:
            registrar = get_object_or_404(Registrar, reg_id=registrar_cys_code)
            program_reg.registered_by = registrar
            program_reg.save()

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
    
class GetAttendee(generics.ListAPIView):
    serializer_class = GetAttendeeSerializer
    queryset = ProgramRegistration.objects.all()
    search_fields = ['attendee', 'program', 'registered_by']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = search_fields
    

   

class AllPrograme(generics.ListAPIView):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()
    