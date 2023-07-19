from tkinter import *
import tkinter as tk
import datetime
import csv
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import filedialog
import tkinter.ttk as ttk
import Conexion

class Evento:
    def __init__(self, titulo, fecha, hora, duracion, descripcion="", importancia="normal", etiquetas=None):
        self.titulo = titulo
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
        self.hora = datetime.strptime(hora, "%H:%M:%S").strftime("%H:%M:%S")
        self.duracion = datetime.strptime(duracion, "%H:%M:%S").strftime("%H:%M:%S")
        self.descripcion = descripcion
        self.importancia = importancia
        self.etiquetas = etiquetas

    #@property
    #def recordatorio(self):
    #    return self._recordatorio

    #@recordatorio.setter
    #def recordatorio(self, value):
    #    if value is None:
    #        self._recordatorio = None
    #    else:
    #        self._recordatorio = datetime.strptime(value, "%d/%m/%Y %H:%M")

    def __str__(self):
        return f"Evento: {self.titulo}\nFecha: {self.fecha}\nHora: {self.hora}\nDuración: {self.duracion}\nDescripción: {self.descripcion}\nImportancia: {self.importancia}\nEtiquetas: {self.etiquetas}"#Recordatorio: {self.recordatorio}

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
        self.titulo= StringVar()
        self.fecha= StringVar()
        self.hora= StringVar()
        self.duracion= StringVar()
        self.descripcion= StringVar()
        self.importancia= StringVar(value="Normal")
        self.recordatorio= StringVar()
        self.etiquetas= StringVar()
        self.busqueda= StringVar()

        # Inicialización de variables
        self.eventos = []
        self.evento_actual = None
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



        #self.etiqueta_recordatorio = tk.Label(self.frame_evento, text="Fecha recordatorio:")
        #self.etiqueta_recordatorio.pack(side="top", anchor="w")
        #self.entrada_recordatorio = tk.Entry(self.frame_evento, textvariable=self.recordatorio)
        #self.entrada_recordatorio.pack(side="top", anchor="w")


        self.etiqueta_etiquetas = tk.Label(self.frame_evento, text="Etiquetas:")
        self.etiqueta_etiquetas.pack(side="top", anchor="w")
        self.entrada_etiquetas = tk.Entry(self.frame_evento, textvariable= self.etiquetas)
        self.entrada_etiquetas.pack(side="top", anchor="w")

        self.boton_crear_evento = tk.Button(self.frame_evento, text="Crear evento", command= lambda: self.crear_evento(self.titulo.get(), self.fecha.get(), self.hora.get(), self.duracion.get(), self.descripcion.get(), self.importancia.get(), self.etiquetas.get())) #self.recordatorio.get(), self.etiquetas.get()))
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
    def crear_evento(self, titulo, fecha, hora, duracion, descripcion="", importancia="normal", etiquetas=None):
        nuevo_evento = Evento(
            self.titulo.get(),
            self.fecha.get().strip(),
            self.hora.get(),
            self.duracion.get(),
            self.descripcion.get(),
            self.importancia.get(),
            self.etiquetas.get())
        print(self.duracion.get())
        print(nuevo_evento)
        # Verificar si la hora del evento ya existe en la lista de eventos
        for evento in self.eventos:
            if evento.hora == nuevo_evento.hora:
                messagebox.showerror(
                    "Error",
                    f'Ya existe un evento a la hora'
                )
                break

        else:
            Conexion.nuevo_evento(nuevo_evento)
            self.eventos.append(nuevo_evento)
            messagebox.showinfo(
                "Evento creado",
                f"Nuevo evento:\n {titulo} \ncreado exitosamente!!"
            )
        



    def buscar_evento(self):
        # Obtener el valor de la entrada de búsqueda
        valor_busqueda = self.entrada_busqueda.get()

        # Determinar el tipo de búsqueda a realizar
        if self.opcion_busqueda.get() == 1:
            # Buscar por título
            evento_encontrado = None
            for evento in self.eventos:
                if evento.titulo == valor_busqueda:
                    evento_encontrado = evento
                    break

            if evento_encontrado:
                # Mostrar la información del evento encontrado
                tk.messagebox.showinfo(
                    "Eventos",
                    f"Título: {evento_encontrado.titulo}\n"
                    f"Fecha: {evento_encontrado.fecha}\n"
                    f"Hora: {evento_encontrado.hora}\n")
            else:
                # Mostrar un mensaje de error si no se encontró el evento
                tk.messagebox.showerror("Error", "El evento buscado no existe.")
        elif self.opcion_busqueda.get() == 2:
            # Buscar por etiqueta
            eventos_encontrados = []
            for evento in self.eventos:
                if valor_busqueda in evento.etiquetas:
                    eventos_encontrados.append(evento)

            if eventos_encontrados:
                # Mostrar la información de los eventos encontrados
                texto_eventos = ""
                for evento in eventos_encontrados:
                    texto_eventos += f"Título: {evento.titulo}\n" \
                                     f"Fecha: {evento.fecha}\n" \
                                     f"Hora: {evento.hora}\n\n"
                tk.messagebox.showinfo("Eventos encontrados", texto_eventos)
            else:
                # Mostrar un mensaje de error si no se encontraron eventos
                tk.messagebox.showerror("Error", "No se encontraron eventos con la etiqueta especificada.")

    def eliminar_evento(self):
        del self.eventos

        Conexion.eliminar_evento("cena con scaloni")
        messagebox.showinfo(
            "Evento eliminado",
            f"Evento:\n {self.titulo.get()} \nEliminado exitosamente!!")


    def mostrar_eventos(self):
        ventana_secundaria = tk.Toplevel(self.frame_evento)
        ventana_secundaria.geometry("1400x300")

        # Crear objeto Frame para la tabla
        frame_tabla = tk.Frame(ventana_secundaria)
        frame_tabla.pack(expand=True, fill="both")
        ventana_secundaria.title("Calendario de eventos")
        ventana_secundaria.config(bg="pink")
        ventana_secundaria.config(relief="groove")
        ventana_secundaria.config(bd="35")
        ventana_secundaria.config(cursor="pencil")
        ventana_secundaria.iconbitmap("calendario.ico")

        # Crear tabla
        tabla = ttk.Treeview(frame_tabla, columns=("columna1", "columna2", "columna3", "columna4", "columna5", "columna6", "columna7"))
        tabla.heading("#0", text="Titulo")
        tabla.heading("columna1", text="fecha")
        tabla.heading("columna2", text="hora")
        tabla.heading("columna3", text="duracion")
        tabla.heading("columna4", text="descripcion")
        tabla.heading("columna5", text="importancia")
        tabla.heading("columna6", text="recordatorio")
        tabla.heading("columna7", text="etiquetas")

        for evento in self.eventos:
            tabla.insert("", "end", text=self.titulo.get(), values=(self.fecha.get(), self.hora.get(), self.duracion.get(), self.descripcion.get(), self.importancia.get(), self.recordatorio.get(), self.etiquetas.get()))

        tabla.pack(expand=True, fill="both")

        # Mostrar ventana secundaria
        ventana_secundaria.mainloop()



    def modificarevento(self):
        ventana_secundaria2 = tk.Toplevel(self.frame_evento)
        ventana_secundaria2.title("Calendario de eventos")
        ventana_secundaria2.config(bg="pink")
        ventana_secundaria2.config(relief="groove")
        ventana_secundaria2.config(bd="35")
        ventana_secundaria2.config(cursor="pencil")
        ventana_secundaria2.iconbitmap("calendario.ico")

        # Crear objeto Frame para la tabla
        frame_tabla = tk.Frame(ventana_secundaria2)
        frame_tabla.grid(row=0, column=0, sticky="nsew")

        # Configuración de la ventana
        ventana_secundaria2.title("Modificar evento")

        # Creación del formulario para ingresar los datos del evento
        self.frame = tk.Frame(frame_tabla)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Campo de entrada para el título del evento
        tk.Label(self.frame, text="Título:").grid(row=0, column=0)
        self.titulo = tk.Entry(self.frame)
        self.titulo.grid(row=0, column=1)
        self.titulo.insert(0, self.titulo.get())

        # Campo de entrada para la fecha del evento
        tk.Label(self.frame, text="Fecha (dd/mm/aaaa):").grid(row=1, column=0)
        self.fecha = tk.Entry(self.frame)
        self.fecha.grid(row=1, column=1)
        self.fecha.insert(0, self.fecha.get())

        # Campo de entrada para la hora del evento
        tk.Label(self.frame, text="Hora (hh:mm):").grid(row=2, column=0)
        self.hora = tk.Entry(self.frame)
        self.hora.grid(row=2, column=1)
        self.hora.insert(0, self.hora.get())

        # Campo de entrada para la duración del evento
        tk.Label(self.frame, text="Duración:").grid(row=3, column=0)
        self.duracion = tk.Entry(self.frame)
        self.duracion.grid(row=3, column=1)
        self.duracion.insert(0, self.duracion.get())


        # Campo de entrada para la descripción del evento
        tk.Label(self.frame, text="Descripción:").grid(row=4, column=0)
        self.descripcion = tk.Entry(self.frame)
        self.descripcion.grid(row=4, column=1)
        self.descripcion.insert(0, self.descripcion.get())

        # Campo de entrada para la importancia del evento
        tk.Label(self.frame, text="Importancia:").grid(row=5, column=0)
        self.importancia = tk.StringVar(frame_tabla)
        self.importancia.set(self.importancia.get())
        opciones_importancia = ["Normal", "Importante"]
        self.importancia_menu = tk.OptionMenu(self.frame, self.importancia, *opciones_importancia)
        self.importancia_menu.grid(row=5, column=1)

        # Campo de entrada para la fecha y hora del recordatorio del evento
        tk.Label(self.frame, text="Fecha y hora del recordatorio (dd/mm/aaaa hh:mm):").grid(row=6, column=0)
        self.recordatorio = tk.Entry(self.frame)
        self.recordatorio.grid(row=6, column=1)
        self.recordatorio.insert(0, self.recordatorio.get())

        # Campo de entrada para las etiquetas del evento
        tk.Label(self.frame, text="Etiquetas (separadas por comas):").grid(row=7, column=0)
        self.etiquetas = tk.Entry(self.frame)
        self.etiquetas.grid(row=7, column=1)
        self.etiquetas.insert(0, self.etiquetas.get())


        # Botón para guardar los cambios del


        # Botón para guardar los cambios del evento
        tk.Button(frame_tabla, text="Guardar", command=self.guardar).grid(row=8, column=0, pady=10)


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

    def semanal(self):
        ventana = tk.Tk()
        ventana.title("Calendario Semanal")

        tabla = tk.Frame(ventana)
        tabla.grid(row=0, column=0)



        # Crear las etiquetas de días de la semana
        dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, dia in enumerate(dias_semana):
            etiqueta_dia = tk.Label(tabla, text=dia, padx=5, pady=5, borderwidth=2, relief="groove")
            etiqueta_dia.grid(row=0, column=i+1, sticky="nsew")

        # Crear las etiquetas de hora en la columna 0
        horas = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
        for i, hora in enumerate(horas):
            etiqueta_hora = tk.Label(tabla, text=hora, padx=5, pady=5, borderwidth=2, relief="groove")
            etiqueta_hora.grid(row=i+1, column=0, sticky="nsew")



        for fila, hora in enumerate(horas):
            for columna, dia in enumerate(dias_semana):
                dia_semana = datetime.strptime(self.fecha.get(), '%d/%m/%Y').strftime('%A')
                hora_semanal= datetime.strptime(self.hora.get(), '%H:%M').strftime('%H:%M')
                eventos_del_dia = [evento for evento in self.eventos if dia_semana == dia and hora_semanal== hora]
                for evento in eventos_del_dia:
                    if evento.importancia == "Importante":
                        etiqueta_evento = tk.Label(tabla, text=evento.titulo, padx=5, pady=5, borderwidth=2, relief="groove", background="red")
                        etiqueta_evento.grid(row=fila+1, column=columna+1, sticky="nsew")
                    else:
                        etiqueta_evento = tk.Label(tabla, text=evento.titulo, padx=5, pady=5, borderwidth=2, relief="groove")
                        etiqueta_evento.grid(row=fila+1, column=columna+1, sticky="nsew")
        for i in range(len(dias_semana)+1):
            tabla.columnconfigure(i, weight=1, minsize=100)
        for i in range(len(horas)+1):
            tabla.rowconfigure(i, weight=1, minsize=50)



#..................pantalla2......................



#......................fila1........................................
#conexion
#Conexion.conectar()

Conexion.create_if_not_exists()
#Conexion.conectar()

root = tk.Tk()

# Pasar la instancia de tkinter.Tk() a la clase CalendarApp
app = CalendarApp(root)

# Llamar al método mainloop() de la instancia de tkinter.Tk()
root.mainloop()