from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexpage,name="indexpage"),   
    path('ad_login', views.ad_login, name='ad_login'),
    path('ad_logout', views.ad_login, name='ad_logout'),
    path('department_list', views.department_list, name='department_list'),
    path('department_add', views.department_add, name='department_add'),
    path('department_edit/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_detail/<str:pk>/', views.department_detail, name='department_detail'),
    path('department_delete/<str:pk>/', views.department_delete, name='department_delete'),
    path('bulk_upload_depa/', views.bulk_upload_depa, name='bulk_upload_depa'),
    path('export_departmnt', views.export_departmnt, name='export_departmnt'),


    path('designation_list', views.designation_list, name='designation_list'),
    path('designation_add', views.designation_add, name='designation_add'),
    path('designation_edit/<str:pk>/', views.designation_edit, name='designation_edit'),
    path('designation_detail/<str:pk>/', views.designation_detail, name='designation_detail'),
    path('designation_delete/<str:pk>/', views.designation_delete, name='designation_delete'),
    path('bulk_upload_des/', views.bulk_upload_des, name='bulk_upload_des'),
    path('export_designations', views.export_designations_to_excel, name='export_designations'),


    path('location_list', views.location_list, name='location_list'),
    path('locationn_add', views.locationn_add, name='locationn_add'),
    path('locationn_edit/<str:pk>/', views.locationn_edit, name='locationn_edit'),
    path('locationn_detail/<str:pk>/', views.locationn_detail, name='locationn_detail'),
    path('locationn_delete/<str:pk>/', views.locationn_delete, name='locationn_delete'),
    path('bulk_upload_location/', views.bulk_upload_location, name='bulk_upload_location'),
    path('export_location', views.export_location, name='export_location'),

]