from tkinter import*
import tkinter as tk
import datetime
import csv
import tkinter.messagebox as messagebox
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from calendario_stage4 import *

                        
#...............pantalla................
raiz=tk.Tk()
raiz.iconbitmap("calendario.ico")
raiz.geometry("500x600")
raiz.title("calendario de eventos")
raiz.config(bg="pink")
miFrame=Frame(raiz)
miFrame.pack()
miFrame.config(bd="25")
miFrame.config(relief="raised")
miFrame.config(bg="pink")
miFrame.config(cursor="hand2")
Label(miFrame,text="Lunes").grid(row=1,column=2)
Label(miFrame,text="Martes").grid(row=1,column=3)
Label(miFrame,text="Miercoles").grid(row=1,column=4)
Label(miFrame,text="Jueves").grid(row=1,column=5)
Label(miFrame,text="Viernes").grid(row=1,column=6)
Label(miFrame,text="Sabado").grid(row=1,column=7)
Label(miFrame,text="Domingo").grid(row=1,column=8)

#..................pantalla2......................

def envia_boton():
   ventana_secundaria= tk.Toplevel(raiz)
   calendario= CalendarApp(ventana_secundaria)



#......................fila1........................................


boton1=Button(miFrame,text="1",width=7,command=envia_boton)
boton1.grid(row=3 , column=2 )
boton2=Button(miFrame,text="2",width=7,command=envia_boton)
boton2.grid(row=3 , column=3 )
boton3=Button(miFrame,text="3",width=7,command=envia_boton)
boton3.grid(row=3 , column=4 )
boton4=Button(miFrame,text="4",width=7,command=envia_boton)
boton4.grid(row=3 , column=5 )
boton5=Button(miFrame,text="5",width=7,command=envia_boton)
boton5.grid(row=3 , column=6 )
boton6=Button(miFrame,text="6",width=7,command=envia_boton)
boton6.grid(row=3 , column=7 )
boton7=Button(miFrame,text="7",width=7,command=envia_boton)
boton7.grid(row=3 , column=8 )
#..........................fila2.............................

boton8=Button(miFrame,text="8",width=7,command=envia_boton)
boton8.grid(row=4 , column=2 )
boton9=Button(miFrame,text="9",width=7,command=envia_boton)
boton9.grid(row=4 , column=3 )
boton10=Button(miFrame,text="10",width=7,command=envia_boton)
boton10.grid(row=4 , column=4 )
boton11=Button(miFrame,text="11",width=7,command=envia_boton)
boton11.grid(row=4 , column=5 )
boton12=Button(miFrame,text="12",width=7,command=envia_boton)
boton12.grid(row=4 , column=6 )
boton13=Button(miFrame,text="13",width=7,command=envia_boton)
boton13.grid(row=4 , column=7 )
boton14=Button(miFrame,text="14",width=7,command=envia_boton)
boton14.grid(row=4 , column=8 )

#.............................fila3.............................

boton15=Button(miFrame,text="15",width=7,command=envia_boton)
boton15.grid(row=5 , column=2 )
boton16=Button(miFrame,text="16",width=7,command=envia_boton)
boton16.grid(row=5 , column=3 )
boton17=Button(miFrame,text="17",width=7,command=envia_boton)
boton17.grid(row=5 , column=4 )
boton18=Button(miFrame,text="18",width=7,command=envia_boton)
boton18.grid(row=5 , column=5 )
boton19=Button(miFrame,text="19",width=7,command=envia_boton)
boton19.grid(row=5 , column=6 )
boton20=Button(miFrame,text="20",width=7,command=envia_boton)
boton20.grid(row=5 , column=7 )
boton21=Button(miFrame,text="21",width=7,command=envia_boton)
boton21.grid(row=5 , column=8 )

#........................fila4.............................

boton22=Button(miFrame,text="22",width=7,command=envia_boton)
boton22.grid(row=6 , column=2 )
boton23=Button(miFrame,text="23",width=7,command=envia_boton)
boton23.grid(row=6 , column=3 )
boton24=Button(miFrame,text="24",width=7,command=envia_boton)
boton24.grid(row=6 , column=4 )
boton25=Button(miFrame,text="25",width=7,command=envia_boton)
boton25.grid(row=6 , column=5 )
boton26=Button(miFrame,text="26",width=7,command=envia_boton)
boton26.grid(row=6 , column=6 )
boton27=Button(miFrame,text="27",width=7,command=envia_boton)
boton27.grid(row=6 , column=7 )
boton28=Button(miFrame,text="28",width=7,command=envia_boton)
boton28.grid(row=6 , column=8 )


#.............fila5.............

boton29=Button(miFrame,text="29",width=7,command=envia_boton)
boton29.grid(row=7 , column=2 )
boton30=Button(miFrame,text="30",width=7,command=envia_boton)
boton30.grid(row=7 , column=3 )
boton31=Button(miFrame,text="31",width=7,command=envia_boton)
boton31.grid(row=7 , column=4 )


#def crear_eventos():
 #   eventos=entrada_titulo.get()
  #  return eventos
    





raiz.mainloop()