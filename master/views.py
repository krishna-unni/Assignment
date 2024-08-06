from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
import os
from master.forms import DepartmentForm, Designation_Form, LocationForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from master.dbquery import department_list_query, designation_list_query, location_list_query
import json
from master.models import Department,User,Designation
import openpyxl
from django.http import HttpResponse
import pandas as pd
from io import BytesIO


def indexpage(request):
    return render(request, 'index.html')

def ad_login(request):
    template_name = 'login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username,'username')
        password = request.POST.get('password')
        print(password,'password')

        # user_exist = User.objects.filter(username=username).exists()
        # print(user_exist,'user_exist')
        # if user_exist:
        user = authenticate(request, username=username, password=password)
        print('user',user)
        if user is not None:
            if user.role == 'ADMIN' :
                login(request, user)
        
                return redirect('indexpage')
            elif user.role == 'VIEWER':
                login(request, user)
                return redirect('indexpage')
            else:
                context = {'msg': 'Invalid Username or Password!'}
                return render(request, template_name, context)
        else:
            context = {'msg': 'Password is incorrect!'}
            return render(request, template_name, context)
        # else:
        #     context = {'msg': 'User Does Not exist'}
        #     return render(request, template_name, context)  
    return render(request, template_name)


def ad_logout(request):
    logout(request)
    return redirect(ad_login)

# def department_list(request):
#     print("ajjjjjjjjjjjh")
#     if request.method == "GET":
#         template_name = 'master/department_list.html'
#         dep = department_list_query()
#         print(dep,'dep')
#         departments = [{'department_id': item[0], 'department_name': item[1], 'description': item[2]} for item in dep]
#         context = {'departments':departments}
#         return render(request, template_name, context )
    
# @csrf_exempt
def department_list(request):
    if request.method == "GET":
        template_name = 'master/department_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        dep = department_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(dep)
    

def department_add(request):
    form = DepartmentForm()
    template_name = 'master/add_department.html'
    context = {'form': form}
    
    if request.method == 'POST':
        print(request.user.id,"Form submitted")
        form = DepartmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            # data.created_by =User.objects.get(id=request.user.id)
            data.save()
           
            messages.success(request, 'Department added Successfully.', 'alert-success')
            return redirect('department_list')
            
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else :
        print("Rendering form")
        return render(request, template_name, context)
    
    
# @login_required(login_url='ad_login')    
def department_edit(request, pk):
    template_name = 'master/department_edit.html'
    try:
        uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'Department not found.', 'alert-danger')
        return redirect('department_list')
    try:
        dep_obj = Department.objects.get(department_id=pk)
    except Department.DoesNotExist:
        messages.error(request, 'Department not found.', 'alert-danger')
        return redirect('department_list')
    form = DepartmentForm(instance=dep_obj)
    context = {'form': form, 'dep_obj': dep_obj}
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=dep_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Department Successfully Updated.', 'alert-success')
            return redirect('department_list')
        else:
            print(form.errors)
            messages.error(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    
# @login_required(login_url='ad_login')
def department_detail(request,pk):
    try:
       
        uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'Invalid department ID.', 'alert-danger')
        return redirect('department_list')

    try:
        departments = Department.objects.get(department_id=pk)
    except departments.DoesNotExist:
        messages.error(request, 'Department not found.', 'alert-danger')
        return redirect('department_list')
    context = {
        'departments': departments
    }
    
    return render(request, 'master/department_detail.html', context)

# @login_required(login_url='ad_login')
def department_delete(request, pk):
    department = Department.objects.get(department_id=pk)
    
    department.delete()
    messages.success(request, 'Department Deleted Successfully', 'alert-success')
    return redirect('department_list')
def handle_uploaded_file(file):
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        print(f"Row data: {row}")  # Log row data for debugging
        if row[0] is not None:  # Ensure department_name is not None
            data.append(row)

    return data

