from django.db import connection
from django.conf import settings


def department_list_query(start_index, page_length, search_value, draw):
    script1 = '''
    SELECT 
        d.department_id, d.department_name, d.description
    FROM master_department d
    WHERE d.department_name <> 'ALL' AND d.description <> 'ALL'
    '''
    
    script2 = '''
    SELECT COUNT(*) FROM master_department d
    WHERE d.department_name <> 'ALL' AND d.description <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND (d.department_name LIKE %s OR d.description LIKE %s)"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY d.department_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', '%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        departments = cursor.fetchall()
        
        cursor.execute(script2, ('%' + search_value + '%', '%' + search_value + '%') if search_value else ())
        total_records = cursor.fetchone()[0]

    department_list = []
    sl_no = int(start_index) + 1 if start_index.isdigit() else 1

    for row in departments:
        department = {
            'sl_no': sl_no,
            'department_id': row[0],
            'department_name': row[1],
            'description': row[2]
        }
        department_list.append(department)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": department_list
    }
    return response



# def department_list_query():
#     script1 = ''' 
#     SELECT 
#         d.department_id, d.department_name, d.description
#     FROM master_department d
#     WHERE d.department_name <> 'ALL'
#     '''
#     # code for list query
#     with connection.cursor() as cursor:
#         cursor.execute(script1)
#         task = cursor.fetchall()  
#     return task


# def designation_list_query():
#     script1 = ''' 
#     SELECT 
#         ds.designation_id, ds.designation_name, ds.description, 
#         d.department_name
#     FROM master_designation ds
#     LEFT JOIN master_department d ON ds.department_id = d.department_id
#     WHERE ds.designation_name <> 'ALL'
#     '''
    
#     with connection.cursor() as cursor:
#         cursor.execute(script1)
#         task = cursor.fetchall()  
#     return task

def designation_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        ds.designation_id, ds.designation_name, ds.description, 
        d.department_name
    FROM master_designation ds
    LEFT JOIN master_department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_designation ds
    LEFT JOIN master_department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND ds.designation_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY ds.designation_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        designations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    designation_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in designations:
        designation = {
            'sl_no':sl_no,
            'designation_id': row[0],
            'designation_name': row[1],
            'description': row[2],
            'department_name': row[3]
        }
        designation_list.append(designation)
        sl_no += 1
    print(designation_list)
    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": designation_list
    }
    return response

# def location_list_query():
#     script1 = ''' 
#     SELECT 
#         l.location_id, l.location_name, l.description
#     FROM master_location l
#     WHERE l.location_name <> 'ALL'
#     '''
#     with connection.cursor() as cursor:
#         cursor.execute(script1)
#         task = cursor.fetchall()  
#     return task
def location_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        l.location_id, l.location_name, l.description
    FROM master_location l
    WHERE l.location_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_location l
    WHERE l.location_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND l.location_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY l.location_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        locations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    location_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in locations:
        location = {
            'sl_no':sl_no,
            'location_id': row[0],
            'location_name': row[1],
            'description': row[2]
        }
        location_list.append(location)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": location_list
    }
    return response


