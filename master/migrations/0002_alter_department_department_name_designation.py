# Generated by Django 4.2.14 on 2024-08-03 13:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('designation_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('designation_name', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='master.user')),
                ('department', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designation_dep', to='master.department')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_updated_by', to='master.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
