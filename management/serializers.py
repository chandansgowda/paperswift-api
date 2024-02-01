from rest_framework import serializers
from core.models import Department, Examination, Course, Teacher

class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'