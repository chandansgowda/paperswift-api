from django.contrib import admin
from .models import Course, Assignment

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'scheme')
    search_fields = ('name', 'code')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'paper_setter', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('course__name', 'paper_setter__name')
    date_hierarchy = 'date'
    ordering = ('-date',)
    fieldsets = (
        ('Assignment Details', {
            'fields': ('course', 'paper_setter', 'date', 'status'),
        }),
    )

admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
