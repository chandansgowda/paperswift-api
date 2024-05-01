from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Examination, Assignment, AssignmentStatus


@receiver(post_save, sender=Examination)
def update_assignment_status(sender, instance, created, **kwargs):
    """
    Update Assignment status when Examination is marked as completed.
    """
    if not created and instance.is_exam_completed:
        assignments = Assignment.objects.filter(exam=instance)

        for assignment in assignments:
            if assignment.status != AssignmentStatus.COMPLETED:
                assignment.status = AssignmentStatus.COMPLETED
                assignment.save()