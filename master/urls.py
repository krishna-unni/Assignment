from django.urls import path
from . import views

urlpatterns = [
    path('index',views.indexpage,name="indexpage"),   
    path('', views.ad_login, name='ad_login'),
    path('ad_logout', views.ad_logout, name='ad_logout'),


    # -----------------------------department------------------------------------------
    path('department_list', views.department_list, name='department_list'),
    path('department_add', views.department_add, name='department_add'),
    path('department_edit/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_detail/<str:pk>/', views.department_detail, name='department_detail'),
    path('department_delete/<str:pk>/', views.department_delete, name='department_delete'),
    path('bulk_upload_depa/', views.bulk_upload_depa, name='bulk_upload_depa'),
    path('export_departmnt', views.export_departmnt, name='export_departmnt'),
    path('download_excel',  views.download_excel, name='download_excel'),


    # ----------------------designation--------------------------------------------------
    path('designation_list', views.designation_list, name='designation_list'),
    path('designation_add', views.designation_add, name='designation_add'),
    path('designation_edit/<str:pk>/', views.designation_edit, name='designation_edit'),
    path('designation_detail/<str:pk>/', views.designation_detail, name='designation_detail'),
    path('designation_delete/<str:pk>/', views.designation_delete, name='designation_delete'),
    path('bulk_upload_des/', views.bulk_upload_des, name='bulk_upload_des'),
    path('export_designations', views.export_designations_to_excel, name='export_designations'),


    # ------------------------------------------------location---------------------------
    path('location_list', views.location_list, name='location_list'),
    path('locationn_add', views.locationn_add, name='locationn_add'),
    path('locationn_edit/<str:pk>/', views.locationn_edit, name='locationn_edit'),
    path('locationn_detail/<str:pk>/', views.locationn_detail, name='locationn_detail'),
    path('locationn_delete/<str:pk>/', views.locationn_delete, name='locationn_delete'),
    path('bulk_upload_location/', views.bulk_upload_location, name='bulk_upload_location'),
    path('export_location', views.export_location, name='export_location'),


    # ----------------------------employee ----------------------------------------------
    path('employee_list', views.employee_list, name='employee_list'),
    path('employee_add', views.employee_add, name='employee_add'),
    path('designations', views.designations, name='designations'),
    path('employee_edit/<str:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_detail/<str:pk>/', views.employee_detail, name='employee_detail'),
    path('employee_delete/<str:pk>/', views.employee_delete, name='employee_delete'),
    path('bulk_upload_employee/', views.bulk_upload_employee, name='bulk_upload_employee'),
    path('filter_employees/', views.filter_employees, name='filter_employees'),
    path('export_employee/', views.export_employee, name='export_employee'),
    path('download_template/', views.download_template, name='download_template'),
    path('download_selected/', views.download_selected, name='download_selected'),
    path('download_employee/<str:employee_id>/', views.download_employee, name='download_employee'),
    path('mail_pdf/<str:employee_id>/', views.send_email_pdf, name='mail_pdf'),


    # ----------------------------accounts-------------------------------------------------
    path('users/', views.user_list, name='user_list'),
    path('users_add/', views.user_add, name='user_add'),
    path('users_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_detail/<str:pk>/', views.user_detail, name='user_detail'),
    path('users_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('bulk_upload_user/', views.bulk_upload_user, name='bulk_upload_user'),
    path('export_user/', views.export_user, name='export_user'),



    


    








]