def bulk_upload_depa(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            # Handle missing file error
            return redirect('department_list')  # Or render an error template

        data = handle_uploaded_file(request.FILES['file'])
        
        for row in data:
            department_name = row[0]
            description = row[1] if len(row) > 1 else ''
            
            print(f"Processing department_name: {department_name}, description: {description}")  # Log data for debugging

            if department_name:
                if not Department.objects.filter(department_name=department_name).exists():
                    Department.objects.create(department_name=department_name, description=description)
        
        return redirect('department_list')
    
def export_departmnt(request): 
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Departments'
    columns = ['Sl.No',  'Department Name', 'Description']
    row_num = 1
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title    
    for index, department in enumerate(Department.objects.all(), start=1):
        row_num += 1
        row = [
            index, 
            department.department_name,
            department.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=departments.xlsx'

    workbook.save(response)
    return response


def download_excel(request):
    # Create an empty DataFrame
    df = pd.DataFrame()
    
    # Create a BytesIO object to hold the Excel file
    output = BytesIO()
    
    # Write the DataFrame to the BytesIO object
    df.to_excel(output, index=False, engine='openpyxl')
    
    # Seek to the beginning of the BytesIO object
    output.seek(0)
    
    # Create an HTTP response with the file content
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="empty_excel_sheet.xlsx"'
    
    return response
# def designation_list(request):
#     if request.method == "GET":
#         template_name = 'master/designation_list.html'
#         des = designation_list_query()
#         print(des,'des')
#         designations = [{'designation_id': item[0], 'department': item[1],'designation_name':item[2], 'description': item[3]} for item in des]
#         context = {'designations': designations}
#         return render(request, template_name, context )
def designation_list(request):
    if request.method == "GET":
        template_name = 'master/designation_list.html'
        return render(request, template_name)

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        des = designation_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(des)
    
def designation_add(request):
    form = Designation_Form()
    template_name = 'master/add_designation.html'
    context = {'form': form}
   
    if request.method == 'POST':
        print(request.user.id, "Form submitted")
        form = Designation_Form(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            # try:
            #     data.created_by = User.objects.get(id=request.user.id)
            # except User.DoesNotExist:
            #     messages.error(request, 'User not found.', extra_tags='alert-danger')
            #     return redirect('designation_list')  # Or render an error template

            data.save()
            messages.success(request, 'Designation Successfully Updated.', 'alert-success')
            return redirect('designation_list')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        print("Rendering form")
        return render(request, template_name, context)
    

# @login_required(login_url='adlogin')   
def designation_edit(request, pk):
    template_name = 'master/designation_edit.html'
    try:
        uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'Designation not found.', 'alert-danger')
        return redirect('designation_list')
    try:
        des_obj = Designation.objects.get(designation_id=pk)
    except des_obj.DoesNotExist:
        messages.error(request, 'Designation not found.', 'alert-danger')
        return redirect('designation_list')
    form = Designation_Form(instance=des_obj)
    context = {'form': form, 'des_obj': des_obj}
    if request.method == 'POST':
        form = Designation_Form(request.POST, request.FILES, instance=des_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Designation Successfully Updated.', 'alert-success')
            return redirect('designation_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    
def designation_detail(request,pk):
    try:
       uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'designation not found.', 'alert-danger')
        return redirect('designation_list')

    try:
         designation = get_object_or_404(Designation,designation_id=pk)
    except designation.DoesNotExist:
        messages.error(request, 'designation not found.', 'alert-danger')
        return redirect('designation_list')
    
    department_name = designation.department.department_name
    context = {
        'designation': designation,
        'department_name':department_name
    }
    return render(request, 'master/designation_detail.html', context)

def designation_delete(request, pk):
    designation = Designation.objects.get(designation_id=pk)
    designation.delete()
    messages.success(request, 'Designation Deleted Successfully', 'alert-success')
    return redirect('designation_list')
def bulk_upload_des(request):
    if request.method == 'POST':
       
        data = handle_uploaded_file(request.FILES['file'])
        print(data,"data")
       
        for row in data:
            department_name = row[0]
            designation_name = row[1]
            description = row[2]
            department = Department.objects.filter(department_name=department_name).first()
            if department and not Designation.objects.filter(designation_name=designation_name, department=department).exists():
                Designation.objects.create(department=department, designation_name=designation_name, description=description)

        return redirect('designation_list')
    
def export_designations_to_excel(request): 
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Departments'
    columns = ['Sl.No',  'Department Name', 'Description']
    row_num = 1
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title    
    for index, department in enumerate(Department.objects.all(), start=1):
        row_num += 1
        row = [
            index,  # Sl.No
            department.department_name,
            department.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=departments.xlsx'

    workbook.save(response)
    return response


# def location_list(request):
#     if request.method == "GET":
#         template_name = 'master/location_list.html'
#         location = location_list_query()
#         print(location,'location')
#         locations = [{'location_id': item[0], 'location_name': item[1], 'description': item[2]} for item in location]
#         context = {'location': locations}
#         return render(request, template_name, context )
def location_list(request):
    if request.method == "GET":
        template_name = 'master/location_list.html'
       
        return render(request, template_name, )

    if request.method == "POST":
        start_index = request.POST.get('start')
        page_length = request.POST.get('length')
        search_value = request.POST.get('search[value]')
        draw = request.POST.get('draw')
       
        loc = location_list_query(start_index, page_length, search_value, draw)
       
        return JsonResponse(loc)

def locationn_add(request):
    form = LocationForm()
    template_name = 'master/location_add.html'
    context = {'form': form}
   
    if request.method == 'POST':
        print(request.user.id, "Form submitted")
        form = LocationForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("Form is valid")
            data = form.save()
            # try:
            #     data.created_by = User.objects.get(id=request.user.id)
            # except User.DoesNotExist:
            #     messages.error(request, 'User not found.', extra_tags='alert-danger')
            #     return redirect('location_list')  # Or render an error template

            data.save()
            messages.success(request, 'Location Successfully Updated.', 'alert-success')
            return redirect('location_list')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors to debug
            messages.error(request, 'Data is not valid.', extra_tags='alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        print("Rendering form")
        return render(request, template_name, context)
    
 
def locationn_edit(request, pk):
    template_name = 'master/location_edit.html'
    try:
        uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'Location not found.', 'alert-danger')
        return redirect('location_list')
    try:
        loc_obj = Location.objects.get(location_id=pk)
    except loc_obj.DoesNotExist:
        messages.error(request, 'Location not found.', 'alert-danger')
        return redirect('location_list')
    
    form = LocationForm(instance=loc_obj)
    context = {'form': form, 'loc_obj': loc_obj}
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=loc_obj)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Location Successfully Updated.', 'alert-success')
            return redirect('location_list')
        else:
            print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, template_name, context)
    else:
        return render(request, template_name, context)
    
def locationn_detail(request,pk):
    try:
       
        uuid_obj = uuid.UUID(pk)
    except ValueError:
        messages.error(request, 'Location not found.', 'alert-danger')
        return redirect('location_list')

    try:
         location = get_object_or_404(Location,location_id=pk)
    except location.DoesNotExist:
        messages.error(request, 'Location not found.', 'alert-danger')
        return redirect('location_list')
    context = {
        'location': location
    }
    
    return render(request, 'master/location_detail.html', context)


    

def locationn_delete(request, pk):
    location = Location.objects.get(location_id=pk)
    
    location.delete()
    messages.success(request, 'Location Deleted Successfully', 'alert-success')
    return redirect('location_list')

def bulk_upload_location(request):
    if request.method == 'POST':
        data = handle_uploaded_file(request.FILES['file'])      
        for row in data:            
            if not Location.objects.filter(location_name=row[0]).exists():
                Location.objects.create(location_name=row[0],description=row[1])
        return redirect('location_list')
    
def export_location(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Locations'

    columns = ['Sl.No', 'Location Name', 'Description']
    row_num = 1

   
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

   
    for index, location in enumerate(Location.objects.all(), start=1):
        row_num += 1
        row = [
            index,  
            location.location_name,
            location.description,
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=locations.xlsx'

    workbook.save(response)
    return response
