from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(["POST"])
def update_server_webhook(request):
    return Response(request.data, 200)