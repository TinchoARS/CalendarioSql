from datetime import datetime, timedelta
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
def eventos_semana_actual():

    eventos_semana = "SELECT id, titulo, fecha, hora, duracion, descripcion, importancia, fecha_Recordatorio, etiquetas FROM eventos WHERE fecha BETWEEN %s AND %s"
    with conn.cursor() as cursor:
        cursor.execute(eventos_semana, (start_of_week, end_of_week))
        eventos = cursor.fetchall()

    for evento in eventos:
        print(f"ID: {evento[0]}, titulo: {evento[1]}")


    conn.close()
eventos_semana_actual()
