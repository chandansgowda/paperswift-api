from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Assignment, Examination, Course, Teacher, TeacherYear
from drf_spectacular.utils import extend_schema

from utils.check_user import check_user
from utils.send_email import send_email


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
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
            #TODO: Send email to the paper setter asking for approval
            send_email(paper_setter.user.email, subject="Invitation to set Question paper", htmlContent="<html><head></head><body><p>Hello,</p>You have been invited to set question paper. Please use this link to accept the invite - google.com</p></body></html>")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
def set_paper_setter_decision(request):
    '''
    REQUEST Data -
    {
        "email": "x@a.com",
        "exam_id":1,
        "course_code": "20CS710",
        has_approved:true
    }
    '''
    try:
        email = request.data["email"]
        password = request.data["password"]
        if check_user(email, password):
            exam_id = request.data["exam_id"]
            course_code = request.data["course_code"]
            has_approved = request.data["has_approved"]
            exam = Examination.objects.get(eid=exam_id)
            course = Course.objects.get(code=course_code)
            assignment = Assignment.objects.get(exam=exam, course=course)

            if has_approved:
                assignment.status = "In Progress"
            else:
                assignment.status = "Invite Rejected"
            assignment.save()

            return JsonResponse({"success": True})
        else:
            raise Exception("Invalid Credentials")
    except Exception as e:
        return JsonResponse({"error": str(e)})