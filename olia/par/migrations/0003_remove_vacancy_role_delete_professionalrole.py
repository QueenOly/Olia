# Generated by Django 5.0.6 on 2024-07-06 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0002_remove_vacancy_role_vacancy_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='role',
        ),
        migrations.DeleteModel(
            name='ProfessionalRole',
        ),
    ]
