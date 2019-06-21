"""

Подключение к SQL Server (локально) и выполнение select

Connect to SQL Server (local) and execute select

"""


import pypyodbc


driver = 'Driver={SQL Server}'
server = 'Server=computer_name\SQLEXPRESS' #localhost  
database = 'Database=Northwind'
conn_str = ';'.join([driver, server, database])
# port
# user
# psw


try:

    connection = pypyodbc.connect(conn_str)
    print('connection - done', '\n')
    cursor = connection.cursor()
    mySQLQuery = """
        SELECT CompanyName, ContactName, Country
        FROM  dbo.Customers
        WHERE country = 'UK'
    """
    cursor.execute(mySQLQuery)
    results = cursor.fetchall()
    
    for row in results:
        comp_name = row[0]
        cont_name = row[1]
        country = row[2]
        print(' | '.join([comp_name, cont_name, country]), '\n')

except Exception as ex:
    print(ex)

finally:
    connection.close()
    print('\n', 'connection - close') 