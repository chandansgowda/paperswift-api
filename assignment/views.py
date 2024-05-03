from collections import defaultdict
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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Assignment, Examination, Course, Teacher, TeacherYear
from drf_spectacular.utils import extend_schema
from paperswift_api import settings
from dotenv import load_dotenv


from utils.generate_token import generate_random_token
from utils.html_content import *
from utils.send_email import send_email

logger = logging.getLogger('logger')
load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL')


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
@permission_classes([IsAdminUser])
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
            assignment_obj.save()
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

        upload_link = f"http://127.0.0.1:8000/assignment/upload-qp?exam_id={exam_id}&course_code={course_code}&course_name={course.name}&sem={exam.sem}&tracking_token={assignment.tracking_token}"

        if assignment.status == "In Progress":
            send_email(assignment.paper_setter.user.email, subject="Question Paper Details", htmlContent=get_qp_details_html(
                syllabus_copy_link=course.syllabus_doc_url, upload_link=upload_link, deadline=exam.paper_submission_deadline, course_code=course.code, course_name=course.name, branch=course.department, semester=exam.sem, name=assignment.paper_setter.name))

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
        assignmentObj.status = "Update Requested"
        assignmentObj.save()

        exam = Examination.objects.get(eid=exam_id)
        course = Course.objects.get(code=course_code)
        upload_link = f"http://127.0.0.1:8000/assignment/upload-qp?exam_id={exam_id}&course_code={course_code}&course_name={course.name}&sem={exam.sem}&tracking_token={assignmentObj.tracking_token}"

        send_email(assignmentObj.paper_setter.user.email, subject=f"Change Requested for {course_code} Question Paper", htmlContent=get_qp_review_html(
                syllabus_copy_link=course.syllabus_doc_url, upload_link=upload_link, deadline=exam.paper_submission_deadline, course_code=course.code, course_name=course.name, branch=course.department, semester=exam.sem, name=assignmentObj.paper_setter.name, comment=comment))

        return Response({"message": "Comment added successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
@permission_classes([IsAdminUser])
def accept_question_paper(request):
    try:
        logger.debug(request.data)
        tracking_token = request.data["tracking_token"]
        exam_id = request.data["exam_id"]
        course_code = request.data["course_code"]

        assignmentObj = Assignment.objects.get(
            exam__eid=exam_id, course__code=course_code)
        if assignmentObj.tracking_token != tracking_token:
            raise Exception("Invalid Token")
        if assignmentObj.status != "Submitted" and assignmentObj.status != "Update Requested":
            raise Exception(
                "Operation Not Allowed. Question paper is not uploaded yet.")

        assignmentObj.status = "Completed"
        assignmentObj.save()

        exam = Examination.objects.get(eid=exam_id)
        course = Course.objects.get(code=course_code)
        send_email(assignmentObj.paper_setter.user.email, subject=f"Your {course_code} Question Paper has been accepted", htmlContent=get_submission_accepted_html(course_code=course.code, course_name=course.name, branch=course.department, semester=exam.sem, name=assignmentObj.paper_setter.name))

        return Response({"message": "Success"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["GET"])
@permission_classes([IsAdminUser])
def submitted_papers(request, exam_id):
    try:
        examObj = Examination.objects.get(eid=exam_id)
        assignmentObjs = Assignment.objects.filter(exam=examObj)
        response = defaultdict(list)
        for assignmentObj in assignmentObjs:
            if assignmentObj.status == "Submitted" or assignmentObj.status == "Update Requested":
                department = assignmentObj.course.department.code
                response[department].append({
                    "assignment_id": assignmentObj.id,
                    "course_id": assignmentObj.course.code,
                    "course_name": assignmentObj.course.name,
                    "paper_setter": Teacher.objects.get(id=assignmentObj.paper_setter.id).name,
                    "assigned_date": assignmentObj.assigned_date,
                    "status": assignmentObj.status,
                    "comment": assignmentObj.comments[-1]["comment"] if assignmentObj.comments else "NA",
                    "submission_date": assignmentObj.submission_date,
                    "qp_doc_url": assignmentObj.qp_doc_url,
                    "tracking_token": assignmentObj.tracking_token
                })

        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_report(request):
    try:
        assignmentObjs = Assignment.objects.all()
        response = defaultdict(int)
        for assignmentObj in assignmentObjs:
            response[assignmentObj.status] += 1
        logger.info(f"Requested report: {response}")
        return JsonResponse(response)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(tags=['Assignment'])
@api_view(["POST"])
@permission_classes([IsAdminUser])
def send_reminder(request):
    try:
        logger.debug(request.data)
        assignment_id = request.data["assignment_id"]
        assignmentObj = Assignment.objects.get(id=assignment_id)
        status = assignmentObj.status

        logger.info(f"Assignment status is: {assignmentObj}")
        if status=="Request Pending":
            link = f"http://127.0.0.1:8000/assignment/set_paper_setter_decision?exam_id={assignmentObj.exam.eid}&course_code={assignmentObj.course.code}&token={assignmentObj.tracking_token}&has_approved="
            html_content = get_invitation_reminder_html(
                semester=assignmentObj.course.sem,
                course_name=assignmentObj.course.name,
                course_code=assignmentObj.course.code,
                branch=assignmentObj.course.department.name,
                deadline=assignmentObj.exam.paper_submission_deadline,
                link=link,
                name=assignmentObj.paper_setter.name
            )
            send_email(email=assignmentObj.paper_setter.user.email, subject="PaperSwift Reminder: Please Respond ASAP", htmlContent=html_content)

        elif status=="In Progress":
            upload_link = f"http://127.0.0.1:8000/assignment/upload-qp?exam_id={assignmentObj.exam.eid}&course_code={assignmentObj.course.code}&course_name={assignmentObj.course.name}&sem={assignmentObj.exam.sem}&tracking_token={assignmentObj.tracking_token}"
            html_content = get_submission_reminder_html(
                semester=assignmentObj.course.sem,
                course_name=assignmentObj.course.name,
                course_code=assignmentObj.course.code,
                branch=assignmentObj.course.department.name,
                deadline=assignmentObj.exam.paper_submission_deadline,
                name=assignmentObj.paper_setter.name,
                syllabus_copy_link=assignmentObj.course.syllabus_doc_url,
                upload_link=upload_link
            )
            send_email(email=assignmentObj.paper_setter.user.email, subject="PaperSwift Reminder: Submit Question Paper", htmlContent=html_content)

        elif status=="Update Requested":
            upload_link = f"http://127.0.0.1:8000/assignment/upload-qp?exam_id={assignmentObj.exam.eid}&course_code={assignmentObj.course.code}&course_name={assignmentObj.course.name}&sem={assignmentObj.exam.sem}&tracking_token={assignmentObj.tracking_token}"
            html_content = get_review_reminder_html(
                semester=assignmentObj.course.sem,
                course_name=assignmentObj.course.name,
                course_code=assignmentObj.course.code,
                branch=assignmentObj.course.department.name,
                deadline=assignmentObj.exam.paper_submission_deadline,
                name=assignmentObj.paper_setter.name,
                syllabus_copy_link=assignmentObj.course.syllabus_doc_url,
                upload_link=upload_link,
                comment=assignmentObj.comments[-1]["comment"]
            )
            send_email(email=assignmentObj.paper_setter.user.email, subject="PaperSwift Reminder: Submit Question Paper", htmlContent=html_content)

        else:
            raise Exception(f"Reminder can't be sent for status:{assignmentObj.status}")

        return JsonResponse({"message": "Reminder sent successfully"})
    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def upload_qp_form(request):
    return render(request, 'upload_qp_form.html')
