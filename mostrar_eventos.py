# Mostrar eventos almacenados en la tabla
def most_eventos():
    mostrar_eventos = "SELECT id, titulo, fecha, hora, duracion, descripcion, importancia, fecha_Recordatorio, etiquetas FROM eventos"
    with conn.cursor() as cursor:
        cursor.execute(mostrar_eventos)
        eventos = cursor.fetchall()

    for evento in eventos:
        print(f"ID: {evento[0]}, titulo: {evento[1]}, Fecha: {evento[2]}, hora: {evento[3]}, duracion: {evento[4]}, descripcion: {evento[5]}, importancia: {evento[6]}, fecha_Recordatorio: {evento[7]}")
