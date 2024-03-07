from tkinter import ttk, messagebox
import tkinter as tk
import numpy as np
import pandas as pd
import cv2 as cv
import tkinter.messagebox as mesagebox
from PIL import Image, ImageTk
import os
from aws import Aws
import zipfile
import connection
import threading



input_camara = 1
widht = 1280
height  = 720
nombre_notebook = 'NOTE-888'



class Producto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=170)
        self.master = master

        array_producto = []
        array_lista_nombres_producto = []
        self.lista_fotos_producto_duplicados = []
        self.lista_nombres_fotos_producto_duplicados = []


        self.registro =  pd.DataFrame
        self.congelar_producto = False
        self.congelar_parte_productos = False
        self.congelar_video_servidor = False
        self.lock = threading.Lock()


        self.df = pd.read_csv("./CSVs/AnalisisFisico.csv", sep='|', dtype=str)
        self.df_filtrado  = pd.DataFrame



        self.estilo={
            "background1": "#010937",
            "background2": "#020f59",
            "background3": "#101f78",
            "font_color": "white",
            "fuente": ("Arial", 12, "bold"),
            "tamano_boton": (10, 2)
        }

        self.master.geometry("1366x768")
        self.create_widgets()


    def on_checkbox_toggle(self):
        if self.checkbox_var.get() == 1:
            if self.image : self.image.release()
            self.congelar_producto = True
            self.congelar_parte_productos = True
            self.congelar_video_servidor = False
            self.frame_foto.grid_remove()
            self.frame_foto_pesa.grid(row=0, column=1, sticky="nsew", padx=10 , pady=10)
            connection.conectarServidor()
            self.mostrarImagenServidor()
            connection.desconectarServidor()
            
        else:
            self.congelar_producto = False
            self.congelar_video_servidor = True
            self.frame_foto.grid(row=0, column=1, sticky="nsew", padx=10 , pady=10)
            self.frame_foto_pesa.grid_remove()
            self.image = cv.VideoCapture(input_camara)

            self.actualizar_video_producto()



    
    def create_widgets(self):

        self.titulo = tk.Label(text='AnfiBot', font=("KacstBook", 48, 'bold'))
        self.titulo.pack()

        self.notebook = ttk.Notebook(self.master)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.pack()

        self.frame_productos        = tk.Frame(self.notebook, width=1366, height=768)
        self.frame_parte_productos  = tk.Frame(self.notebook, width=1366, height=768)
        self.frame_categoria_parte  = tk.Frame(self.notebook, width=1366, height=768)
        self.frame_duplicado_parte  = tk.Frame(self.notebook, width=1366, height=768)
        self.frame_aws              = tk.Frame(self.notebook, width=1366, height=768)
        self.frame_csv_server       = tk.Frame(self.notebook, width=1366, height=768)

        
        #======================================
        #========PAGE (PRODUCTOS)==============
        #======================================
        self.frame_productos.grid(row=1, column=0, sticky="nsew")


            #---------------FRAME ENTRADAS---------------------
        self.frame_entradas = tk.LabelFrame(self.frame_productos, text='Inputs')
        self.frame_entradas.grid(row=0, column=0, sticky="nsew", padx=10 , pady=10)


        
        self.contador_sku_label = tk.Label(self.frame_entradas, text='Contador SKU: ')
        self.sku_label          = tk.Label(self.frame_entradas, text='SKU')
        self.ean_label          = tk.Label(self.frame_entradas, text='EAN')
        self.descripcion_label  = tk.Label(self.frame_entradas, text='DESCRIPCION')

        self.sku_input          = ttk.Entry(self.frame_entradas)
        self.ean_input          = ttk.Entry(self.frame_entradas)
        self.descripcion_input  = tk.Text(self.frame_entradas)
        self.descripcion_input.config(width=20, height=4)



            #--------------FRAME DE FOTO----------------------
        self.frame_foto = tk.LabelFrame(self.frame_productos, text='Foto')
        self.frame_foto.grid(row=0, column=1, sticky="nsew", padx=10 , pady=10)

        self.frame_foto_pesa = tk.LabelFrame(self.frame_productos, text='Foto PESA')
        self.frame_foto_pesa.grid_remove()
    
        
        self.label_video                    = tk.Label(self.frame_foto)
        self.image                          = None

        self.lienzo_video_server = tk.Canvas(self.frame_foto_pesa, width=640, height=480)

        self.nombre_imagen_producto_label   = tk.Label(self.frame_foto, text='Aqui el nombre de tus imagenes ...')
        self.nombre_imagen_producto_label.grid_propagate(False) 

        self.capturar_imagen_button         = tk.Button(self.frame_foto, text="Capturar",height = 2, command=self.capturarImagen)
        self.eliminar_ultima_imagen_button  = tk.Button(self.frame_foto, text="Eliminar",height = 2, command=self.eliminarUltimaImagen)


            #---------------FRAME INFORMACION---------------------
        self.frame_informacion = tk.LabelFrame(self.frame_productos, text='Información')
        self.frame_informacion.grid(row=0, column=2, sticky="nsew", padx=10)

        self.categoria_eye_domiciliario_label           = tk.Label(self.frame_informacion, text='Eye Domiciliario : ')
        self.categoria_eye_no_domiciliario_label        = tk.Label(self.frame_informacion, text='Eye NO Domiciliario: ')
        self.categoria_raee                             = tk.Label(self.frame_informacion, text='RAEE: ')
        self.categoria_aceite_y_lubricante              = tk.Label(self.frame_informacion, text='Aceites y Lubricantes: ')
        self.categoria_baterias                         = tk.Label(self.frame_informacion, text='Baterías: ')
        self.categoria_neumaticos                       = tk.Label(self.frame_informacion, text='Neumáticos: ')
        self.pilas                                      = tk.Label(self.frame_informacion, text='Pilas: ')

            #---------------FRAME OPTION PESA---------------------
        self.frame_check_foto_pesa = tk.LabelFrame(self.frame_productos, text='Cámara pesa')
        self.frame_check_foto_pesa.grid(row=2, column=1, sticky="nsew", padx=5)

        self.checkbox_var = tk.IntVar()
        self.check_activar_foto_pesa        = ttk.Checkbutton(self.frame_check_foto_pesa, text="Activar cámara pesa:", variable=self.checkbox_var, command=self.on_checkbox_toggle)
                
                #-------GRID-------------
        #input
        self.contador_sku_label.grid        (row=0, column=1, padx=10, pady=20)
        self.sku_label.grid                 (row=1, column=0, padx=10, pady=40)
        self.sku_input.grid                 (row=1, column=1, padx=10, pady=40)
        self.ean_label.grid                 (row=2, column=0, padx=10, pady=40)
        self.ean_input.grid                 (row=2, column=1, padx=10, pady=40)
        self.descripcion_label.grid         (row=3, column=0, padx=10, pady=40)
        self.descripcion_input.grid         (row=3, column=1, padx=10, pady=40)
        
        #fotos
        self.label_video.grid                   (row=0, column=0, columnspan=3,  padx=5, pady=20)
        self.label_video.grid                   (row=1, column=0, columnspan=3,  padx=5, pady=20)
        self.lienzo_video_server.grid           (row=0, column=0, columnspan=3,  padx=5, pady=20)
        self.capturar_imagen_button.grid        (row=2, column=0, padx=5, pady=20)
        self.nombre_imagen_producto_label.grid  (row=2, column=1, padx=5, pady=20)
        self.eliminar_ultima_imagen_button.grid (row=2, column=2, padx=5, pady=20)

        #info
        self.categoria_eye_domiciliario_label.grid      (row=0, column=0, padx=10, pady=20)
        self.categoria_eye_no_domiciliario_label.grid   (row=1, column=0, padx=10, pady=20)
        self.categoria_raee.grid                        (row=2, column=0, padx=10, pady=20)
        self.categoria_aceite_y_lubricante.grid         (row=3, column=0, padx=10, pady=20)
        self.categoria_baterias.grid                    (row=4, column=0, padx=10, pady=20)
        self.categoria_neumaticos.grid                  (row=5, column=0, padx=10, pady=20)
        self.pilas.grid                                 (row=6, column=0, padx=10, pady=20)

        #pesa
        self.check_activar_foto_pesa.grid (row=0, column=0, padx=10, pady=20) 

        
        #===========================================
        #========PAGE (PARTE PRODUCTOS)=============
        #===========================================
        self.frame_parte_productos.grid(row=0, column=0, sticky="nsew") 
        
        
         #---------------FRAME ENTRADAS---------------------
        self.frame_entradas_partes_producto = tk.LabelFrame(self.frame_parte_productos, text='Inputs')
        self.frame_entradas_partes_producto.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.contador_sku_label_partes_producto_label     = tk.Label(self.frame_entradas_partes_producto, text='Contador SKU: ')
        self.nombre_parte_priducto_label                  = tk.Label(self.frame_entradas_partes_producto, text='Nombre Parte del Producto') 
        self.peso_parte_producto_label                    = tk.Label(self.frame_entradas_partes_producto, text='Peso Parte del Producto') 
        self.categoria_del_producto_label                 = tk.Label(self.frame_entradas_partes_producto, text='Categoría del Producto') 

        self.nombre_parte_producto_input           = ttk.Entry(self.frame_entradas_partes_producto)
        self.peso_parte_producto_input             = ttk.Entry(self.frame_entradas_partes_producto)
        self.categoria_del_producto_input          = ttk.Combobox(
                                                        self.frame_entradas_partes_producto,
                                                        state   = "readonly",
                                                        values  = [
                                                            "EYE Domiciliario",
                                                            "EYE No domiciliario",
                                                            "RAEE",
                                                            "Aceites y lubricantes",
                                                            "Baterías",
                                                            "Neumáticos",
                                                            "PILAS",
                                                        ])
        self.categoria_del_producto_input.current(0)


        #--------------FRAME DE FOTO----------------------
        self.frame_foto_partes_producto = tk.LabelFrame(self.frame_parte_productos, text='Foto')
        self.frame_foto_partes_producto.grid(row=0, column=1, sticky="nsew", padx=10 , pady=10)


        
        self.label_video_parte_productos    = tk.Label(self.frame_foto_partes_producto)
        self.image_parte_productos          = None

        self.nombre_parte_producto_label    = tk.Label(self.frame_foto_partes_producto, text='')


        self.capturar_imagen_parte_producto_button      = tk.Button(self.frame_foto_partes_producto, text="Capturar",height = 2, command=self.capturarImagenPartes)
        self.recapturar_imagen_parte_producto_button    = tk.Button(self.frame_foto_partes_producto, text="RE - Capturar",height = 2, command=self.descongelarImagen)
        self.recapturar_imagen_parte_producto_button.config(state='disable')
        




        self.contador_sku_label_partes_producto_label.grid  (row=1, column=0, padx=10, pady=20)
        self.nombre_parte_priducto_label.grid               (row=2, column=0, padx=10, pady=40)
        self.nombre_parte_producto_input.grid              (row=2, column=1, padx=10, pady=40)
        self.peso_parte_producto_label.grid                 (row=3, column=0, padx=10, pady=40)
        self.peso_parte_producto_input.grid                (row=3, column=1, padx=10, pady=40)
        self.categoria_del_producto_label.grid              (row=4, column=0, padx=10, pady=40)
        self.categoria_del_producto_input.grid             (row=4, column=1 )

        self.label_video_parte_productos.grid                   (row=0, column=0, columnspan=3,  padx=5, pady=20)
        self.nombre_parte_producto_label.grid                   (row=1, column=0, columnspan=3,  padx=5, pady=20)
        self.capturar_imagen_parte_producto_button.grid         (row=1, column=1, columnspan=3,  padx=5, pady=20)
        self.recapturar_imagen_parte_producto_button.grid       (row=1, column=2, columnspan=3,  padx=5, pady=20)



        #============================================
        #========PAGE (CATEGORIA PARTES)=============
        #============================================
        self.frame_categoria_parte.grid(row=0, column=0, sticky="nsew") 

        self.frame_entradas_categoria_partes = tk.LabelFrame(self.frame_categoria_parte, text='Inputs')
        self.frame_entradas_categoria_partes.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_informacion_csv = tk.LabelFrame(self.frame_categoria_parte, text='SKUS')
        self.frame_informacion_csv.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_tabla = self.frame_informacion_csv
        self.frame_tabla.place(x= 500, y=10, height=550, width=350)

        #=========================
        #======CATEGORIA EYE======
        #=========================


        self.categoría_eye_label            = ttk.Label(self.frame_entradas_categoria_partes, text="Material EYE")
        self.categoría_eye_input            = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "CARTÓN",
                                                    "Envases de PP que NO contienen sustancias con grasa (5)",
                                                    "PVC (3)",
                                                    "MADERA",
                                                    "Papel",
                                                    "Otros envases plásticos (7)",
                                                    "Envases de PS que NO contienen sustancias con grasa (6)",
                                                    "Otros envases PET (1)",
                                                    "Envases de PEBD que NO contienen sustancias con grasa (4)",
                                                    "Envases de PEAD que NO contienen sustancias con grasa (2)",
                                                    "VIDRIO",
                                                    "Hojalata",
                                                    "OTRO MATERIAL",
                                                    "Envases de PP que  contienen sustancias con grasa (5)",
                                                    "Envases de PEBD que  contienen sustancias con grasa (4)",
                                                    "Envases de aluminio",
                                                    "Botellas PET (1)",
                                                    "Otro papel compuesto",
                                                    "Envases de PS que  contienen sustancias con grasa (6) y envases de EPS",
                                                    "CARTÓN PARA BEBIDAS",
                                                    "Aluminio (latas)",
                                                    "Envases de PEAD que contienen sustancias con grasa (2)",
                                                    "Otros Envases de Metal",
                                                    "Metal con aire comprimido",
                                                    "Plástico compostable",
                                                    "PULPA DE PAPEL",
                                                ])

        self.caracteristicas_eye_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Caracteristicas")
        self.caracteristicas_eye_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Flexible",
                                                    "Rigido",
                                                    "Corrugado",
                                                    "Transparente",
                                                    "Color",
                                                    "Cartulina",
                                                    "Compuesto",
                                                ])

        self.definir_otro_label             = ttk.Label(self.frame_entradas_categoria_partes, text="Definir Otro")
        self.definir_otro_input             = ttk.Entry(self.frame_entradas_categoria_partes,width=32)


        self.productos_por_envase_label     = ttk.Label(self.frame_entradas_categoria_partes, text="Productos por envase")
        self.productos_por_envase_input     = ttk.Entry(self.frame_entradas_categoria_partes,width=32)


        self.tipo_de_parte_label            = ttk.Label(self.frame_entradas_categoria_partes, text="Tipo de Parte")
        self.tipo_de_parte_input            = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "PRIMARIO",
                                                    "SECUNDARIO",
                                                    "TERCIARIO",
                                                ])


        self.caract_reciclable_label        = ttk.Label(self.frame_entradas_categoria_partes, text="Caracteriticas Reciclables")
        self.caract_reciclable_input        = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Sin material reciclado",
                                                    "100% Material reciclado",
                                                ])


        self.caract_retornable_label        = ttk.Label(self.frame_entradas_categoria_partes, text="Caracteriticas Retornable")
        self.caract_retornable_input        = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "No Retornable",
                                                    "Retornable Nuevo",
                                                ])


        self.peligrosidad_label             = ttk.Label(self.frame_entradas_categoria_partes, text="Peligrosidad")
        self.peligrosidad_input             = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Residuo NO Peligroso",
                                                    "Residuo Peligroso",
                                                ])



        #=========================
        #=====CATEGORIA RAEE======
        #=========================
        self.categoria_raee_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Categoria RAEE")
        self.categoria_raee_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Aparatos de intercambio de temperatura",
                                                    "Aparatos grandes superior a los 50cm",
                                                    "AP - Otros aparatos pequeños",
                                                    "Aparatos pequeños inferior a los 50cm",
                                                    "Lámparas",
                                                    "Pantallas superior a los 100cm2",
                                                ])


        #===============================
        #=====ACEITE Y LUBRICANTE=======
        #===============================
        self.categoria_aceites_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Categoria Aceite y Lubricante")
        self.categoria_aceites_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Aceites Lubricantes No Recuperables",
                                                    "Aceites Lubricantes Recuperables",
                                                ])


        self.cantidad_m_cubico_label     = ttk.Label(self.frame_entradas_categoria_partes, text="Cantidad m cubicos")
        self.cantidad_m_cubico_input     = ttk.Entry(self.frame_entradas_categoria_partes,width=32)


        #===============================
        #===========BATERIAS============
        #===============================
        self.categoria_baterias_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Categoria Bateria")
        self.categoria_baterias_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "De plomo para vehiculos motorizados",
                                                    "De plomo industriales",
                                                    "Otras baterias, pilas o acumuladores para vehiculos motorizados"
                                                ])


        #==============================
        #==========NEUMATICOS==========
        #==============================
        self.categoria_neumatico_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Categoria Neumatico")
        self.categoria_neumatico_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "CATEGORÍA A",
                                                    "CATEGORÍA B",
                                                    "MACIZOS",
                                                    "Bicicletas, sillas de rueda y similares"
                                                ])


        self.cantidad_m_neumatico_label     = ttk.Label(self.frame_entradas_categoria_partes, text="Cantidad de Neumaticos")
        self.cantidad_m_neumatico_input     = ttk.Entry(self.frame_entradas_categoria_partes,width=32)


        #===============================
        #=============PILAS=============
        #===============================
        self.categoria_pilas_label      = ttk.Label(self.frame_entradas_categoria_partes, text="Categoria Pilas")
        self.categoria_pilas_input      = ttk.Combobox(self.frame_entradas_categoria_partes,
                                                width=30,
                                                state   = "readonly",
                                                values  = [
                                                    "Botón litio",
                                                    "Botón mercurio",
                                                    "Botón óxido de manganeso",
                                                    "Botón óxido de plata",
                                                    "Botón zinc aire",
                                                    "Botón alcalinas",
                                                    "Estándar alcalina",
                                                    "Estándar litio no recargable",
                                                    "Estándar zinc carbón",
                                                    "Estándar zinc dióxido de manganeso",
                                                    "Acumulador niquel-cadmio",
                                                    "Acumulador níquel hidruro metálico",
                                                    "Acumulador ion litio",
                                                    "Otras pilas",
                                                ])


        self.cantidad_m_pilas_input     = ttk.Entry(self.frame_entradas_categoria_partes,width=32)
        self.cantidad_m_pilas_label     = ttk.Label(self.frame_entradas_categoria_partes, text="Cantidad de Pilas")

        #======================================
        #===================SKUS===============
        #======================================

        self.tree_view = ttk.Treeview(self.frame_tabla)
        self.tree_view.place(relheight=1, relwidth=1, width=200)

        tree_scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree_view.yview) 
        tree_scroll_x = tk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree_view.xview)

        self.tree_view.configure(xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)

        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")

        self.mostrarDf(self.tree_view)

        #=======================================
        #==============botones==================
        #=======================================

        self.otra_parte_button      = tk.Button(self.frame_categoria_parte, text="Otra Parte",height = 2, command=self.otraParte)
        self.otra_parte_button.place(x= 900, y=100)
        self.otra_producto_button   = tk.Button(self.frame_categoria_parte, text="Otro Producto",height = 2, command=self.otroProducto)
        self.otra_producto_button.place(x= 900, y=200)
        self.eliminar_ultimo_button = tk.Button(self.frame_categoria_parte, text="Eliminar Ultimo Registro",height = 2, command=self.EliminarUltimoRegistro)
        self.eliminar_ultimo_button.place(x= 900, y=300)

        self.traer_un_registro_ean  = tk.Entry(self.frame_categoria_parte, width=20)
        self.traer_un_registro_ean.place(x= 900, y=400)
        self.traer_un_registro_button = tk.Button(self.frame_categoria_parte, text="Traer Registro",height = 2, command=self.traerRegistro)
        self.traer_un_registro_button.place(x= 900, y=430)
        self.subir_un_registro_button = tk.Button(self.frame_categoria_parte, text="Subir Registro",height = 2, command=self.subirRegistro)
        self.subir_un_registro_button.place(x= 1050, y=430)
        self.subir_un_registro_button.config(state='disable')




        self.categoría_eye_label.grid           (row=1, column=0, padx=6, pady=6)
        self.categoría_eye_input.grid           (row=1, column=1, padx=6, pady=6)
        self.caracteristicas_eye_label.grid     (row=2, column=0, padx=6, pady=6)      
        self.caracteristicas_eye_input.grid     (row=2, column=1, padx=6, pady=6)
        self.definir_otro_label.grid            (row=3, column=0, padx=6, pady=6)
        self.definir_otro_input.grid            (row=3, column=1, padx=6, pady=6)
        self.productos_por_envase_label.grid    (row=4, column=0, padx=6, pady=6)
        self.productos_por_envase_input.grid    (row=4, column=1, padx=6, pady=6)
        self.tipo_de_parte_label.grid           (row=5, column=0, padx=6, pady=6)
        self.tipo_de_parte_input.grid           (row=5, column=1, padx=6, pady=6)
        self.caract_reciclable_label.grid       (row=6, column=0, padx=6, pady=6)
        self.caract_reciclable_input.grid       (row=6, column=1, padx=6, pady=6)
        self.caract_retornable_label.grid       (row=7, column=0, padx=6, pady=6)
        self.caract_retornable_input.grid       (row=7, column=1, padx=6, pady=6)
        self.peligrosidad_label.grid            (row=8, column=0, padx=6, pady=6)
        self.peligrosidad_input.grid            (row=8, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------
        self.categoria_raee_label.grid          (row=9, column=0, padx=6, pady=6)
        self.categoria_raee_input.grid          (row=9, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------
        self.categoria_aceites_label.grid       (row=10, column=0, padx=6, pady=6)
        self.categoria_aceites_input.grid       (row=10, column=1, padx=6, pady=6)
        self.cantidad_m_cubico_label.grid       (row=11, column=0, padx=6, pady=6)
        self.cantidad_m_cubico_input.grid       (row=11, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------
        self.categoria_baterias_label.grid      (row=12, column=0, padx=6, pady=6)
        self.categoria_baterias_input.grid      (row=12, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------
        self.categoria_neumatico_label.grid     (row=13, column=0, padx=6, pady=6)
        self.categoria_neumatico_input.grid     (row=13, column=1, padx=6, pady=6)
        self.cantidad_m_neumatico_label.grid    (row=14, column=0, padx=6, pady=6)
        self.cantidad_m_neumatico_input.grid    (row=14, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------
        self.categoria_pilas_label.grid         (row=15, column=0, padx=6, pady=6)
        self.categoria_pilas_input.grid         (row=15, column=1, padx=6, pady=6)
        self.cantidad_m_pilas_label.grid        (row=16, column=0, padx=6, pady=6)
        self.cantidad_m_pilas_input.grid        (row=16, column=1, padx=6, pady=6)
        #------------------------------------------------------------------------


        #==========================================
        #========PAGE (DUPLICADO PARTES)===========
        #==========================================
        self.frame_duplicado_parte.grid(row=0, column=0, sticky="nsew") 

        #--------------------CSV DATA ---------------------
        self.frame_duplicado_data = tk.LabelFrame(self.frame_duplicado_parte, text='Data')
        self.frame_duplicado_data.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_tabla_duplicado = self.frame_duplicado_data
        self.frame_tabla_duplicado.place(x= 10, y=10, height=550, width=350)

        self.tree_view_duplicado_data = ttk.Treeview(self.frame_tabla_duplicado)
        self.tree_view_duplicado_data.place(relheight=1, relwidth=1, width=200)

        tree_scroll_y_duplicado_data = tk.Scrollbar(self.frame_tabla_duplicado, orient="vertical", command=self.tree_view_duplicado_data.yview) 
        tree_scroll_x_duplicado_Data = tk.Scrollbar(self.frame_tabla_duplicado, orient="horizontal", command=self.tree_view_duplicado_data.xview)

        self.tree_view_duplicado_data.configure(xscrollcommand=tree_scroll_x_duplicado_Data.set, yscrollcommand=tree_scroll_y_duplicado_data.set)

        tree_scroll_y_duplicado_data.pack(side="right", fill="y")
        tree_scroll_x_duplicado_Data.pack(side="bottom", fill="x")

        self.mostrarDf(self.tree_view_duplicado_data)

        #--------------------FILTROS---------------------
        self.frame_duplicado_filtros = tk.LabelFrame(self.frame_duplicado_parte, text='Filtros')
        self.frame_duplicado_filtros.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_duplicado_filtros.place(x= 370, y=10, height=550, width=550)

        self.sku_filtro_label       = tk.Label(self.frame_duplicado_filtros, text='SKU filtro')
        self.sku_filtro_input       = tk.Entry(self.frame_duplicado_filtros, width=20)
        self.filtrar_button         = tk.Button(self.frame_duplicado_filtros, text="Filtrar",height = 2, command=self.mostrarFiltrado)
        self.ean_filtro_label       = tk.Label(self.frame_duplicado_filtros, text='EAN filtro')
        self.ean_filtro_input       = tk.Entry(self.frame_duplicado_filtros, width=20)

        self.nuevo_nombre_producto_filtrado_label   = tk.Label(self.frame_duplicado_filtros, text='Nuevo Nombre de Imagen')
        self.nuevo_nombre_producto_filtrado_input   = tk.Entry(self.frame_duplicado_filtros, width=18)

        self.nuevo_sku_filtrado_label   = tk.Label(self.frame_duplicado_filtros, text='Nuevo SKU de Imagen')
        self.nuevo_sku_filtrado_input   = tk.Entry(self.frame_duplicado_filtros, width=18)

        self.nuevo_ean_filtrado_label   = tk.Label(self.frame_duplicado_filtros, text='Nuevo EAN de Imagen')
        self.nuevo_ean_filtrado_input   = tk.Entry(self.frame_duplicado_filtros, width=18)

        self.duplicar_data                          = tk.Button(self.frame_duplicado_filtros, text="Duplicar",height = 2, command=self.duplicarData)


        self.sku_filtro_label.grid                      (row=0, column=0, padx=6, pady=6)
        self.sku_filtro_input.grid                      (row=1, column=0, padx=6, pady=6)
        self.ean_filtro_label.grid                      (row=0, column=2, padx=6, pady=6)
        self.ean_filtro_input.grid                      (row=1, column=2, padx=6, pady=6)
        self.filtrar_button.grid                        (row=3, column=1, padx=6, pady=6)
        self.nuevo_nombre_producto_filtrado_label.grid  (row=4, column=1, padx=6, pady=6)
        self.nuevo_nombre_producto_filtrado_input.grid  (row=5, column=1, padx=6, pady=6)
        self.nuevo_sku_filtrado_label.grid              (row=6, column=1, padx=6, pady=6)
        self.nuevo_sku_filtrado_input.grid              (row=7, column=1, padx=6, pady=6)
        self.nuevo_ean_filtrado_label.grid              (row=8, column=1, padx=6, pady=6)
        self.nuevo_ean_filtrado_input.grid              (row=9, column=1, padx=6, pady=6)


        self.duplicar_data.grid                         (row=10, column=1, padx=6, pady=6)


        #----------------DATA FILTRADA-------------------
        self.frame_duplicado_data_filtrada = tk.LabelFrame(self.frame_duplicado_parte, text='Data')
        self.frame_duplicado_data_filtrada.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_tabla_filtrada = self.frame_duplicado_data_filtrada
        self.frame_tabla_filtrada.place(x= 930, y=10, height=550, width=400)

        self.tree_view_duplicado_data_filtrada = ttk.Treeview(self.frame_tabla_filtrada)
        self.tree_view_duplicado_data_filtrada.place(relheight=1, relwidth=1, width=200)

        tree_scroll_y_duplicado_data_filtrada = tk.Scrollbar(self.frame_tabla_filtrada, orient="vertical", command=self.tree_view_duplicado_data_filtrada.yview) 
        tree_scroll_x_duplicado_Data_fitrada = tk.Scrollbar(self.frame_tabla_filtrada, orient="horizontal", command=self.tree_view_duplicado_data_filtrada.xview)

        self.tree_view_duplicado_data_filtrada.configure(xscrollcommand=tree_scroll_x_duplicado_Data_fitrada.set, yscrollcommand=tree_scroll_y_duplicado_data_filtrada.set)

        tree_scroll_y_duplicado_data_filtrada.pack(side="right", fill="y")
        tree_scroll_x_duplicado_Data_fitrada.pack(side="bottom", fill="x")

        

        #=============================
        #========PAGE (AWS)===========
        #=============================

        self.nombrecsv_aws_label    = tk.Label(self.frame_aws, text='Coloque el nombre del archivo')
        self.nombrecsv_aws_input    = tk.Entry(self.frame_aws)
        self.subir_aws_button       = tk.Button(self.frame_aws, text="Subir Archivo",height = 2, command=self.subirAWS)

        self.nombrecsv_aws_label.pack(pady=6)
        self.nombrecsv_aws_input.pack(pady=6)
        self.subir_aws_button.pack(pady=6)

        #=======================================
        #========PAGE (DATA SINERGIA)===========
        #=======================================
        self.frame_csv_server.grid(row=0, column=0, sticky="nsew") 

        self.frame_csv_sinergia = tk.LabelFrame(self.frame_csv_server, text='Data Sinergia')
        self.frame_csv_sinergia.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_tabla_data_sinergia = self.frame_csv_sinergia
        self.frame_tabla_data_sinergia.place(x= 10, y=10, height=550, width=1100)

        self.tree_view_data_sinergia = ttk.Treeview(self.frame_tabla_data_sinergia)
        self.tree_view_data_sinergia.place(relheight=1, relwidth=1, width=200)

        tree_scroll_y_data_sinergia = tk.Scrollbar(self.frame_tabla_data_sinergia, orient="vertical", command=self.tree_view_data_sinergia.yview) 
        tree_scroll_x_data_sinergia = tk.Scrollbar(self.frame_tabla_data_sinergia, orient="horizontal", command=self.tree_view_data_sinergia.xview)

        self.tree_view_data_sinergia.configure(xscrollcommand=tree_scroll_x_data_sinergia.set, yscrollcommand=tree_scroll_y_data_sinergia.set)

        tree_scroll_y_data_sinergia.pack(side="right", fill="y")
        tree_scroll_x_data_sinergia.pack(side="bottom", fill="x")


        #self.mostrarDataSinergiaCSV(self.tree_view_data_sinergia)



        self.notebook.add(self.frame_productos, text='Productos')
        self.notebook.add(self.frame_parte_productos, text='Partes Producto')
        self.notebook.add(self.frame_categoria_parte, text='Categoria')
        self.notebook.add(self.frame_duplicado_parte, text='Duplicado de Partes')
        self.notebook.add(self.frame_aws, text='AWS')
        self.notebook.add(self.frame_csv_server, text='Data Sinergia')

    def on_tab_changed(self, event):
        page = self.notebook.index(self.notebook.select())
        df_cant_sku = pd.read_csv('./CSVs/AnalisisFisico.csv', sep='|')
        cantidad_sku = df_cant_sku.iloc[:, 0].nunique()

        cantidad_eye_domiciliario       = df_cant_sku[df_cant_sku['CATEGORIA'] == 'EYE Domiciliario']['CATEGORIA'].value_counts().get('EYE Domiciliario', 0)
        cantidad_eye_no_domiciliario    = df_cant_sku[df_cant_sku['CATEGORIA'] == 'EYE No Domiciliario']['CATEGORIA'].value_counts().get('EYE No Domiciliario', 0)
        cantidad_raee                   = df_cant_sku[df_cant_sku['CATEGORIA'] == 'RAEE']['CATEGORIA'].value_counts().get('RAEE', 0)
        cantidad_aceite_lubricante      = df_cant_sku[df_cant_sku['CATEGORIA'] == 'Aceites y lubricantes']['CATEGORIA'].value_counts().get('Aceites y lubricantes', 0)
        cantidad_baterias               = df_cant_sku[df_cant_sku['CATEGORIA'] == 'Baterías']['CATEGORIA'].value_counts().get('Baterías', 0)
        cantidad_neumaticos             = df_cant_sku[df_cant_sku['CATEGORIA'] == 'Neumáticos']['CATEGORIA'].value_counts().get('Neumáticos', 0)
        cantidad_pilas                  = df_cant_sku[df_cant_sku['CATEGORIA'] == 'PILAS']['CATEGORIA'].value_counts().get('PILAS', 0) 
        
        if page == 0 :
            if self.image_parte_productos : self.image_parte_productos.release()
            self.congelar_parte_productos = True
            self.congelar_producto = False
            self.image = cv.VideoCapture(input_camara)


            self.actualizar_video_producto()

        if page == 1 :
            if self.image : self.image.release()
            self.congelar_producto = True
            self.congelar_parte_productos = False
            self.image_parte_productos = cv.VideoCapture(input_camara)
            self.actualizar_video_parte_producto()


        if page == 2:
            if self.image : self.image.release()
            if self.image_parte_productos : self.image_parte_productos.release()
            self.congelar_producto = True
            self.congelar_parte_productos = True
            self.eliminarTreeView()
            self.df = pd.read_csv("./CSVs/AnalisisFisico.csv", sep='|', dtype=str)
            self.mostrarDf(self.tree_view)

            if self.categoria_del_producto_input.get() == "EYE Domiciliario" : self.tipo_de_parte_input.current(0)
            else: self.tipo_de_parte_input.set('')


            if self.categoria_del_producto_input.get() != "EYE Domiciliario" and self.categoria_del_producto_input.get() != "EYE No domiciliario" : 
                self.categoría_eye_input.config(state="disabled")
                self.categoría_eye_label.configure(foreground="red")
                self.caracteristicas_eye_input.config(state="disabled")
                self.caracteristicas_eye_label.configure(foreground="red")
                self.definir_otro_input.config(state="disabled")
                self.definir_otro_label.configure(foreground="red")
                self.productos_por_envase_input.config(state="disabled")
                self.productos_por_envase_label.configure(foreground="red")
                self.tipo_de_parte_input.config(state="disabled")
                self.tipo_de_parte_label.configure(foreground="red")
                self.caract_reciclable_input.config(state="disabled")
                self.caract_reciclable_label.configure(foreground="red")
                self.caract_retornable_input.config(state="disabled")
                self.caract_retornable_label.configure(foreground="red")
                self.peligrosidad_input.config(state="disabled")
                self.peligrosidad_label.configure(foreground="red")
                self.caract_reciclable_input.set('')
                self.caract_retornable_input.set('')
                self.peligrosidad_input.set('')
            else:
                self.categoría_eye_input.config(state="normal")
                self.categoría_eye_label.configure(foreground="black")
                self.caracteristicas_eye_input.config(state="normal")
                self.caracteristicas_eye_label.configure(foreground="black")
                self.definir_otro_input.config(state="normal")
                self.definir_otro_label.configure(foreground="black")
                self.productos_por_envase_input.config(state="normal")
                self.productos_por_envase_label.configure(foreground="black")
                self.tipo_de_parte_input.config(state="normal")
                self.tipo_de_parte_label.configure(foreground="black")
                self.caract_reciclable_input.config(state="normal")
                self.caract_reciclable_label.configure(foreground="black")
                self.caract_retornable_input.config(state="normal")
                self.caract_retornable_label.configure(foreground="black")
                self.peligrosidad_input.config(state="normal")
                self.peligrosidad_label.configure(foreground="black")
                self.caract_reciclable_input.current(0)
                self.caract_retornable_input.current(0)
                self.peligrosidad_input.current(0)

            if self.categoria_del_producto_input.get() != "RAEE" : 
                self.categoria_raee_input.config(state="disabled", background="gray")
                self.categoria_raee_label.configure(foreground="red")
            else:
                self.categoria_raee_input.config(state="normal", background="white")
                self.categoria_raee_label.configure(foreground="black")
                self.categoria_raee_input.current(2)

            if self.categoria_del_producto_input.get() != "Aceites y lubricantes" : 
                self.categoria_aceites_input.config(state="disabled", background="gray")
                self.categoria_aceites_label.configure(foreground="red")
                self.cantidad_m_cubico_input.config(state="disabled", background="gray")
                self.cantidad_m_cubico_label.configure(foreground="red")
            else:
                self.categoria_aceites_input.config(state="normal", background="white")
                self.categoria_aceites_label.configure(foreground="black")
                self.cantidad_m_cubico_input.config(state="normal", background="white")
                self.cantidad_m_cubico_label.configure(foreground="black")

            if self.categoria_del_producto_input.get() != "Baterías" : 
                self.categoria_baterias_input.config(state="disabled", background="gray")
                self.categoria_baterias_label.configure(foreground="red")
            else:
                self.categoria_baterias_input.config(state="normal", background="white")
                self.categoria_baterias_label.configure(foreground="black")

            if self.categoria_del_producto_input.get() != "Neumáticos" : 
                self.categoria_neumatico_input.config(state="disabled", background="gray")
                self.categoria_neumatico_label.configure(foreground="red")
                self.cantidad_m_neumatico_input.config(state="disabled", background="gray")
                self.cantidad_m_neumatico_label.configure(foreground="red")
            else:
                self.categoria_neumatico_input.config(state="normal", background="white")
                self.categoria_neumatico_label.configure(foreground="black")
                self.cantidad_m_neumatico_input.config(state="normal", background="white")
                self.cantidad_m_neumatico_label.configure(foreground="black")

            if self.categoria_del_producto_input.get() != "PILAS" : 
                self.categoria_pilas_input.config(state="disabled", background="gray")
                self.categoria_pilas_label.configure(foreground="red")
                self.cantidad_m_pilas_input.config(state="disabled", background="gray")
                self.cantidad_m_pilas_label.configure(foreground="red")
            else:
                self.categoria_pilas_input.config(state="normal", background="white")
                self.categoria_pilas_label.configure(foreground="black")
                self.cantidad_m_pilas_input.config(state="normal", background="white")
                self.cantidad_m_pilas_label.configure(foreground="black")

        
        if page == 3:
            if self.image_parte_productos : self.image_parte_productos.release()
            self.congelar_parte_productos = True
            if self.image : self.image.release()
            self.congelar_producto = True

        if page == 5:
            
            self.mostrarDataSinergiaCSV(self.tree_view_data_sinergia)


        self.contador_sku_label.config(text='Contador SKU: '+str(cantidad_sku))
        self.contador_sku_label_partes_producto_label.config(text='Contador SKU: '+str(cantidad_sku))

        self.categoria_eye_domiciliario_label.config(text='Eye Domiciliario :  '+str(cantidad_eye_domiciliario))
        self.categoria_eye_no_domiciliario_label.config(text='Eye No Domiciliario :  '+str(cantidad_eye_no_domiciliario))
        self.categoria_raee.config(text='RAEE :  '+str(cantidad_raee))            
        self.categoria_aceite_y_lubricante.config(text='Aceite y Lubricantes :  '+str(cantidad_aceite_lubricante))     
        self.categoria_baterias.config(text='Baterías :  '+str(cantidad_baterias))                 
        self.categoria_neumaticos.config(text='Neumáticos :  '+str(cantidad_neumaticos))  
        self.pilas.config(text='Pilas :  '+str(cantidad_pilas))  

        print("Se cambió a la página:", page)

    def caprturarImagenServidor(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            frame = connection.last_frame
            nombre = self.ean_input.get()
            array_lista_nombres_producto.append(nombre+"("+str(len(array_lista_nombres_producto))+").jpg")
            cv.imwrite("Images/"+array_lista_nombres_producto[-1]+".jpg", frame)

            self.nombre_imagen_producto_label.config(text="|".join(array_lista_nombres_producto))

    def mostrarImagenServidor(self):
        cv.namedWindow('Pesa Grande')
        cv.setMouseCallback('Pesa Grande', self.caprturarImagenServidor)
        while True:
            frame = connection.last_frame
            if frame is not None:
                cv.imshow('Pesa Grande', frame)
                cv.waitKey(1)
                if self.congelar_video_servidor == True:
                    break
                if cv.getWindowProperty('Pesa Grande', cv.WND_PROP_VISIBLE) < 1:
                    break
        cv.destroyAllWindows()
    
    def actualizar_video_parte_producto(self):
        ret, frame = self.image_parte_productos.read()  # Leer un frame de la cámara
        if ret:
            # Convertir el frame de OpenCV a formato de imagen de PIL
            imagen = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            # Escalar la imagen para que se ajuste al tamaño del widget Label
            imagen = imagen.resize((640, 380))
            # Convertir la imagen de PIL a formato compatible con Tkinter
            imagen_tk = ImageTk.PhotoImage(imagen)
            # Actualizar el widget Label con la nueva imagen
            self.label_video_parte_productos.configure(image=imagen_tk)
            self.label_video_parte_productos.image = imagen_tk
        # Llamar a la función nuevamente después de un intervalo de tiempo (25 ms)
        if self.congelar_parte_productos == False :
            self.after(25, self.actualizar_video_parte_producto)
    
    def actualizar_video_producto(self):
        ret, frame = self.image.read()  # Leer un frame de la cámara
        if ret:
            # Convertir el frame de OpenCV a formato de imagen de PIL
            imagen = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            # Escalar la imagen para que se ajuste al tamaño del widget Label
            imagen = imagen.resize((640, 380))
            # Convertir la imagen de PIL a formato compatible con Tkinter
            imagen_tk = ImageTk.PhotoImage(imagen)
            # Actualizar el widget Label con la nueva imagen
            self.label_video.configure(image=imagen_tk)
            self.label_video.image = imagen_tk
        # Llamar a la función nuevamente después de un intervalo de tiempo (25 ms)
        if self.congelar_producto == False:
            self.after(25, self.actualizar_video_producto)

    def capturarImagen(self):
        ret, frame = self.image.read()
        nombre = self.ean_input.get()
        array_lista_nombres_producto.append(nombre+"("+str(len(array_lista_nombres_producto))+").jpg")
        cv.imwrite("Images/"+array_lista_nombres_producto[-1]+".jpg", frame)

        self.nombre_imagen_producto_label.config(text="|".join(array_lista_nombres_producto))

    def capturarImagenPartes(self):
        self.recapturar_imagen_parte_producto_button.config(state='normal')
        self.capturar_imagen_parte_producto_button.config(state="disable")
        nombre_producto = self.ean_input.get()
        nombre_parte = self.nombre_parte_producto_input.get()
        ret, frame = self.image_parte_productos.read()
        self.foto_parte = frame
        self.nombre_parte_producto_label.config(text= nombre_producto+"_parte_"+nombre_parte+".jpg")
        self.congelar_parte_productos = True

    def descongelarImagen(self):
        self.capturar_imagen_parte_producto_button.config(state="normal")
        self.recapturar_imagen_parte_producto_button.config(state='disable')
        self.congelar_parte_productos = False   
        self.actualizar_video_parte_producto()   
        
    def eliminarUltimaImagen(self):
        #========ELIMINAR ULTIMA FOTO TOMADA==========
        # DESCRIPCION
        # -----------
        # Funcion encargada de eliminar la ultima foto tomada.abs
        # Se elimina tanto en el Label que indica los nombres de las fotos
        # como en las imagenes guardadas
        
        if len(array_lista_nombres_producto) > 0:
            borrar = array_lista_nombres_producto.pop()
            self.nombre_imagen_producto_label.config(text="|".join(array_lista_nombres_producto)) #se cambia por pantalla

            os.remove("Images/"+borrar+".jpg")

    def mostrarDataSinergiaCSV(self, tree_view):
        items = tree_view.get_children()
        try:
            connection.desconectarServidor()
        except:
            pass
        for item in items:
            tree_view.delete(item)


        connection.conectarServidor()
        while connection.recived_csv is None:
            print("Esperando CSV...")
        df_serv = pd.DataFrame()
        df_serv = connection.recived_csv
        tree_view["column"] = list(df_serv.columns)
        tree_view["show"] = "headings"
        
        for column in tree_view["column"]:
            tree_view.heading(column, text=column)
        
        df_rows = df_serv.to_numpy().tolist()
        for row in df_rows:
            tree_view.insert("", "end", values=row)
        connection.desconectarServidor()      

    def mostrarDf(self, tree_view):
        #========MOSTRAR DATAFRAMA DEL CSV==========
        # DESCRIPCION
        # -----------
        # Muestra los resultados del csv en una tabla que fue convertida a un dataframe para se mostrada

        tree_view["column"] = list(self.df.columns)
        tree_view["show"] = "headings"
        
        for column in tree_view["column"]:
            tree_view.heading(column, text=column)
        
        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            tree_view.insert("", "end", values=row)

    def mostrarFiltrado(self):
        filtro = ''

        if (self.sku_filtro_input.get() != '' and self.ean_filtro_input.get() != '') or (self.sku_filtro_input.get() == '' and self.ean_filtro_input.get() == ''):
            print('NO PUEDEN ESTAR AMBOS VACIOS O AMBOS LLENOS') 
            filtro = ''
            return

        if self.sku_filtro_input.get() != '' : 
            filtro = 'SKU'
            self.df_filtrado = self.df[self.df[filtro] == self.sku_filtro_input.get()]
        if self.ean_filtro_input.get() != '' : 
            filtro = 'EAN'
            self.df_filtrado = self.df[self.df[filtro] == self.ean_filtro_input.get()]
    

        self.tree_view_duplicado_data_filtrada.delete(*self.tree_view_duplicado_data_filtrada.get_children())
        self.tree_view_duplicado_data_filtrada["column"] = list(self.df_filtrado.columns)
        self.tree_view_duplicado_data_filtrada["show"] = "headings"
        for column in self.tree_view_duplicado_data_filtrada["column"]:
            self.tree_view_duplicado_data_filtrada.heading(column, text=column)
        
        df_rows = self.df_filtrado.to_numpy().tolist()
        for row in df_rows:
            self.tree_view_duplicado_data_filtrada.insert("", "end", values=row)



        print(filtro)

    def otraParte(self):
        if self.validacionInputs():
            self.subirInformacion()

            self.nombre_parte_producto_input.delete(0, tk.END)
            self.nombre_parte_producto_input.insert(0, '')

            self.peso_parte_producto_input.delete(0, tk.END)
            self.peso_parte_producto_input.insert(0, '')

            self.categoria_del_producto_input.current(0)

            self.nombre_parte_producto_label.config(text='')

            self.capturar_imagen_parte_producto_button.config(state="normal")
            self.recapturar_imagen_parte_producto_button.config(state='disable')

            self.notebook.select(1)

    def otroProducto(self):
        if self.validacionInputs():
            self.subirInformacion()

            
            array_producto.clear()
            array_lista_nombres_producto.clear()

            self.sku_input.delete(0, tk.END)
            self.sku_input.insert(0, '')

            self.ean_input.delete(0, tk.END)
            self.ean_input.insert(0, '')

            self.descripcion_input.delete('1.0', tk.END)
            self.descripcion_input.insert('1.0', '')

            self.nombre_imagen_producto_label.config(text='')


            self.nombre_parte_producto_input.delete(0, tk.END)
            self.nombre_parte_producto_input.insert(0, '')

            self.peso_parte_producto_input.delete(0, tk.END)
            self.peso_parte_producto_input.insert(0, '')

            self.categoria_del_producto_input.current(0)

            self.nombre_parte_producto_label.config(text='')

            self.capturar_imagen_parte_producto_button.config(state="normal")
            self.recapturar_imagen_parte_producto_button.config(state='disable')

            self.notebook.select(0)

    def EliminarUltimoRegistro(self):
        self.eliminarTreeView()


        df = pd.read_csv('./CSVs/AnalisisFisico.csv', sep='|')
        ultimo_registro = df.tail(1)
        self.df = df.drop(df.index[-1])
        self.df.to_csv('./CSVs/AnalisisFisico.csv', sep='|', index=False)

        ultimo_registro = ultimo_registro.astype(str)
        data = ultimo_registro.values.tolist()
        connection.dropLastRecord(data)
        
        
        
        self.mostrarDf(self.tree_view)

    def eliminarTreeView(self) :
        items = self.tree_view.get_children()

        for item in items:
            self.tree_view.delete(item)

    def subirInformacion(self):
        nombre = self.ean_input.get()
        cv.imwrite("Images/"+nombre+"_parte_"+self.nombre_parte_producto_input.get()+".jpg", self.foto_parte )
        arrayInformacion = [
            self.sku_input.get(),
            self.ean_input.get(),
            self.descripcion_input.get("1.0", "end-1c"),
            ' , '.join(array_lista_nombres_producto),
            self.nombre_parte_producto_input.get(),
            self.peso_parte_producto_input.get(),
            self.categoria_del_producto_input.get(),
            self.nombre_parte_producto_label.cget("text"),
            self.categoría_eye_input.get(),
            self.caracteristicas_eye_input.get(),
            self.definir_otro_input.get(),
            self.productos_por_envase_input.get(),
            self.tipo_de_parte_input.get(),
            self.peligrosidad_input.get(),
            self.caract_reciclable_input.get(),
            self.caract_retornable_input.get(),
            self.categoria_raee_input.get(),
            self.categoria_aceites_input.get(),
            self.categoria_baterias_input.get(),
            self.categoria_neumatico_input.get(),
            self.cantidad_m_neumatico_input.get(),
            self.categoria_pilas_input.get(),
            self.cantidad_m_pilas_input.get()
        ]

        df = pd.DataFrame(
                    [arrayInformacion],
                    columns=[
                            "SKU",
                            "EAN",
                            "DESCRIPCION",
                            "NOMBRE IMAGEN PRODUCTO",
                            "PARTE",
                            "PESO INFORMADO",
                            "CATEGORIA",
                            "NOMBRE IMAGEN PARTE",
                            "CATEGORIA EYE",
                            "CARACTERISTICAS EYE",
                            "DEFINIR OTRO",
                            "PRODUCTO POR ENVASE",
                            "TIPO DE PARTE",
                            "CARACTERISTICAS RECICLABLES",
                            "CARACTERISTICAS RETORNABLE",
                            "PELIGROSIDAD",
                            "CATEGORIA RAEE",
                            "CATEGORIA ACEITE",
                            "CATEGORIA BATERIA",
                            "CATEGORIA NEUMATICO",
                            "CANTIDAD NEUMATICOS",
                            "CATEGORIA PILA",
                            "CANTIDAD DE PILAS",
                            ]
                )
        #Subido de forma local
        df.to_csv('./CSVs/AnalisisFisico.csv', sep='|',   mode='a', header=False, index=False) 

        #Subido al servidor
        df = df.astype(str)
        data = df.values.tolist()
        connection.sendRecords(data)

    def validacionInputs(self):
        flag = True
        errores = []

        if self.sku_input.get() == '' : 
            print('falta sku')
            errores.append('SKU')
            flag = False

        if self.ean_input.get() == '' :
            print('falta ean')
            errores.append('EAN')
            flag = False

        if len(array_lista_nombres_producto) == 0 :
            print('falta sacar foto al prodcto')
            errores.append('FOTO PRODUCTO')
            flag = False

        if self.nombre_parte_producto_input.get() == '':
            print('falta colocar a el nombre de la parte')
            errores.append('NOMBRE DE LA PARTE')
            flag = False

        if self.peso_parte_producto_input.get() == '':
            print('falta peso')
            errores.append('PESO')
            flag = False

        if self.nombre_parte_producto_label.cget("text") == '':
            print('falta sacar foto a la parte del producto')
            errores.append('FOTO PARTE DEL PRODUCTO')
            flag = False

        if flag == False:
            messagebox.showinfo(message='Faltan los siguientes requerimientos: '+', '.join(errores), title='ADVERTENCIA')

        return flag

    def duplicarData(self):
        if (self.sku_filtro_input.get() != '' and self.ean_filtro_input.get() != '') or (self.sku_filtro_input.get() == '' and self.ean_filtro_input.get() == ''):
            print('NO PUEDEN ESTAR AMBOS VACIOS O AMBOS LLENOS') 
            return
        
        if self.nuevo_nombre_producto_filtrado_input.get() == '' or self.nuevo_nombre_producto_filtrado_input.get() == '' or self.nuevo_ean_filtrado_input.get() == '':
            print('NO PUEDEN HABER CAMPOS VACIOS') 
            return

        self.sacarIMagenesProducto()
        self.df_filtrado['SKU'] = self.nuevo_sku_filtrado_input.get()
        self.df_filtrado['EAN'] = self.nuevo_ean_filtrado_input.get()
        self.df_filtrado['NOMBRE IMAGEN PRODUCTO'] = ' , '.join(self.lista_nombres_fotos_producto_duplicados)
        #Subido de forma local
        self.df_filtrado.to_csv('./CSVs/AnalisisFisico.csv',  mode='a', sep='|' , header=False, index=False) 

        #Subido al servidor
        self.df_filtrado = self.df_filtrado.astype(str)
        data = self.df_filtrado.values.tolist()
        connection.sendRecords(data=data)

        self.tree_view_duplicado_data_filtrada.delete(*self.tree_view_duplicado_data_filtrada.get_children())
        self.sku_filtro_input.delete(0, tk.END)
        self.sku_filtro_input.insert(0, '')

        self.ean_filtro_input.delete(0, tk.END)
        self.ean_filtro_input.insert(0, '')

        self.nuevo_sku_filtrado_input.delete(0, tk.END)
        self.nuevo_sku_filtrado_input.insert(0, '')

        self.nuevo_ean_filtrado_input.delete(0, tk.END)
        self.nuevo_ean_filtrado_input.insert(0, '')

        self.nuevo_nombre_producto_filtrado_input.delete(0, tk.END)
        self.nuevo_nombre_producto_filtrado_input.insert(0, '')

        self.tree_view_duplicado_data.delete(*self.tree_view_duplicado_data.get_children())
        self.mostrarDf(self.tree_view_duplicado_data)

    def traerRegistro(self):
        self.registro =  pd.DataFrame
        ean = self.traer_un_registro_ean.get()
        if ean == '': return
        
        df = pd.read_csv("./CSVs/AnalisisFisico.csv", sep='|', dtype=str)
        self.registro = df.loc[df['EAN'] == ean].head(1)
        self.registro.index = [0]


        if len(self.registro) == 0 : return

        self.traer_un_registro_button.config(state='disable')
        self.subir_un_registro_button.config(state='normal')
        self.otra_parte_button.config(state='disable')
        self.otra_producto_button.config(state='disable')
        self.eliminar_ultimo_button.config(state='disable')

        self.capturar_imagen_button.config(state='disable')
        self.eliminar_ultima_imagen_button.config(state='disable')

        self.capturar_imagen_parte_producto_button.config(state='normal')
        self.recapturar_imagen_parte_producto_button.config(state='disable')

        self.sku_input.delete(0, tk.END)
        self.sku_input.insert(0, self.registro['SKU'].values[0])
        
        self.ean_input.delete(0, tk.END)
        self.ean_input.insert(0, self.registro['EAN'].values[0])
        
        self.descripcion_input.delete('1.0', tk.END)
        self.descripcion_input.insert('1.0', self.registro['DESCRIPCION'].values[0])
        
        self.nombre_parte_producto_input.delete(0, tk.END)
        self.nombre_parte_producto_input.insert(0, self.registro['PARTE'].values[0])
        
        self.peso_parte_producto_input.delete(0, tk.END)
        self.peso_parte_producto_input.insert(0, self.registro['PESO INFORMADO'].values[0])
        
        self.categoria_del_producto_input.delete(0, tk.END)
        self.categoria_del_producto_input.insert(0, self.registro['CATEGORIA'].values[0])
        
        self.categoría_eye_input.delete(0, tk.END)
        self.categoría_eye_input.insert(0,  self.registro['CARACTERISTICAS EYE'].values[0])

        self.caracteristicas_eye_input.delete(0, tk.END)
        self.caracteristicas_eye_input.insert(0, self.registro['CARACTERISTICAS EYE'].values[0])

        self.definir_otro_input.delete(0, tk.END)
        self.definir_otro_input.insert(0, self.registro['DEFINIR OTRO'].values[0])

        self.productos_por_envase_input.delete(0, tk.END)
        self.productos_por_envase_input.insert(0, self.registro['PRODUCTO POR ENVASE'].values[0])

        self.tipo_de_parte_input.delete(0, tk.END)
        self.tipo_de_parte_input.insert(0, self.registro['TIPO DE PARTE'].values[0])

        self.peligrosidad_input.delete(0, tk.END)
        self.peligrosidad_input.insert(0, self.registro['PELIGROSIDAD'].values[0])

        self.caract_reciclable_input.delete(0, tk.END)
        self.caract_reciclable_input.insert(0, self.registro['CARACTERISTICAS RECICLABLES'].values[0])

        self.caract_retornable_input.delete(0, tk.END)
        self.caract_retornable_input.insert(0, self.registro['CARACTERISTICAS RETORNABLE'].values[0])

        self.categoria_raee_input.delete(0, tk.END)
        self.categoria_raee_input.insert(0, self.registro['CATEGORIA RAEE'].values[0])

        self.categoria_aceites_input.delete(0, tk.END)
        self.categoria_aceites_input.insert(0, self.registro['CATEGORIA ACEITE'].values[0])

        self.categoria_baterias_input.delete(0, tk.END)
        self.categoria_baterias_input.insert(0, self.registro['CATEGORIA BATERIA'].values[0])

        self.categoria_neumatico_input.delete(0, tk.END)
        self.categoria_neumatico_input.insert(0, self.registro['CATEGORIA NEUMATICO'].values[0])

        self.cantidad_m_neumatico_input.delete(0, tk.END)
        self.cantidad_m_neumatico_input.insert(0, self.registro['CANTIDAD NEUMATICOS'].values[0])

        self.categoria_pilas_input.delete(0, tk.END)
        self.categoria_pilas_input.insert(0, self.registro['CATEGORIA PILA'].values[0])

        self.cantidad_m_pilas_input.delete(0, tk.END)
        self.cantidad_m_pilas_input.insert(0, self.registro['CANTIDAD DE PILAS'].values[0])

        
     

        print(registro['SKU'].values[0])

    def subirRegistro(self):
        self.traer_un_registro_button.config(state='normal')
        self.subir_un_registro_button.config(state='disable')
        self.otra_parte_button.config(state='normal')
        self.otra_producto_button.config(state='normal')
        self.eliminar_ultimo_button.config(state='normal')
        self.capturar_imagen_button.config(state='normal')
        self.eliminar_ultima_imagen_button.config(state='normal')
        
        self.traer_un_registro_ean.delete(0, tk.END)
        self.traer_un_registro_ean.insert(0, '')


        self.registro.loc[0,'SKU'] = self.sku_input.get()
        self.registro.loc[0,'EAN'] = self.ean_input.get()
        self.registro.loc[0,'DESCRIPCION'] = self.descripcion_input.get('1.0', tk.END).rstrip()
        self.registro.loc[0,'PARTE'] = self.nombre_parte_producto_input.get()
        self.registro.loc[0,'PESO INFORMADO'] = self.peso_parte_producto_input.get()
        self.registro.loc[0,'CATEGORIA'] = self.categoria_del_producto_input.get()
        self.registro.loc[0,'CARACTERISTICAS EYE'] = self.categoría_eye_input.get()
        self.registro.loc[0,'CARACTERISTICAS EYE'] = self.caracteristicas_eye_input.get()
        self.registro.loc[0,'DEFINIR OTRO'] = self.definir_otro_input.get()
        self.registro.loc[0,'PRODUCTO POR ENVASE'] = self.productos_por_envase_input.get()
        self.registro.loc[0,'TIPO DE PARTE'] = self.tipo_de_parte_input.get()
        self.registro.loc[0,'PELIGROSIDAD'] = self.peligrosidad_input.get()
        self.registro.loc[0,'CARACTERISTICAS RECICLABLES'] = self.caract_reciclable_input.get()
        self.registro.loc[0,'CARACTERISTICAS RETORNABLE'] = self.caract_retornable_input.get()
        self.registro.loc[0,'CATEGORIA RAEE'] = self.categoria_raee_input.get()
        self.registro.loc[0,'CATEGORIA ACEITE'] = self.categoria_aceites_input.get()
        self.registro.loc[0,'CATEGORIA BATERIA'] = self.categoria_baterias_input.get()
        self.registro.loc[0,'CATEGORIA NEUMATICO'] = self.categoria_neumatico_input.get()
        self.registro.loc[0,'CANTIDAD NEUMATICOS'] = self.cantidad_m_neumatico_input.get()
        self.registro.loc[0,'CATEGORIA PILA'] = self.categoria_pilas_input.get()
        self.registro.loc[0,'CANTIDAD DE PILAS'] = self.cantidad_m_pilas_input.get()
        self.registro.loc[0,'NOMBRE IMAGEN PARTE'] = self.nombre_parte_producto_input.get()

        nombre = self.ean_input.get()
        cv.imwrite("Images/"+nombre+"_parte_"+self.nombre_parte_producto_input.get()+".jpg", self.foto_parte )
        #Subido de forma local
        self.registro.to_csv('./CSVs/AnalisisFisico.csv', sep='|',   mode='a', header=False, index=False) 

        #Subido al servidor
        self.registro = self.registro.astype(str)
        data = self.registro.values.tolist()
        connection.sendRecords(data)

        print(self.registro)
 
    def sacarIMagenesProducto(self):
        self.lista_fotos_producto_duplicados.clear()
        while 1: 

            frame  = self.captureImageDuplicado("Producto")
            self.lista_fotos_producto_duplicados.append(frame)

            respuesta = mesagebox.askquestion("FOTO PRODUCTO", "¿Deseas seguir sacando fotos?")
            print(respuesta)
            if respuesta == 'no':
                break
        self.lista_nombres_fotos_producto_duplicados.clear()
        i = 0
        for foto in self.lista_fotos_producto_duplicados :
            cv.imwrite('Images/'+self.nuevo_nombre_producto_filtrado_input.get() + '('+str(i)+').jpg', foto)
            self.lista_nombres_fotos_producto_duplicados.append(self.nuevo_nombre_producto_filtrado_input.get() + '('+str(i)+').jpg')
            i+=1
                   
    def captureImageDuplicado(self,nombreProducto):
        #========ESTRUCTURA GRAFICA==========
        # DESCRIPCION
        # -----------
        # Encargado de de actualizar los fotogramas del video que se muestra por pantalla y guardar el ultimo
        # frame una vez que se hace click encima.

        global loop 
        loop = True
        cap = cv.VideoCapture(input_camara)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            print("----")
            exit()

        cv.namedWindow(nombreProducto)

        while loop:
            ret, frame = cap.read()

            if not ret :
                print("no se recibe nada")

            #cv.resize(frame, (1920, 1080 ))
            cv.imshow(nombreProducto, frame)
            cv.setMouseCallback(nombreProducto, self.click_event) 
            cv.setWindowProperty(nombreProducto, cv.WND_PROP_TOPMOST, 1)


            if cv.waitKey(1) == ord('q') or cv.waitKey(1) == chr(27): 
                break
        
        cap.release()
        cv.destroyAllWindows()
        return frame

    def click_event(self, event, x, y, flags, param):
        #========ESTRUCTURA GRAFICA==========
        # DESCRIPCION
        # -----------
        # Encargado de campturar la accion click sobre el video que se muestra en pantall para sacar el ultimo frame.

        if event == cv.EVENT_LBUTTONDOWN:
            global loop 
            loop = False
        
    def subirAWS(self):
        aws = Aws()
        path    = './CSVs/AnalisisFisico.csv'
        bucket  = 'analisis-fisico' 
        object_name = self.nombrecsv_aws_input.get()+'('+nombre_notebook+').csv'
        if aws.upload_file(path, bucket, object_name) == False : messagebox.showinfo(message='NO se pudo subir el archivo csv', title='Infomración')
        else:
            self.create_zip('./Images', './ZIP/fotos.zip')
            path        = './ZIP/fotos.zip'
            object_name = self.nombrecsv_aws_input.get()+'('+nombre_notebook+').zip'
            if aws.upload_file(path, bucket, object_name) == False : messagebox.showinfo(message='NO se pudo subir el archivo zip', title='Infomración')
            else: 
                self.nombrecsv_aws_input.delete(0, tk.END)
                self.nombrecsv_aws_input.insert(0, '')
                messagebox.showinfo(message='Los archivos se subieron exitosamente!!', title='Infomración')

    def create_zip(self, folder_path, zip_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))
    


#-------------------------- 


# def sendDataCSVServer():
#     data =[
#         ['prueba 22','asd','ads','asdasd(0).jpg','asd','asd','Aceites y lubricantes','asdasd_parte_asd.jpg','','','','','','Sin material reciclado','No Retornable','Residuo NO Peligroso','','Aceites Lubricantes No Recuperables','','','','',''],
#         ['prueba 22','asd','ads','asdasd(0).jpg','asd','asd','Aceites y lubricantes','asdasd_parte_asd.jpg','','','','','','Sin material reciclado','No Retornable','Residuo NO Peligroso','','Aceites Lubricantes No Recuperables','','','','','']
#     ]
#     aux = pd.DataFrame(data)
#     data = aux.values.tolist()
#     connection.sendRecords(data)


# sendDataCSVServer()

#===========================
#===========MAIN============
#===========================
array_producto = []
array_lista_nombres_producto = []
array_categoria_partes_producto = []
array_partes_producto = []
array_df = []

page = 0


try:
    connection.desconectarServidor()
except:
    pass

ventana_princiapl = tk.Tk()
producto = Producto(master=ventana_princiapl)
ventana_princiapl.mainloop()

