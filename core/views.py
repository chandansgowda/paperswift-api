from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess
import json


# Create your views here.

@api_view(["POST"])
def update_server_webhook(request):
    if "ref" in request.data and request.data["ref"]=="refs/heads/main":
        subprocess.run(['git','restore','.'])
        subprocess.run(['git','pull'])
        return Response("Deployement Successful", 200)
    return Response("Forbidden", 403)
