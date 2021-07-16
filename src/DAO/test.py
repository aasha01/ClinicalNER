import src.DAO.ConnectUMLS as connumls
import mysql.connector

# print(connumls.get_literacy('Abdominal Pain'))

try:
    # conn = mysql.connector.connect(user='aasha', password='24H=1day', host='localhost', database='umls')
    # # Get descriptions
    # sql_select_Query = "select * from mrconso where STR like 'Abdominal pain';"
    # cursor = conn.cursor()
    # cursor.execute(sql_select_Query)
    result = connumls.get_entity("Abdominal pain")
    # get all records
    print('Type:', type(result))
    print('Result')
    print(result)
except mysql.connector.Error as e:
    print(e.msg)

