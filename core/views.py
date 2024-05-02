from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import os
import subprocess


# Create your views here.

@api_view(["POST"])
def update_server_webhook(request):
    if "ref" in request.data and request.data["ref"] == "refs/heads/main":
        subprocess.run(['git', 'restore', '.'])
        subprocess.run(['git', 'pull'])
        return Response("Deployement Successful", 200)
    return Response("Forbidden", 403)


@staff_member_required
def serve_protected_file(request, file_path):
    full_path = os.path.join('./media/question_papers', file_path)

    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            response = HttpResponse(
                f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(full_path)
            return response
    else:
        return HttpResponse("File not found", status=404)
