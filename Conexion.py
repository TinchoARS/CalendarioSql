import mysql.connector

conexion = mysql.connector.connect(user='root', password='Marman6403', host='localhost', database='calendario', port='3306')

print(conexion)

