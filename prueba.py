from tkinter import *
import tkinter as tk
import datetime
import csv
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import filedialog
from calendario_stage4 import *
from Conexion import *

class Evento:
    def __init__(self, titulo, fecha, hora, duracion=1, descripcion="", importancia="normal", recordatorio=None, etiquetas=None):
        self.titulo = titulo
        self.fecha = fecha
        self.hora = hora
        self.duracion = duracion
        self.descripcion = descripcion
        self.importancia = importancia
        self.recordatorio = recordatorio
        self.etiquetas = etiquetas if etiquetas is not None else []

    @property
    def recordatorio(self):
        return self._recordatorio

    @recordatorio.setter
    def recordatorio(self, value):
        if value is None:
            self._recordatorio = None
        else:
            self._recordatorio = datetime.strptime(value, "%d/%m/%Y %H:%M")


#.............Pantalla....................

class CalendarApp:
    def __init__(self, master):
        self.master = master
        master.title("Calendario de eventos")
        master.config(bg="pink")
        master.config(relief="groove")
        master.config(bd="35")
        master.config(cursor="pencil")
        master.iconbitmap("calendario.ico")
        self.titulo = tk.StringVar()
        self.fecha = tk.StringVar()
        self.hora = tk.StringVar()
        self.duracion = tk.StringVar()
        self.descripcion = tk.StringVar()
        self.importancia = tk.StringVar()
        self.recordatorio = tk.StringVar()
        self.etiquetas = tk.StringVar()
        self.ordenamiento_actual = "cronologico"

        # Creación de widgets
        self.frame_calendario = tk.Frame(master)
        self.frame_evento = tk.Frame(master)
        self.frame_busqueda = tk.Frame(master)

        # Configuración de widgets
        # Configuración de widgets
        self.frame_calendario.pack(side="left", padx=20, pady=20)
        self.frame_evento.pack(side="left", padx=20, pady=20)
        self.frame_busqueda.pack(side="left", padx=20, pady=20)

        self.etiqueta_titulo = tk.Label(self.frame_evento, text="Título:")
        self.etiqueta_titulo.pack(side="top", anchor="w")
        self.entrada_titulo = tk.Entry(self.frame_evento, textvariable=self.titulo)
        self.entrada_titulo.pack(side="top", anchor="w")

        self.etiqueta_fecha = tk.Label(self.frame_evento, text="Fecha:")
        self.etiqueta_fecha.pack(side="top", anchor="w")
        self.entrada_fecha = tk.Entry(self.frame_evento, textvariable=self.fecha)
        self.entrada_fecha.pack(side="top", anchor="w")

        self.etiqueta_hora = tk.Label(self.frame_evento, text="Hora:")
        self.etiqueta_hora.pack(side="top", anchor="w")
        self.entrada_hora = tk.Entry(self.frame_evento, textvariable=self.hora)
        self.entrada_hora.pack(side="top", anchor="w")

        self.etiqueta_duracion = tk.Label(self.frame_evento, text="Duración (horas):")
        self.etiqueta_duracion.pack(side="top", anchor="w")
        self.entrada_duracion = tk.Entry(self.frame_evento, textvariable=self.duracion)
        self.entrada_duracion.pack(side="top", anchor="w")

        self.etiqueta_descripcion = tk.Label(self.frame_evento, text="Descripción:")
        self.etiqueta_descripcion.pack(side="top", anchor="w")
        self.entrada_descripcion = tk.Entry(self.frame_evento, textvariable=self.descripcion)
        self.entrada_descripcion.pack(side="top", anchor="w")


        self.etiqueta_importancia = tk.Label(self.frame_evento, text="Importancia:")
        self.etiqueta_importancia.pack(side="top", anchor="w")
        self.lista_importancia = tk.OptionMenu(self.frame_evento, self.importancia, "Normal", "Importante")
        self.lista_importancia.pack(side="top", anchor="w")



        self.etiqueta_recordatorio = tk.Label(self.frame_evento, text="Fecha recordatorio:")
        self.etiqueta_recordatorio.pack(side="top", anchor="w")
        self.entrada_recordatorio = tk.Entry(self.frame_evento, textvariable=self.recordatorio)
        self.entrada_recordatorio.pack(side="top", anchor="w")


        self.etiqueta_etiquetas = tk.Label(self.frame_evento, text="Etiquetas:")
        self.etiqueta_etiquetas.pack(side="top", anchor="w")
        self.entrada_etiquetas = tk.Entry(self.frame_evento, textvariable= self.etiquetas)
        self.entrada_etiquetas.pack(side="top", anchor="w")

        self.boton_crear_evento = tk.Button(self.frame_evento, text="Crear evento", command= lambda: self.crear_evento(self.titulo.get(), self.fecha.get(), self.hora.get(), self.duracion.get(), self.descripcion.get(), self.importancia.get(), self.recordatorio.get(), self.etiquetas.get()))
        self.boton_crear_evento.pack(side="top", anchor="w")

         # Crear el Radiobutton para seleccionar el tipo de búsqueda
        self.opcion_busqueda = tk.IntVar()
        self.opcion_busqueda.set(1)
        self.radio_titulo = tk.Radiobutton(self.frame_busqueda, text="Buscar por título", variable=self.opcion_busqueda, value=1)
        self.radio_titulo.pack()
        self.radio_etiqueta = tk.Radiobutton(self.frame_busqueda, text="Buscar por etiqueta", variable=self.opcion_busqueda, value=2)
        self.radio_etiqueta.pack()

        self.etiqueta_busqueda = tk.Label(self.frame_busqueda, text="Buscar eventos:", textvariable=self.busqueda)
        self.etiqueta_busqueda.pack(side="left", anchor="w")
        self.entrada_busqueda = tk.Entry(self.frame_busqueda)
        self.entrada_busqueda.pack(side="left", anchor="w")
        self.boton_buscar = tk.Button(self.frame_busqueda, text="Buscar", command= self.buscar_evento)
        self.boton_buscar.pack(side="left", anchor="w")

        self.boton_eliminar = tk.Button(self.frame_busqueda, text="Eliminar", command= self.eliminar_evento)
        self.boton_eliminar.pack(side="left", padx=5, pady=5)

        btn_mostrar = tk.Button(self.frame_evento, text="Mostrar lista", command=self.mostrar_eventos)
        btn_mostrar.pack()

        self.boton_modificar= tk.Button(self.frame_busqueda, text="Modificar", command= self.modificarevento)
        self.boton_modificar.pack(side="left", padx=5, pady=5)

        self.boton_semanl= tk.Button(self.frame_busqueda, text="Semanal", command= self.semanal)
        self.boton_semanl.pack(side="left", padx=5, pady=5)

        # Ubicación de widgets
        # ...

        # Asociación de eventos
        # ...
    def crear_evento(self, titulo, fecha, hora, duracion, descripcion, importancia, recordatorio, etiquetas):
        print("Llamando a la función crear_evento")
        titulo = self.titulo.get()
        fecha = datetime.strptime(self.fecha.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        hora = datetime.strptime(self.hora.get(), "%H:%M").strftime("%H:%M")
        print(f"Valor de 'titulo': {titulo}")
        print(f"Valor de 'fecha': {fecha}")
        duracion = int(self.duracion.get())
        descripcion = self.descripcion.get()
        importancia = self.importancia.get()
        recordatorio = self.recordatorio.get()
        etiquetas = self.etiquetas.get()

        conec = conectar()
        cursor = conec.cursor()
        try:
            # Insertar la fecha en la tabla "fecha"
            consulta = "SELECT COUNT(*) FROM eventos WHERE fecha_idfecha = %s AND hora_idhora = %s"
            cursor.execute(consulta, (fecha, hora))
            resultado = cursor.fetchone()

            # Si ya existe un evento en la misma hora y fecha, mostrar un mensaje de error y no insertar el nuevo evento
            if resultado[0] > 0:
                messagebox.showerror("Error", "Ya existe un evento a la misma hora y fecha.")
            else:
                cursor.execute("INSERT INTO fecha (fecha) VALUES (%s)", (fecha,))
                conec.commit()

                # Obtener el ID de la fecha insertada
                fecha_id = cursor.lastrowid

                # Insertar la hora en la tabla "hora" asociada a la fecha insertada
                cursor.execute("INSERT INTO hora (idhora, fecha_idfecha) VALUES (NULL, %s)", (fecha_id,))
                conec.commit()

                # Obtener el ID de la hora insertada
                hora_id = cursor.lastrowid

                # Insertar el evento en la tabla "eventos"
                cursor.execute("""
                    INSERT INTO eventos (titulo, fecha_idfecha, hora_idhora, duracion, descripcion, importancia, recordatorio, etiquetas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (titulo, fecha_id, hora_id, duracion, descripcion, importancia, recordatorio, etiquetas))
                conec.commit()
            for evento in self.eventos:
                print(f"Título: {evento.titulo}, Fecha: {evento.fecha}, Hora: {evento.hora}")
            cursor.close()
            conec.close()
        except Exception as e:
            print(f"Error al crear el evento: {str(e)}")
        



   
    def guardar(self):
        """
        Método que se ejecuta al presionar el botón "Guardar" en la ventana de
        modificación de un evento. Actualiza los datos del evento y los almacena en
        el calendario.
        """
        # Obtener los datos ingresados por el usuario en la ventana de modificación
        titulo = self.titulo.get()
        fecha = self.fecha.get()
        hora = self.hora.get()
        duracion = self.duracion.get()
        descripcion = self.descripcion.get()
        importancia = self.importancia.get()
        recordatorio = self.recordatorio.get()
        etiquetas = self.etiquetas.get()
        messagebox.showerror(
            "Error",
            f'Ya existe un evento a la hora'
        )

        # Crear el objeto evento con los datos ingresados
        evento_modificado = Evento(
            titulo=titulo,
            fecha=fecha,
            hora=hora,
            duracion=duracion,
            descripcion=descripcion,
            importancia=importancia,
            recordatorio=recordatorio,
            etiquetas=etiquetas
        )
        self.eventos.append(evento_modificado)

    

#..................pantalla2......................



#......................fila1........................................
#conexion
#Conexion.conectar()




root = tk.Tk()

# Pasar la instancia de tkinter.Tk() a la clase CalendarApp
app = CalendarApp(root)

# Llamar al método mainloop() de la instancia de tkinter.Tk()
root.mainloop()