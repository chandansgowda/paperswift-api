from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Degree, Examination, Course, TeacherYear
from .serializers import *
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User


@extend_schema(tags=['Degrees'])
class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


@extend_schema(tags=['Schemes'])
class SchemeViewSet(viewsets.ModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer


@extend_schema(tags=['Exams'])
class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Departments'])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Courses'])
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Teachers'])
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.create_user(
            email=request.data["email"], password='welcome', username=request.data["email"])
        user.save()
        request._full_data = {**request.data, "user": user.id}
        print(user)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=['Teachers'])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_teachers_by_year(request):
    """""
    Get all paper setters by academic year (start year)
    """""
    try:
        year = int(request.query_params.get('year'))
        teacher_year_records = TeacherYear.objects.filter(year=year)
        response = {"teachers": [], "count": len(teacher_year_records)}
        for teacher_record in teacher_year_records:
            response["teachers"].append(model_to_dict(teacher_record.teacher))
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)})


@extend_schema(tags=['Teachers'])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def clone_teacher_list(request):
    '''
    Clone teacher list from previous academic year. Format - {"year":2000,"teacher_ids":[1,2]}
    Here year is the target academic year and teacher_ids are the ids of teachers to be cloned
    '''
    try:
        year = request.data["year"]
        teacher_ids = request.data["teacher_ids"]
        for teacher_id in teacher_ids:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_year = TeacherYear(teacher=teacher, year=year)
            teacher_year.save()
            print("Done")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})
