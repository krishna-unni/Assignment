# Generated by Django 4.2.14 on 2024-08-16 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_employee_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='employee',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
