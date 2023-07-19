import mysql.connector

conexion = mysql.connector.connect(user='root', password='martin', host='localhost', database='calendario', port='3306')

print(conexion)

