from django.db import connection
from django.conf import settings


def department_list_query():
    script1 = ''' 
    SELECT 
        d.department_id, d.department_name, d.description
    FROM master_department d
    WHERE d.department_name <> 'ALL'
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(script1)
        task = cursor.fetchall()  
    return task


def designation_list_query():
    script1 = ''' 
    SELECT 
        ds.designation_id, ds.designation_name, ds.description, 
        d.department_name
    FROM master_designation ds
    LEFT JOIN master_department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(script1)
        task = cursor.fetchall()  
    return task



def location_list_query():
    script1 = ''' 
    SELECT 
        l.location_id, l.location_name, l.description
    FROM master_location l
    WHERE l.location_name <> 'ALL'
    '''
    with connection.cursor() as cursor:
        cursor.execute(script1)
        task = cursor.fetchall()  
    return task

