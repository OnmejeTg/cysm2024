from rest_framework import serializers
from .models import Program, ProgramRegistration


class ProgramSerializer(serializers.ModelSerializer):
    flyer = serializers.FileField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = Program
        fields = "__all__"

class ProgramRegisterSerializer(serializers.Serializer):
    programe_id = serializers.CharField()
    user_cys_code = serializers.CharField()
    registrar_cys_code = serializers.CharField(required=False)

    

class GetAttendeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgramRegistration
        fields = "__all__"
        depth = 1