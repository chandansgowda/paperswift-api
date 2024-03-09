from django.contrib import admin
from .models import *


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'hod')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'designation',
                    'qualification', 'is_external')
    list_filter = ('is_external', 'gender', 'designation')
    search_fields = ('name', 'designation', 'qualification')
    ordering = ('id',)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('sid', 'degree', 'year', 'guidelines_doc_url')
    search_fields = ('year', 'degree')
    ordering = ('sid',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'scheme', 'department',
                    'sem', 'syllabus_doc_url')
    list_filter = ('department', 'sem')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('eid', 'degree', 'sem', 'scheme', 'is_supplementary',
                    'paper_submission_deadline', 'is_exam_completed')
    list_filter = ('degree', 'sem', 'is_supplementary', 'is_exam_completed')
    search_fields = ('sem', 'degree')
    ordering = ('eid',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    def papersetter_name(self, obj):
        return obj.paper_setter.first_name + " " + obj.paper_setter.last_name

    list_display = ('exam', 'course', 'paper_setter', 'assigned_date',
                    'status', 'submission_date', 'qp_doc_url', 'is_paid', 'payment_ref_id')
    list_filter = ('exam', 'status', 'is_paid')
    search_fields = ('course__name', 'paper_setter__name')
    date_hierarchy = 'assigned_date'
    ordering = ('-assigned_date',)
    fieldsets = (
        ('Assignment Details', {
            'fields': ('exam', 'course', 'paper_setter', 'assigned_date', 'status', 'submission_date', 'tracking_token', 'qp_doc_url', 'is_paid', 'payment_ref_id', 'comments'),
        }),
    )


@admin.register(TeacherYear)
class TeacherYearAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'year')
    list_filter = ('year',)
    search_fields = ('teacher__name', 'year')


@admin.register(TeacherDepartment)
class TeacherDepartmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'department')
    list_filter = ('department', 'teacher')
    search_fields = ('teacher__name', 'department__name')
