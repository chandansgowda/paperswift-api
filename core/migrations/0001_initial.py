# Generated by Django 4.2.7 on 2023-12-08 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "code",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("syllabus_doc_url", models.URLField(blank=True, null=True)),
                ("sem", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Examination",
            fields=[
                ("eid", models.AutoField(primary_key=True, serialize=False)),
                ("sem", models.IntegerField()),
                ("is_supplementary", models.BooleanField(default=False)),
                ("paper_submission_deadline", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Scheme",
            fields=[
                ("sid", models.AutoField(primary_key=True, serialize=False)),
                ("year", models.IntegerField()),
                ("guidelines_doc_url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("is_external", models.BooleanField(default=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=1,
                    ),
                ),
                ("dob", models.DateField()),
                ("mobile_no", models.CharField(max_length=15)),
                ("address", models.TextField()),
                ("designation", models.CharField(max_length=255)),
                ("qualification", models.CharField(max_length=255)),
                ("bank_account_no", models.CharField(max_length=20)),
                ("bank_ifsc", models.CharField(max_length=15)),
                ("bank_name", models.CharField(max_length=255)),
                ("pan_no", models.CharField(max_length=15, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SuggestedPaperSetter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isExternal", models.BooleanField(default=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.course"
                    ),
                ),
                (
                    "exam",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.examination",
                    ),
                ),
                (
                    "paper_setter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.teacher"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="examination",
            name="scheme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.scheme"
            ),
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "code",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "hod",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.teacher",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.department"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="scheme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.scheme"
            ),
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assigned_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Request Pending", "Request Pending"),
                            ("In Progress", "In Progress"),
                            ("Update Requested", "Update Requested"),
                            ("Completed", "Completed"),
                        ],
                        default="Request Pending",
                        max_length=20,
                    ),
                ),
                ("submission_date", models.DateTimeField(blank=True, null=True)),
                ("qp_doc_url", models.URLField(blank=True, null=True)),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "payment_ref_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.course"
                    ),
                ),
                (
                    "exam",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.examination",
                    ),
                ),
                (
                    "paper_setter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.teacher"
                    ),
                ),
            ],
        ),
    ]
