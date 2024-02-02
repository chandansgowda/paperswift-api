from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Assignment, Examination, Course, Teacher, TeacherYear
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bulk_assign_paper_setters(request):
    '''
    Bulk Assign Paper Setters - POST JSON in this format -
{
     exam_id:1,
     assignments:[
        {
            course_code: 123123,
            paper_setter_id: 2
        },
        ...
    ]
}
    '''
    try:
        exam_id = request.data["exam_id"]
        assignments = request.data["assignments"]
        exam = Examination.objects.get(eid=exam_id)
        for assignment in assignments:
            course = Course.objects.get(code=assignment["course_code"])
            paper_setter = Teacher.objects.get(id=assignment["paper_setter_id"])
            assignment_obj = Assignment(exam=exam, course=course,paper_setter=paper_setter)
            assignment_obj.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})