from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess
import json


# Create your views here.

@api_view(["POST"])
def update_server_webhook(request):
    if request.data['hook']['events'][0]=="push":
        subprocess.run(['git','restore','.'])
        subprocess.run(['git','pull'])
        return Response("Deployement Successful", 200)
    return Response("Forbidden", 403)
