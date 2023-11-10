from django.contrib import admin
from .models import PaperSetter, Course, Assignment

class PaperSetterAdmin(admin.ModelAdmin):
    list_display = ('psid', 'name', 'email')
    search_fields = ('name', 'email')

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

admin.site.register(PaperSetter, PaperSetterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
