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




def employee_list_query(start_index, page_length, search_value, draw, start_date=None, end_date=None):
    # Set default values if start_index or page_length are None
    start_index = start_index if start_index is not None else 0
    page_length = page_length if page_length is not None else 10
    
    # Convert to integers and handle possible conversion errors
    try:
        start_index = int(start_index)
        page_length = int(page_length)
    except ValueError:
        start_index = 0
        page_length = 10
    
    # Base SQL script
    script1 = ''' 
    SELECT 
        e.employee_id, e.join_date, e.emp_no, e.name, e.phone, e.address, 
        e.emp_start_date, e.emp_end_date, e.photo, e.status,
        d.department_name, ds.designation_name, l.location_name
    FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM master_employee e
    LEFT JOIN master_department d ON e.department_id = d.department_id
    LEFT JOIN master_designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN master_location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    # Add search filter
    if search_value:
        search_script = " AND e.name LIKE %s"
        script1 += search_script
        script2 += search_script
    
    # Add date filter
    if start_date and end_date:
        date_filter = " AND e.emp_start_date >= %s AND e.emp_end_date <= %s"
        script1 += date_filter
        script2 += date_filter
    
    # Order and limit results
    script1 += " ORDER BY e.name ASC LIMIT %s OFFSET %s;"
    
    # Prepare parameters for the queries
    params = []
    if search_value:
        params.append('%' + search_value + '%')
    if start_date and end_date:
        params.append(start_date)
        params.append(end_date)
    params.extend([page_length, start_index])
    
    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(script1, params)
        employees = cursor.fetchall()

        # Adjust parameters for the count query
        count_params = []
        if search_value:
            count_params.append('%' + search_value + '%')
        if start_date and end_date:
            count_params.append(start_date)
            count_params.append(end_date)

        cursor.execute(script2, count_params)
        total_records = cursor.fetchone()[0]

    # Process results
    employee_list = []
    sl_no = start_index + 1

    for row in employees:
        employee = {
            'sl_no': sl_no,
            'employee_id': row[0],
            'join_date': row[1],
            'emp_no': row[2],
            'name': row[3],
            'phone': row[4],
            'address': row[5],
            'emp_start_date': row[6],
            'emp_end_date': row[7],
            'photo': settings.MEDIA_URL + row[8] if row[8] else '',  # Handle case where photo might be None
            'status': row[9],
            'department_name': row[10],
            'designation_name': row[11],
            'location_name': row[12],
        }
        employee_list.append(employee)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": employee_list
    }
    return response
def user_list_query(start_index, page_length, search_value, draw):
    # Ensure start_index and page_length are not None
    if start_index is None:
        start_index = 0  # Default to 0 if not provided
    if page_length is None:
        page_length = 10  # Default to 10 if not provided

    script1 = '''
    SELECT 
        u.id, u.username, u.email
    FROM master_user u
    WHERE u.username <> 'ALL'
    '''
    
    script2 = '''
    SELECT COUNT(*) 
    FROM master_user u
    WHERE u.username <> 'ALL'
    '''

    if search_value:
        search_script = " AND u.username LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY u.username ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        users = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    user_list = []
    if isinstance(start_index, int):
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in users:
        user = {
            'sl_no': sl_no,
            'id': row[0],
            'username': row[1],
            'email': row[2],  # Assuming the email column is also fetched
        }
        user_list.append(user)
       
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": user_list
    }
    return response
