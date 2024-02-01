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

app_name = 'management'

router = DefaultRouter()
router.register(r'exams', ExaminationViewSet, basename='exams')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
    path('teachers/<int:year>', get_teachers_by_year),
    path('clone_previous_academic_year_list', clone_teacher_list)
]
