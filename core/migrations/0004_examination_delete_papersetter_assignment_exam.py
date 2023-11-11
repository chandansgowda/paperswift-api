# Generated by Django 4.2.6 on 2023-11-11 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_assignment_paper_setter"),
    ]

    operations = [
        migrations.CreateModel(
            name="Examination",
            fields=[
                ("eid", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("sem", models.IntegerField()),
                ("isSupplementary", models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name="PaperSetter",
        ),
        migrations.AddField(
            model_name="assignment",
            name="exam",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.examination",
            ),
        ),
    ]
