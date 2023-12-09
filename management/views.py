from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Examination, Course
from .serializers import *
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Exams'])
class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Courses'])
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
