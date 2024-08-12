from django import forms
from .models import Department
from django.forms import modelformset_factory
from master.models import *

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name','description']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'true'})  # Updated to Textarea
           }

class Designation_Form(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['department','designation_name', 'description']
        widgets = {
            'department':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'true'})  # Updated to Textarea
            
           }
    def __init__(self, *args, **kwargs):
        super(Designation_Form, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name','description']
        widgets = {
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': 'true'})  # Updated to Textarea
           
          
        }

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d' 
class EmpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [ 'join_date', 'emp_no', 'name', 'phone', 'address', 'emp_start_date', 'emp_end_date', 'photo', 'status', 'department', 'designation', 'location']
        widgets = {
            'join_date': DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'emp_no': forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emp_start_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'emp_end_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control','id': 'department-dropdown'}),
            'designation': forms.Select(attrs={'class': 'form-control','id': 'designation-dropdown'}),
            'location': forms.Select(attrs={'class': 'form-control',})
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name','description']
        widgets = {
            'skill_name': forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
            'description':forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
        }

SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=0, can_delete=True)

class UseraddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}),
            'role': forms.Select(attrs={'class': 'form-control'}, choices=User.ROLE_TYPES),
        }
class UsereditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',  'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
           
            'role': forms.Select(attrs={'class': 'form-control'}, choices=User.ROLE_TYPES),
        }


