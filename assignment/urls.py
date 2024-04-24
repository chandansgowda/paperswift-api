"""
URL configuration for paperswift_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'assignment'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('bulk_assign_paper_setters', bulk_assign_paper_setters),
    path('set_paper_setter_decision', set_paper_setter_decision),
    path('upload_question_paper', upload_question_paper),
    path('comment', add_comment),
    path('accept_question_paper', accept_question_paper),
    path('submitted_papers/<exam_id>', submitted_papers)
]
