from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Attendee, Registrar
from datetime import datetime
from django.contrib.auth.models import User


class AttendeeSerializer(serializers.ModelSerializer):
    program = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    registrar_cys_code = serializers.CharField(required=False)

    class Meta:
        model = Attendee
        fields = [
            "id",
            "attendee_user",
            "dob",
            "mob",
            "cys_code",
            "surname",
            "other_name",
            "sex",
            "email",
            "phone",
            "age_bracket",
            "state",
            "lga_of_residence",
            "town_of_residence",
            "place_of_work",
            "occupation",
            "school",
            "sch_fellowship",
            "church",
            "marital_status", 
            "program",
            "registrar_cys_code",
        ]
        read_only_fields = ["cys_code", "attendee_user"]

    def create(self, validated_data):
        validated_data["surname"] = validated_data["surname"].upper().strip()
        validated_data["other_name"] = validated_data["other_name"].capitalize().strip()
        validated_data["sex"] = validated_data["sex"].strip().upper()[0]
        current_year = str(datetime.now().year)[2:]
        last_entry_count = (
            int(Attendee.objects.latest("created_at").cys_code.split("-")[-1][1:]) + 1
            if Attendee.objects.exists()
            else 1
        )

        validated_data[
            "cys_code"
        ] = f"CYS{current_year}-{validated_data['sex']}{last_entry_count}"
        attendee_user = User.objects.create_user(
            username=validated_data["cys_code"],
            password=validated_data["surname"].lower(),
            first_name=validated_data["surname"],
            last_name=validated_data["other_name"],
        )
        validated_data["attendee_user"] = attendee_user
        # import pdb; pdb.set_trace()
        obj = Attendee.objects.create(
           attendee_user=attendee_user,
           dob=validated_data.pop("dob", None),
           mob=validated_data.pop("mob", None),
           cys_code=validated_data.pop("cys_code", None),
           surname=validated_data.pop("surname", None),
           other_name=validated_data.pop("other_name", None),
           sex=validated_data.pop("sex", None),
           phone=validated_data.pop("phone", None),
           email=validated_data.pop("email", None),
           age_bracket=validated_data.pop("age_bracket", None),
           state=validated_data.pop("state", None),
           lga_of_residence=validated_data.pop("lga_of_residence", None),
           town_of_residence=validated_data.pop("town_of_residence", None),
           place_of_work=validated_data.pop("place_of_work", None),
           occupation=validated_data.pop("occupation", None),
           school=validated_data.pop("school", None),
           sch_fellowship=validated_data.pop("sch_fellowship", None),
           church=validated_data.pop("church", None),
           marital_status=validated_data.pop("marital_status", None),
          
        )

        return obj

class UpdateAttendeeSerializer(serializers.ModelSerializer):
    surname = serializers.CharField(required=False)
    other_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    lga_of_residence = serializers.CharField(required=False)
    town_of_residence = serializers.CharField(required=False)
    occupation = serializers.CharField(required=False)
    school = serializers.CharField(required=False)
    sch_fellowship = serializers.CharField(required=False)
    church = serializers.CharField(required=False)
    marital_status = serializers.CharField(required=False)

    class Meta:
        model = Attendee
        fields = [
            "surname",
            "other_name",
            "email",
            "phone",
            "state",
            "lga_of_residence",
            "town_of_residence",
            "occupation",
            "school",
            "sch_fellowship",
            "church",
            "marital_status",
        ]

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == "surname":
                setattr(instance, field, validated_data[field].upper())
                applicant_user = User.objects.get(username=instance.cys_code)
                applicant_user.first_name = validated_data[field]
                applicant_user.save()
            elif field == "other_name":
                setattr(instance, field, validated_data[field].capitalize())
                applicant_user = User.objects.get(username=instance.cys_code)
                applicant_user.last_name = validated_data[field]
                applicant_user.save()
            else:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TagSerializer(serializers.Serializer):
    cys_code = serializers.CharField()
    program_id = serializers.CharField()


class RegistrarSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Registrar
        fields = '__all__'


class CreateRegistrarSerializer(serializers.Serializer):
    cys_code = serializers.CharField()
    