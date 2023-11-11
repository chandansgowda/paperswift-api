from django.contrib import admin
from .models import Course, Assignment, Examination


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'scheme')
    search_fields = ('name', 'code')


class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('eid', 'sem', 'isSupplementary')
    search_fields = ('sem',)


class AssignmentAdmin(admin.ModelAdmin):

    def papersetter_name(self, obj):
        return obj.paper_setter.first_name + " " + obj.paper_setter.last_name

    list_display = ('course', 'papersetter_name', 'date', 'status')
    list_filter = ('exam', 'status', 'date')
    search_fields = ('course__name', 'paper_setter__name')
    date_hierarchy = 'date'
    ordering = ('-date',)
    fieldsets = (
        ('Assignment Details', {
            'fields': ('exam', 'course', 'paper_setter', 'date', 'status'),
        }),
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(Assignment, AssignmentAdmin)
