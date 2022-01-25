import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter as tk
from collections import OrderedDict


def valor_desplegable():
  # Tomo la variable global
  global scroll_cuadroy
  global scroll_cuadrox
  global cuadro

  # Elimino las barras laterales y el tree preexistentes
  scroll_cuadrox.destroy()
  scroll_cuadroy.destroy()
  cuadro.destroy()

  # Filtro para que solo muestre lo que quiero
  valor_actual = lista_desplegable.get()
  datos_filtrados = datos[datos["Vendedor"] == valor_actual]
  datos_filtrados = datos_filtrados[datos_filtrados["Dias Vencido"] < 0]
  datos_filtrados = datos_filtrados.iloc[:,[0,1,2,3,5,7]]

  # Inserto la nueva tabla
  df = pd.DataFrame(datos_filtrados)
  cols = list(df.columns)

  cuadro=ttk.Treeview(frame2)
  cuadro.pack()
  cuadro["columns"] = cols

  for i in cols: 
    cuadro.column(i, anchor="w", stretch=0)
    cuadro.heading(i, text=i, anchor='w')

  for index, row in df.iterrows():
    cuadro.insert("",0,text=index,values=list(row))
    cuadro.place(x=0,y=0, width=829, height=720)

  scroll_cuadrox = tk.Scrollbar(frame2, orient="horizontal", command=cuadro.xview)
  scroll_cuadroy = tk.Scrollbar(frame1, orient="vertical", command=cuadro.yview)
  cuadro.configure(xscrollcommand=scroll_cuadrox.set, yscrollcommand=scroll_cuadroy.set)
  scroll_cuadrox.pack(side="bottom", fill="x")
  scroll_cuadroy.pack(side="right", fill="y")


root=Tk()
root.geometry('1080x720')
root.title("Golomax")

# -------------- PANDAS --------------

datos = pd.read_csv("reporte.csv", sep=",", skiprows=6, usecols=(22,24,37,38,40,42,44,46), header=0)

datos.rename(columns={"RazonSocialEmpresa":"Cliente",
                      "DireccionEmpresa": "Direccion",
                      "LocalidadEmpresa": "Localidad",
                      "CodigoPostalEmpresa":"CP",
                      "TelefonoEmpresa":"Telefono",
                      "NombreDivisionEmpresaGrupoEconomicoFormateado2": "Empresa",
                      "FechaDocumento": "Fecha FC",
                      "FechaVencimiento": "Vencimiento",
                      "DiasVencimiento": "Dias Vencido",
                      "NumeroDocumento": "Numero FC",
                      "NombreVendedor": "Vendedor",
                      "ImporteVencimiento": "Importe"}, inplace=True)

datos["Importe"] = datos["Importe"].apply(lambda x: x.replace("$",""))
datos["Importe"] = datos["Importe"].apply(lambda x: x.replace(" ",""))
datos["Importe"] = datos["Importe"].apply(lambda x: x.replace(",",".")).astype(float)

datos["Vendedor"] = datos["Vendedor"].apply(lambda x: x.replace("G - ", ""))
datos["Vendedor"] = datos["Vendedor"].apply(lambda x: x.replace("C - ", ""))

# no_facturas = datos[datos["Comprobante"] != "Factura de Ventas"].index
# datos.drop(no_facturas, inplace= True)

vendedores = datos["Vendedor"].unique()
vendedores = sorted(list(vendedores))

datos2 = datos.iloc[:,[0,1,2,3,5,7]]


# ----------------------------------------

# Cuadro
frame1 = Frame(root, bg="#bfdaff")
frame1.place(x=0,y=0,width=250, height=720)

# Abrir Archivos
frame2 = Frame(root)
frame2.place(x=251,y=0, width=829, height=720)

# Botones
boton1 = Button(frame1, text="Buscar", command=valor_desplegable)
boton1.place(x=20, y=90)


# Cuadro
df = pd.DataFrame(datos2)
cols = list(df.columns)

cuadro=ttk.Treeview(frame2)
cuadro.pack()
cuadro["columns"] = cols
for i in cols:
    cuadro.column(i, anchor="w", stretch=0)
    cuadro.heading(i, text=i, anchor='w')

for index, row in df.iterrows():
    cuadro.insert("",0,text=index,values=list(row))
    cuadro.place(x=0,y=0, width=829, height=720)

# Scroll Cuadro
scroll_cuadrox = tk.Scrollbar(frame2, orient="horizontal", command=cuadro.xview)
scroll_cuadroy = tk.Scrollbar(frame1, orient="vertical", command=cuadro.yview)
cuadro.configure(xscrollcommand=scroll_cuadrox.set, yscrollcommand=scroll_cuadroy.set)
scroll_cuadrox.pack(side="bottom", fill="x")
scroll_cuadroy.pack(side="right", fill="y")


# Lista Desplegable
lista_desplegable = ttk.Combobox(frame1, values= list(vendedores), state="readonly")
lista_desplegable.place(x=20, y=50)






root.mainloop()
