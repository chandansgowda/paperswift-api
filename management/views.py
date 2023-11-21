from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Examination
from .serializers import ExaminationSerializer


class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]
