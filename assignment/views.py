from datetime import datetime
import hashlib
import json
import os
import logging
from time import timezone
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Assignment, Examination, Course, Teacher, TeacherYear
from drf_spectacular.utils import extend_schema
from paperswift_api import settings

from utils.check_user import check_user
from utils.generate_token import generate_random_token
from utils.html_content import get_invitation_html, get_qp_details_html
from utils.send_email import send_email

logger = logging.getLogger('logger')


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
            paper_setter = Teacher.objects.get(
                id=assignment["paper_setter_id"])
            assignment_obj, created = Assignment.objects.update_or_create(
                exam=exam, course=course, defaults={
                    "paper_setter": paper_setter,
                    "status": 'Request Pending',
                    "assigned_date": datetime.now(),
                })
            assignment_obj.tracking_token = generate_random_token()
            link = f"http://127.0.0.1:8000/assignment/set_paper_setter_decision?exam_id={exam.eid}&course_code={course.code}&token={assignment_obj.tracking_token}&has_approved="
            send_email(paper_setter.user.email, subject="Invitation to set Question paper",
                       htmlContent=get_invitation_html(semester=exam.sem, course_code=course.code, course_name=course.name, branch=course.department, deadline=exam.paper_submission_deadline, link=link))
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["GET"])
def set_paper_setter_decision(request):
    try:
        tracking_token = request.GET.get("token")
        exam_id = request.GET.get("exam_id")
        course_code = request.GET.get("course_code")
        has_approved = int(request.GET.get("has_approved")) == 1
        exam = Examination.objects.get(eid=exam_id)
        course = Course.objects.get(code=course_code)
        assignment = Assignment.objects.get(exam=exam, course=course)

        if assignment.tracking_token != tracking_token:
            raise Exception("Invalid Token")

        if assignment.status != "Request Pending":
            raise Exception(
                "Invalid Status: Invitation has already been responded to.")

        if has_approved:
            assignment.status = "In Progress"
        else:
            assignment.status = "Invite Rejected"
        assignment.save()

        if assignment.status == "In Progress":
            send_email(assignment.paper_setter.user.email, subject="Question Paper Details", htmlContent=get_qp_details_html(
                syllabus_copy_link=course.syllabus_doc_url, upload_link="#", deadline=exam.paper_submission_deadline, course_code=course.code, course_name=course.name, branch=course.department, semester=exam.sem, name=assignment.paper_setter.name))

        return HttpResponse(f"Thanks for your response. Status Updated - {assignment.status}")
    except Exception as e:
        return HttpResponse("ERROR: "+str(e), status=500)


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
def upload_question_paper(request):
    try:
        tracking_token = request.data["tracking_token"]
        exam_id = request.data["exam_id"]
        course_code = request.data["course_code"]

        assignmentObj = Assignment.objects.get(
            exam__eid=exam_id, course__code=course_code)
        if assignmentObj.tracking_token != tracking_token:
            raise Exception("Invalid Token")
        if assignmentObj.status == "Submitted":
            raise Exception("Question paper is submitted already!")

        question_paper_file = request.FILES.get("question_paper_file")
        department = assignmentObj.course.department.code

        if question_paper_file:
            # Generate a hash of the file name using SHA-256
            file_hash = hashlib.sha256(
                question_paper_file.name.encode()).hexdigest()
            file_extension = os.path.splitext(question_paper_file.name)[1]

            # Define the directory to save the uploaded file
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'question_papers', str(
                exam_id), str(department), str(course_code))

            # Create the directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)

            # Define the path to save the uploaded file
            hashed_file_name = f"{file_hash}{file_extension}"
            file_path = os.path.join(upload_dir, hashed_file_name)

            # Open the file and write the uploaded content to it
            with open(file_path, 'wb') as destination:
                for chunk in question_paper_file.chunks():
                    destination.write(chunk)

            assignmentObj.qp_doc_url = f"{settings.ROOT_URL}/media/question_papers/{exam_id}/{department}/{course_code}/{hashed_file_name}"
            assignmentObj.submission_date = datetime.now()
            assignmentObj.status = "Submitted"
            assignmentObj.save()

            return Response({"message": "Question paper uploaded successfully"})
        else:
            # If no file is uploaded
            raise Exception("No question paper uploaded")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
def add_comment(request):
    try:
        logger.debug(request.data)
        tracking_token = request.data["tracking_token"]
        exam_id = request.data["exam_id"]
        course_code = request.data["course_code"]
        comment = request.data["comment"]
        email = request.data["email"]

        assignmentObj = Assignment.objects.get(
            exam__eid=exam_id, course__code=course_code)
        if assignmentObj.tracking_token != tracking_token:
            raise Exception("Invalid Token")

        new_entry = {
            "email": email,
            "comment": comment,
            "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        assignmentObj.comments.append(new_entry)
        assignmentObj.save()

        return Response({"message": "Comment added successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
