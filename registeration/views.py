from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from program.models import Program, ProgramAuthentication, ProgramRegistration
from .serializers import (
    AttendeeSerializer,
    CreateRegistrarSerializer,
    LoginSerializer,
    RegistrarSerializer,
    TagSerializer,
    UpdateAttendeeSerializer,
)
from .models import Attendee, Registrar
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import portrait
from reportlab.lib import colors
from django.conf import settings
import os

import logging
import traceback
from django.db import transaction

logger = logging.getLogger(__name__)

class Registration(generics.GenericAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = self.serializer_class(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()

            program_id = request.data.get('program')
            user_cys_code = serializer.data.get("cys_code")
            registrar_cys_code = request.data.get('registrar_cys_code')

            if program_id:
                try:
                    program = Program.objects.get(id=program_id)
                    attendee = Attendee.objects.get(cys_code=user_cys_code)
                    
                    program_reg, created = ProgramRegistration.objects.get_or_create(
                        attendee=attendee, program=program
                    )
                    
                    if registrar_cys_code:
                        try:
                            registrar = Registrar.objects.get(reg_id=registrar_cys_code)
                            program_reg.registered_by = registrar
                            program_reg.save()
                        except (Registrar.DoesNotExist, Exception):
                            pass
                except (Program.DoesNotExist, Attendee.DoesNotExist, Exception) as e:
                    logger.error(f"Program association failed: {str(e)}")

            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Registration Error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {"status": "error", "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ViewAttendance(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()
    filter_backends = (DjangoFilterBackend,)
    search_fields = [
        "id",
        "surname",
        "sex",
        "state",
        "occupation",
        "town_of_residence",
        "lga_of_residence",
        "school",
        "marital_status",
    ]
    filterset_fields = search_fields


class ViewAttendee(generics.GenericAPIView):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()

    def get(self, request, pk):
        attendee = get_object_or_404(Attendee, pk=pk)
        serializer_data = self.serializer_class(attendee).data
        if Registrar.objects.filter(attendee=attendee).exists():
            serializer_data['is_registrar'] = True
        else:
            serializer_data['is_registrar'] = False

        return Response({"data":serializer_data}, status=status.HTTP_200_OK)




class AttendeeUpdate(generics.UpdateAPIView):
    serializer_class = UpdateAttendeeSerializer
    queryset = Attendee.objects.all()


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        password = request.data["password"]
        username = request.data["username"]

        auth_user = User.objects.filter(username=username).first()
        if not auth_user or not check_password(password, auth_user.password):
            response_data = {
                "status": "error",
                "message": "Invalid credentials",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        user_type = None
        try:
            attendee_user = Attendee.objects.filter(cys_code=username)[0]
        except:
            attendee_user = None
        # staff_user = Staff.objects.filter(staff_id=username).first()

        if attendee_user:
            user_type = "admin"
        # elif staff_user:
        #     designation = staff_user.designation.lower()
        #     if designation in ["admin", "form master", "bursar"]:
        #         user_type = designation
        #     else:
        #         user_type = "invalid"

        if user_type is None:
            response_data = {
                "status": "error",
                "message": "User type not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(auth_user)
        response_data = {
            "status": "success",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_type": user_type,
            "user_id": attendee_user.id,
        }
        return Response(response_data)


class GetUserTag(generics.GenericAPIView):
    serializer_class = TagSerializer
    permission_classes = []

    def generate_pdf(self, response, content_width, content_height, attendee):
        c = Canvas(response, pagesize=portrait((4.13 * inch, 5.83 * inch)))

        left_margin = 0.2 * inch
        top_margin = 0.2 * inch

        c.setLineWidth(2)
        c.rect(left_margin, top_margin, content_width, content_height)

        def draw_text(font, size, x, y, text):
            c.setFont(font, size)
            c.drawString(x, y, text)

        def draw_colored_rectangle(x, y, width, height, color):
            c.setFillColor(color)
            c.rect(x, y, width, height, fill=True, stroke=False)

        def draw_image(image_path, x, y, width, height):
            c.drawImage(image_path, x, y, width=width, height=height)

        # Draw content

        image_path = os.path.join(settings.MEDIA_ROOT, 'logo-copy.png')
        draw_text("Helvetica-Bold", 15, 0.4 * inch, 4 * inch, "Christian Youth Summit Makurdi")
        draw_text("Helvetica-Bold", 10, 1.3 * inch, 3.8 * inch, "...in pursuit of revival")
        # draw_image("https://www.pythonanywhere.com/user/cysm/files/home/cysm/CYSM/media/logo-copy.png", 1.5 * inch, 4.2 * inch, width=70, height=70)
        draw_image(image_path, 1.5 * inch, 4.2 * inch, width=70, height=70)
        draw_text("Helvetica-Bold", 20.5, 1.2 * inch, 3.3 * inch, "Summit 2024")

        theme_text = "FOR THE MASTER'S USE"
        reference_text = "2 TIMOTHY 2:18"

        # Draw colored background rectangle
        draw_colored_rectangle(0.8 * inch, 2.85 * inch, 2.5 * inch, 0.4 * inch, colors.HexColor("#be202f"))

        # Draw theme text
        c.setFillColor(colors.white)
        draw_text("Helvetica", 9, 1 * inch, 3.1 * inch, "THEME: ")
        draw_text("Helvetica-Bold", 9, 1.5 * inch, 3.1 * inch, theme_text)

        # Draw reference text
        draw_text("Helvetica", 8, 1.6 * inch, 2.9 * inch, reference_text)

        # Draw attendee information
        c.setFillColor(colors.black)
        name = f'{attendee.surname} {attendee.other_name}'
        sex = attendee.sex
        bible_study = '___________'
        cys_id = attendee.cys_code

        draw_text("Helvetica", 11, 0.5 * inch, 2.3 * inch, 'Full Name:')
        draw_text("Helvetica-Bold", 12.5, 1.3 * inch, 2.3 * inch, name.upper())
        draw_text("Helvetica", 11, 0.5 * inch, 1.8 * inch, 'Sex:')
        draw_text("Helvetica-Bold", 12.5, 0.9 * inch, 1.8 * inch, sex.capitalize())
        draw_text("Helvetica", 11, 0.5 * inch, 1.3 * inch, 'Bible Study:')
        draw_text("Helvetica-Bold", 12.5, 1.4 * inch, 1.3 * inch, bible_study)

        # Draw CYS ID
        draw_colored_rectangle(1.3 * inch, 0.5 * inch, 0.7 * inch, 0.4 * inch, colors.HexColor("#be202f"))
        c.setFillColor(colors.white)
        draw_text("Helvetica-Bold", 12.5, 1.35 * inch, 0.65 * inch, "CYS ID:")
        c.setFillColor(colors.black)
        draw_text("Helvetica-Bold", 13, 2.1 * inch, 0.65 * inch, cys_id)

        c.save()

    def post(self, request):
        cys_code = self.request.data.get('cys_code')
        program_id = self.request.data.get('program_id')
        try:
            attendee = Attendee.objects.get(cys_code=cys_code)
            program = Program.objects.get(id=program_id)

        except:
            return Response({"error":"Invalid cys code or program id"}, status=status.HTTP_400_BAD_REQUEST)

        output_filename = f"{attendee.cys_code}.pdf"
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
        content_width = 3.7 * inch
        content_height = 5.4 * inch
        self.generate_pdf(response, content_width, content_height, attendee)

        if not ProgramAuthentication.objects.filter(program=program, attendee=attendee).exists():
            ProgramAuthentication.objects.create(program=program, attendee=attendee)

        return response

class ListRegistrar(generics.ListAPIView):
    serializer_class = RegistrarSerializer
    queryset = Registrar.objects.all()


class CreateRegistrar(generics.GenericAPIView):
    serializer_class = CreateRegistrarSerializer

    def post(self, request):
        cys_code = self.request.data.get("cys_code")

        try:
            attendee = Attendee.objects.get(cys_code=cys_code)
        except Attendee.DoesNotExist:
            return Response(
                {"Error": "Invalid csy_code"}, status=status.HTTP_404_NOT_FOUND
            )

        registrar_exists = Registrar.objects.filter(attendee=attendee).exists()
        if registrar_exists:
            return Response(
                {"Error": "Registrar already exists for this attendee"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            last_entry = Registrar.objects.latest("reg_id")
            last_entry_count = int(last_entry.reg_id.split("-")[-1]) + 1
        except Registrar.DoesNotExist:
            last_entry_count = 1

        formatted_id = "%03d" % last_entry_count
        reg_id = f"REG-{formatted_id}"

        Registrar.objects.create(attendee=attendee, reg_id=reg_id)

        return Response(
            {"Success": "Registrar created successfully"},
            status=status.HTTP_201_CREATED,
        )
