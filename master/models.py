import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,AbstractUser, Group, Permission


class User(AbstractUser):
    ROLE_TYPES = (
        ('ADMIN', 'ADMIN'),
        ('VIEWER', 'VIEWER'),
    )

    role = models.CharField(max_length=10, choices=ROLE_TYPES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups' 
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions' 
    )

    def __str__(self):
        return self.username
    
class Base(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_created_by',null = True)
    created_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_updated_by',blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Department(Base):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.department_name) 
    
class Designation(Base):
    designation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey('master.Department', max_length=250, null=True, blank=True, related_name='designation_dep',on_delete=models.SET_NULL)
    designation_name = models.CharField(max_length=50, null=True, blank=False)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.designation_name) 

    
class Location(Base):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    location_name = models.CharField(max_length=50, null=True, blank=False)    
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.location_name) 
    

class Employee(Base):
    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    join_date = models.DateField(null=True, blank=True)
    emp_no = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=255,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    emp_start_date = models.DateField(null=True, blank=True)
    emp_end_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    status = models.CharField(max_length=50)
    department = models.ForeignKey('master.Department', max_length=250, null=True, blank=True, related_name='emp_dep',
                             on_delete=models.SET_NULL)
    designation = models.ForeignKey('master.Designation', max_length=250, null=True, blank=True, related_name='emp_des',
                             on_delete=models.SET_NULL)
    location = models.ForeignKey('master.Location', max_length=250, null=True, blank=True, related_name='emp_loc',
                             on_delete=models.SET_NULL)

    def __str__(self):
        return self.name   

class Skill(models.Model):
    skill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('Employee', related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.skill_name