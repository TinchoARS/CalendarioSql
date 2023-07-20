from tkinter import *
import tkinter as tk
import datetime
import tkinter.messagebox as messagebox
from datetime import datetime
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
        self.root = root
        self.eventos = []  # Lista para almacenar los eventos cargados desde la base de datos
        self.evento_actual = None
        self.ordenamiento_actual = "cronologico"

        # Creación de widgets
        self.frame_calendario = tk.Frame(master)
        self.frame_evento = tk.Frame(master)
        self.frame_busqueda = tk.Frame(master)

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
    # Obtener el valor de búsqueda y el tipo de búsqueda seleccionado
        valor_busqueda = self.entrada_busqueda.get()
        opcion_busqueda = self.opcion_busqueda.get()

    # Obtener todos los eventos de la base de datos
        eventos_registros = Conexion.obtener_eventos()

        if opcion_busqueda == 1:
        # Buscar por título
            eventos_encontrados = [evento for evento in eventos_registros if evento[0] == valor_busqueda]
        else:
        # Buscar por etiqueta
            eventos_encontrados = [evento for evento in eventos_registros if valor_busqueda in evento[6]]

        if eventos_encontrados:
           # Mostrar la información de los eventos encontrados
            texto_eventos = ""
            for evento in eventos_encontrados:
               titulo, fecha_id, hora_id, duracion, descripcion, importancia, etiquetas = evento
               texto_eventos += f"Título: {titulo}\n" \
                             f"Fecha: {fecha_id}\n" \
                             f"Hora: {hora_id}\n\n"
            messagebox.showinfo("Eventos encontrados", texto_eventos)
        else:
        # Mostrar un mensaje de error si no se encontraron eventos
            messagebox.showerror("Error", "No se encontraron eventos con la búsqueda especificada.")


    def eliminar_evento(self):
        titulo = self.entrada_busqueda.get()
        #print(valor_busqueda)
        #del self.eventos
        Conexion.eliminar_evento(str(titulo))
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
        tabla = ttk.Treeview(frame_tabla, columns=("columna1", "columna2", "columna3", "columna4", "columna5", "columna7"))
        tabla.heading("#0", text="Titulo")
        tabla.heading("columna1", text="fecha")
        tabla.heading("columna2", text="hora")
        tabla.heading("columna3", text="duracion")
        tabla.heading("columna4", text="descripcion")
        tabla.heading("columna5", text="importancia")
        tabla.heading("columna7", text="etiquetas")
        
       
        eventos_registros = Conexion.obtener_eventos()

    # Insertar los eventos en la tabla
        for evento in eventos_registros:
            titulo, fecha_id, hora_id, duracion, descripcion, importancia, etiquetas = evento

        # Aquí creamos el objeto Evento con los valores obtenidos de la base de datos
            nuevo_evento = Evento(titulo,  str(fecha_id), str(hora_id),str(duracion), descripcion, importancia, etiquetas)

            tabla.insert("", "end", text=nuevo_evento.titulo, values=(str(nuevo_evento.fecha),str(nuevo_evento.hora), str(nuevo_evento.duracion), nuevo_evento.descripcion, nuevo_evento.importancia, nuevo_evento.etiquetas))
        
        tabla.pack(expand=True, fill="both")

        # Mostrar ventana secundaria
        ventana_secundaria.mainloop()

    def guardar(self):
        # Obtener los datos ingresados por el usuario en la ventana de modificación
        titulo = self.entry_titulo.get()
        fecha = self.entry_fecha.get().strftime("%Y-%m-%d")  # Convertir la fecha a cadena en formato "aaaa-mm-dd"
        hora = self.entry_hora.get()
        duracion = self.entry_duracion.get()
        descripcion = self.entry_descripcion.get()
        importancia = self.combo_importancia.get()
        etiquetas = self.entry_etiquetas.get()

        # Crear el objeto evento con los datos ingresados
        evento_modificado = Evento(
            titulo=titulo,
            fecha=fecha,
            hora=hora,
            duracion=duracion,
            descripcion=descripcion,
            importancia=importancia,
            etiquetas=etiquetas
        )
        
        Conexion.actualizar_evento(self.evento_actual.id, evento_modificado)

        # Actualizar los datos del evento en la lista de eventos
        index = None
        for i, evento in enumerate(self.eventos):
            if evento.titulo == self.evento_actual.titulo:
                index = i
                break

        if index is not None:
            self.eventos[index] = evento_modificado

        # Mostrar mensaje de éxito
        messagebox.showinfo("Evento modificado", "El evento ha sido modificado exitosamente.")


    def modificarevento(self):
        
        # Obtener eventos de la base de datos
        eventos_registros = Conexion.obtener_eventos()

        if not eventos_registros:
            messagebox.showerror("Error", "No hay eventos para modificar.")
            return

        # Actualizar la lista de eventos
        self.eventos = []
        for registro in eventos_registros:
            evento = Evento(
                titulo=registro[0],
                fecha=registro[1],
                hora=registro[2],
                duracion=registro[3],
                descripcion=registro[4],
                importancia=registro[5],
                etiquetas=registro[6]
            )
            self.eventos.append(evento)

        ventana_secundaria2 = tk.Toplevel(self.frame_evento)
        ventana_secundaria2.title("Calendario de eventos")
        ventana_secundaria2.config(bg="pink")
        ventana_secundaria2.config(relief="groove")
        ventana_secundaria2.config(bd="35")
        ventana_secundaria2.config(cursor="pencil")
        ventana_secundaria2.iconbitmap("calendario.ico")

    # Crear objeto Frame para la ventana de modificación
        frame_modificacion = tk.Frame(ventana_secundaria2)
        frame_modificacion.pack(padx=20, pady=20)

    # Obtener el evento seleccionado
        evento_seleccionado = self.entrada_busqueda.get()
        evento_actual = None

        for evento in self.eventos:
            if evento.titulo == evento_seleccionado:
               evento_actual = evento
               break

        if evento_actual is None:
            messagebox.showerror("Error", "Evento no encontrado.")
            ventana_secundaria2.destroy()
            return

    # Configuración de la ventana
        ventana_secundaria2.title("Modificar evento")

    # Creación del formulario para modificar los datos del evento
        tk.Label(frame_modificacion, text="Título:").grid(row=0, column=0)
        self.entry_titulo = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.titulo))
        self.entry_titulo.grid(row=0, column=1)

        tk.Label(frame_modificacion, text="Fecha (aaaa-mm-dd):").grid(row=1, column=0)
        self.entry_fecha = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.fecha))
        self.entry_fecha.grid(row=1, column=1)

        tk.Label(frame_modificacion, text="Hora (hh:mm:ss):").grid(row=2, column=0)
        self.entry_hora = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.hora))
        self.entry_hora.grid(row=2, column=1)

        tk.Label(frame_modificacion, text="Duración (horas):").grid(row=3, column=0)
        self.entry_duracion = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.duracion))
        self.entry_duracion.grid(row=3, column=1)

        tk.Label(frame_modificacion, text="Descripción:").grid(row=4, column=0)
        self.entry_descripcion = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.descripcion))
        self.entry_descripcion.grid(row=4, column=1)

        tk.Label(frame_modificacion, text="Importancia:").grid(row=5, column=0)
        self.combo_importancia = ttk.Combobox(frame_modificacion, values=["Normal", "Importante"], state="readonly")
        self.combo_importancia.set(evento_actual.importancia)
        self.combo_importancia.grid(row=5, column=1)

        tk.Label(frame_modificacion, text="Etiquetas (separadas por comas):").grid(row=6, column=0)
        self.entry_etiquetas = tk.Entry(frame_modificacion, textvariable=tk.StringVar(value=evento_actual.etiquetas))
        self.entry_etiquetas.grid(row=6, column=1)

        tk.Button(frame_modificacion, text="Guardar cambios", command=self.guardar).grid(row=7, column=0, columnspan=2, pady=10)


#cambiar esto depende lo que desee 

Conexion.create_if_not_exists()
#Conexion.conectar()

root = tk.Tk()

# Pasar la instancia de tkinter.Tk() a la clase CalendarApp
app = CalendarApp(root)

# Llamar al método mainloop() de la instancia de tkinter.Tk()
root.mainloop()