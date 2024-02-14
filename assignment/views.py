from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Assignment, Examination, Course, Teacher, TeacherYear
from drf_spectacular.utils import extend_schema

from utils.check_user import check_user
from utils.generate_token import generate_random_token
from utils.send_email import send_email


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
            assignment_obj.tracking_token = generate_random_token()
            assignment_obj.save()
            link = f"http://127.0.0.1:8000/assignment/set_paper_setter_decision?exam_id={exam.eid}&course_code={course.code}&token={assignment_obj.tracking_token}&has_approved="
            send_email(paper_setter.user.email, subject="Invitation to set Question paper", htmlContent= f"<html><head></head><body><p>Hello,</p>You have been invited to set question paper. Awaiting your response: 1.<a href = {link+'1'}>Accept</a> 2.<a href = {link+'0'}>Reject</a></p></body></html>")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})

@extend_schema(tags=['Assignment'])
@api_view(["GET"])
def set_paper_setter_decision(request):
    try:
        tracking_token = request.GET.get("token")
        exam_id = request.GET.get("exam_id")
        course_code = request.GET.get("course_code")
        has_approved = int(request.GET.get("has_approved"))==1
        exam = Examination.objects.get(eid=exam_id)
        course = Course.objects.get(code=course_code)
        assignment = Assignment.objects.get(exam=exam, course=course)

        if assignment.tracking_token!=tracking_token:
            raise Exception("Invalid Token")

        if assignment.status!="Request Pending":
            raise Exception("Invalid Status: Invitation has already been responded to.")

        if has_approved:
            assignment.status = "In Progress"
        else:
            assignment.status = "Invite Rejected"
        assignment.save()

        return HttpResponse(f"Thanks for your response. Status Updated - {assignment.status}")
    except Exception as e:
        return JsonResponse({"error": str(e)})



# NOT USED FOR NOW
# @extend_schema(tags=['Assignment'])
# @api_view(["POST"])
# def set_paper_setter_decision(request):
#     '''
#     REQUEST Data -
#     {
#         "email": "x@a.com",
#         "exam_id":1,
#         "course_code": "20CS710",
#         has_approved:true
#     }
#     '''
#     try:
#         email = request.data["email"]
#         password = request.data["password"]
#         if check_user(email, password):
#             exam_id = request.data["exam_id"]
#             course_code = request.data["course_code"]
#             has_approved = request.data["has_approved"]
#             exam = Examination.objects.get(eid=exam_id)
#             course = Course.objects.get(code=course_code)
#             assignment = Assignment.objects.get(exam=exam, course=course)

#             if has_approved:
#                 assignment.status = "In Progress"
#             else:
#                 assignment.status = "Invite Rejected"
#             assignment.save()

#             return JsonResponse({"success": True})
#         else:
#             raise Exception("Invalid Credentials")
#     except Exception as e:
#         return JsonResponse({"error": str(e)})