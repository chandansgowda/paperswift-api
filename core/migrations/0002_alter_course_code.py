# Generated by Django 4.2.6 on 2023-11-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
