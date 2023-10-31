from django.db import connections

def execute_query(query):
    database_name = 'default'

    with connections[database_name].cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]  # Fetch column names

    data = []
    for row in rows:
        row_data = dict(zip(columns, row))
        data.append(row_data)

    return data
