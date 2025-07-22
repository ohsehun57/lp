import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk
import re
import json
import os
from datetime import datetime

class Estudiante:
    def __init__(self, id, nombre, apellidos, edad, carrera, email="", telefono=""):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = edad
        self.carrera = carrera
        self.email = email
        self.telefono = telefono
        self.notas = {}  # Diccionario {curso: nota}
        self.fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def agregar_nota(self, curso, nota):
        self.notas[curso] = nota
    
    def eliminar_nota(self, curso):
        if curso in self.notas:
            del self.notas[curso]
    
    def calcular_promedio(self):
        if not self.notas:
            return 0
        return sum(self.notas.values()) / len(self.notas)
    
    def esta_aprobado(self):
        return self.calcular_promedio() >= 10.5
    
    def mostrar_informacion(self):
        promedio = self.calcular_promedio()
        notas_str = ", ".join([f"{curso}: {nota}" for curso, nota in self.notas.items()])
        
        return (f"ID: {self.id}\n"
                f"Nombre completo: {self.nombre} {self.apellidos}\n"
                f"Edad: {self.edad} años\n"
                f"Carrera: {self.carrera}\n"
                f"Email: {self.email}\n"
                f"Teléfono: {self.telefono}\n"
                f"Notas: {notas_str if notas_str else 'Sin notas registradas'}\n"
                f"Promedio: {round(promedio, 2)}\n"
                f"Estado: {'Aprobado' if self.esta_aprobado() else 'Desaprobado'}\n"
                f"Fecha de registro: {self.fecha_registro}")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'edad': self.edad,
            'carrera': self.carrera,
            'email': self.email,
            'telefono': self.telefono,
            'notas': self.notas,
            'fecha_registro': self.fecha_registro
        }
    
    @classmethod
    def from_dict(cls, data):
        estudiante = cls(
            data['id'],
            data['nombre'],
            data['apellidos'],
            data['edad'],
            data['carrera'],
            data['email'],
            data['telefono']
        )
        estudiante.notas = data['notas']
        estudiante.fecha_registro = data['fecha_registro']
        return estudiante


class GestorEstudiantes:
    def __init__(self):
        self.estudiantes = []
        self.contador_id = 1
        self.archivo_datos = "estudiantes_data.json"
        self.cargar_datos()
    
    def generar_id(self):
        id_generado = self.contador_id
        self.contador_id += 1
        return id_generado
    
    def agregar_estudiante(self, nombre, apellidos, edad, carrera, email="", telefono=""):
        id_estudiante = self.generar_id()
        estudiante = Estudiante(id_estudiante, nombre, apellidos, edad, carrera, email, telefono)
        self.estudiantes.append(estudiante)
        self.guardar_datos()
        return estudiante
    
    def eliminar_estudiante(self, id_estudiante):
        for i, estudiante in enumerate(self.estudiantes):
            if estudiante.id == id_estudiante:
                del self.estudiantes[i]
                self.guardar_datos()
                return True
        return False
    
    def buscar_estudiante(self, termino):
        resultados = []
        termino = termino.lower()
        for estudiante in self.estudiantes:
            if (termino in estudiante.nombre.lower() or 
                termino in estudiante.apellidos.lower() or
                termino in estudiante.carrera.lower() or
                termino in str(estudiante.id)):
                resultados.append(estudiante)
        return resultados
    
    def obtener_estudiante_por_id(self, id_estudiante):
        for estudiante in self.estudiantes:
            if estudiante.id == id_estudiante:
                return estudiante
        return None
    
    def guardar_datos(self):
        data = [estudiante.to_dict() for estudiante in self.estudiantes]
        with open(self.archivo_datos, 'w') as f:
            json.dump(data, f, indent=4)
    
    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r') as f:
                    data = json.load(f)
                
                self.estudiantes = [Estudiante.from_dict(item) for item in data]
                
                # Actualizar contador de ID al máximo + 1
                if self.estudiantes:
                    max_id = max(estudiante.id for estudiante in self.estudiantes)
                    self.contador_id = max_id + 1
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def ordenar_estudiantes(self, criterio, ascendente=True):
        if criterio == "nombre":
            self.estudiantes.sort(key=lambda e: e.nombre.lower(), reverse=not ascendente)
        elif criterio == "apellidos":
            self.estudiantes.sort(key=lambda e: e.apellidos.lower(), reverse=not ascendente)
        elif criterio == "edad":
            self.estudiantes.sort(key=lambda e: e.edad, reverse=not ascendente)
        elif criterio == "promedio":
            self.estudiantes.sort(key=lambda e: e.calcular_promedio(), reverse=not ascendente)
        elif criterio == "carrera":
            self.estudiantes.sort(key=lambda e: e.carrera.lower(), reverse=not ascendente)
        elif criterio == "id":
            self.estudiantes.sort(key=lambda e: e.id, reverse=not ascendente)
        return self.estudiantes


class SistemaGestionEstudiantes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Académica")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Icono de la aplicación (opcional)
        # self.root.iconbitmap("icono.ico")
        
        self.gestor = GestorEstudiantes()
        self.estudiante_seleccionado = None
        
        self.setup_ui()
        self.cargar_lista_estudiantes()
    
    def setup_ui(self):
        # Estilo y tema
        style = ttk.Style()
        style.configure("TButton", font=('Arial', 10))
        style.configure("TLabel", font=('Arial', 10))
        style.configure("TEntry", font=('Arial', 10))
        style.configure("Heading.TLabel", font=('Arial', 12, 'bold'))
        style.configure("Title.TLabel", font=('Arial', 16, 'bold'))
        
        # Marco principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título del sistema
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = ttk.Label(self.title_frame, text="SISTEMA DE GESTIÓN ACADÉMICA", style="Title.TLabel")
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        # Botón de información
        self.info_button = ttk.Button(self.title_frame, text="ℹ️ Acerca de", command=self.mostrar_acerca_de)
        self.info_button.pack(side=tk.RIGHT, padx=5)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Registro y Lista
        self.tab_registro = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_registro, text="Registro y Lista")
        
        # Tab 2: Notas y Calificaciones
        self.tab_notas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_notas, text="Notas y Calificaciones")
        
        # Tab 3: Estadísticas
        self.tab_estadisticas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_estadisticas, text="Estadísticas")
        
        # Configurar las pestañas
        self.setup_tab_registro()
        self.setup_tab_notas()
        self.setup_tab_estadisticas()
        
        # Barra de estado
        self.statusbar = ttk.Label(self.main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_tab_registro(self):
        # Dividir en dos paneles
        self.panel_frame = ttk.PanedWindow(self.tab_registro, orient=tk.HORIZONTAL)
        self.panel_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Formulario
        self.form_frame = ttk.LabelFrame(self.panel_frame, text="Registro de Estudiante", padding=10)
        self.panel_frame.add(self.form_frame, weight=40)
        
        # Formulario de registro
        ttk.Label(self.form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(self.form_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.form_frame, text="Apellidos:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_apellidos = ttk.Entry(self.form_frame, width=30)
        self.entry_apellidos.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.form_frame, text="Edad:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_edad = ttk.Entry(self.form_frame, width=10)
        self.entry_edad.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.form_frame, text="Carrera:").grid(row=3, column=0, sticky=tk.W, pady=5)
        # Lista predefinida de carreras
        carreras = ["", "Ingeniería Informática", "Ingeniería Civil", "Medicina", "Derecho", 
                   "Administración", "Contabilidad", "Psicología", "Arquitectura", "Otra"]
        self.combo_carrera = ttk.Combobox(self.form_frame, values=carreras, width=28)
        self.combo_carrera.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.form_frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_email = ttk.Entry(self.form_frame, width=30)
        self.entry_email.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.form_frame, text="Teléfono:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_telefono = ttk.Entry(self.form_frame, width=20)
        self.entry_telefono.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botones de acción
        self.button_frame = ttk.Frame(self.form_frame)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.btn_agregar = ttk.Button(self.button_frame, text="Registrar Estudiante", command=self.registrar_estudiante)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(self.button_frame, text="Limpiar Campos", command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(self.button_frame, text="Eliminar Estudiante", command=self.eliminar_estudiante, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        # Panel derecho - Lista de estudiantes
        self.list_frame = ttk.LabelFrame(self.panel_frame, text="Lista de Estudiantes", padding=10)
        self.panel_frame.add(self.list_frame, weight=60)
        
        # Barra de búsqueda
        self.search_frame = ttk.Frame(self.list_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_buscar = ttk.Entry(self.search_frame, width=30)
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_buscar.bind("<KeyRelease>", self.buscar_estudiantes)
        
        # Opciones de ordenamiento
        ttk.Label(self.search_frame, text="Ordenar por:").pack(side=tk.LEFT, padx=(10, 5))
        self.combo_ordenar = ttk.Combobox(self.search_frame, width=15, 
                                         values=["ID", "Nombre", "Apellidos", "Edad", "Carrera", "Promedio"])
        self.combo_ordenar.pack(side=tk.LEFT, padx=(0, 5))
        self.combo_ordenar.set("ID")
        self.combo_ordenar.bind("<<ComboboxSelected>>", self.ordenar_lista)
        
        # Treeview para la lista de estudiantes
        self.tree_frame = ttk.Frame(self.list_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("id", "nombre", "apellidos", "edad", "carrera", "promedio")
        self.tree_estudiantes = ttk.Treeview(self.tree_frame, columns=columns, show="headings", 
                                         selectmode="browse", yscrollcommand=self.tree_scroll.set)
        
        # Configurar columnas
        self.tree_estudiantes.heading("id", text="ID")
        self.tree_estudiantes.heading("nombre", text="Nombre")
        self.tree_estudiantes.heading("apellidos", text="Apellidos")
        self.tree_estudiantes.heading("edad", text="Edad")
        self.tree_estudiantes.heading("carrera", text="Carrera")
        self.tree_estudiantes.heading("promedio", text="Promedio")
        
        self.tree_estudiantes.column("id", width=50, anchor=tk.CENTER)
        self.tree_estudiantes.column("nombre", width=120)
        self.tree_estudiantes.column("apellidos", width=120)
        self.tree_estudiantes.column("edad", width=50, anchor=tk.CENTER)
        self.tree_estudiantes.column("carrera", width=150)
        self.tree_estudiantes.column("promedio", width=70, anchor=tk.CENTER)
        
        self.tree_estudiantes.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.tree_estudiantes.yview)
        
        # Asignar evento de selección
        self.tree_estudiantes.bind("<<TreeviewSelect>>", self.seleccionar_estudiante)
        
        # Detalles del estudiante seleccionado
        self.detalle_frame = ttk.LabelFrame(self.list_frame, text="Detalle del Estudiante")
        self.detalle_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.detalle_texto = tk.Text(self.detalle_frame, height=8, width=50, wrap=tk.WORD, font=('Arial', 9))
        self.detalle_texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detalle_texto.config(state=tk.DISABLED)
    
    def setup_tab_notas(self):
        # Panel principal
        self.notas_frame = ttk.Frame(self.tab_notas)
        self.notas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Selección de estudiante
        self.notas_izq_frame = ttk.LabelFrame(self.notas_frame, text="Seleccionar Estudiante", padding=10)
        self.notas_izq_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), expand=False)
        
        # Listbox para seleccionar estudiante
        self.notas_search_frame = ttk.Frame(self.notas_izq_frame)
        self.notas_search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(self.notas_search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_buscar_notas = ttk.Entry(self.notas_search_frame, width=20)
        self.entry_buscar_notas.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_buscar_notas.bind("<KeyRelease>", self.actualizar_lista_notas)
        
        self.listbox_frame = ttk.Frame(self.notas_izq_frame)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.listbox_scroll = ttk.Scrollbar(self.listbox_frame)
        self.listbox_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_estudiantes = tk.Listbox(self.listbox_frame, width=30, selectmode=tk.SINGLE, 
                                           yscrollcommand=self.listbox_scroll.set)
        self.listbox_estudiantes.pack(fill=tk.BOTH, expand=True)
        self.listbox_scroll.config(command=self.listbox_estudiantes.yview)
        
        self.listbox_estudiantes.bind("<<ListboxSelect>>", self.seleccionar_estudiante_notas)
        
        # Panel derecho - Gestión de notas
        self.notas_der_frame = ttk.LabelFrame(self.notas_frame, text="Gestión de Notas", padding=10)
        self.notas_der_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Información del estudiante seleccionado
        self.estudiante_info_frame = ttk.Frame(self.notas_der_frame)
        self.estudiante_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.estudiante_info_label = ttk.Label(self.estudiante_info_frame, text="Seleccione un estudiante", style="Heading.TLabel")
        self.estudiante_info_label.pack(side=tk.LEFT)
        
        # Formulario para agregar notas
        self.form_notas_frame = ttk.LabelFrame(self.notas_der_frame, text="Agregar Nota")
        self.form_notas_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.notas_form = ttk.Frame(self.form_notas_frame, padding=10)
        self.notas_form.pack(fill=tk.X)
        
        ttk.Label(self.notas_form, text="Curso:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.entry_curso = ttk.Entry(self.notas_form, width=30)
        self.entry_curso.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)
        
        ttk.Label(self.notas_form, text="Nota (0-20):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.entry_nota = ttk.Entry(self.notas_form, width=10)
        self.entry_nota.grid(row=0, column=3, padx=(0, 10), sticky=tk.W)
        
        self.btn_agregar_nota = ttk.Button(self.notas_form, text="Agregar Nota", 
                                         command=self.agregar_nota, state=tk.DISABLED)
        self.btn_agregar_nota.grid(row=0, column=4, padx=5)
        
        # Lista de notas
        self.lista_notas_frame = ttk.LabelFrame(self.notas_der_frame, text="Notas Registradas")
        self.lista_notas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para las notas
        self.notas_tree_frame = ttk.Frame(self.lista_notas_frame)
        self.notas_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notas_scroll = ttk.Scrollbar(self.notas_tree_frame)
        self.notas_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns_notas = ("curso", "nota", "estado")
        self.tree_notas = ttk.Treeview(self.notas_tree_frame, columns=columns_notas, 
                                     show="headings", yscrollcommand=self.notas_scroll.set)
        
        self.tree_notas.heading("curso", text="Curso")
        self.tree_notas.heading("nota", text="Nota")
        self.tree_notas.heading("estado", text="Estado")
        
        self.tree_notas.column("curso", width=200)
        self.tree_notas.column("nota", width=70, anchor=tk.CENTER)
        self.tree_notas.column("estado", width=100, anchor=tk.CENTER)
        
        self.tree_notas.pack(fill=tk.BOTH, expand=True)
        self.notas_scroll.config(command=self.tree_notas.yview)
        
        # Botones para gestionar notas
        self.btn_notas_frame = ttk.Frame(self.lista_notas_frame)
        self.btn_notas_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_eliminar_nota = ttk.Button(self.btn_notas_frame, text="Eliminar Nota Seleccionada", 
                                          command=self.eliminar_nota, state=tk.DISABLED)
        self.btn_eliminar_nota.pack(side=tk.LEFT, padx=5)
        
        # Resumen de rendimiento
        self.resumen_frame = ttk.LabelFrame(self.notas_der_frame, text="Resumen de Rendimiento")
        self.resumen_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.resumen_info = ttk.Label(self.resumen_frame, text="No hay datos disponibles", padding=10)
        self.resumen_info.pack(fill=tk.X)
    
    def setup_tab_estadisticas(self):
        # Panel principal de estadísticas
        self.estadisticas_frame = ttk.Frame(self.tab_estadisticas)
        self.estadisticas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior - Estadísticas generales
        self.stats_general_frame = ttk.LabelFrame(self.estadisticas_frame, text="Estadísticas Generales", padding=10)
        self.stats_general_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para estadísticas generales
        self.grid_stats = ttk.Frame(self.stats_general_frame)
        self.grid_stats.pack(fill=tk.X, padx=10, pady=5)
        
        # Contadores
        self.contador_frame = ttk.Frame(self.grid_stats)
        self.contador_frame.pack(fill=tk.X, pady=5)
        
        # Total de estudiantes
        self.total_frame = ttk.LabelFrame(self.contador_frame, text="Total Estudiantes")
        self.total_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.lbl_total_estudiantes = ttk.Label(self.total_frame, text="0", font=('Arial', 16, 'bold'))
        self.lbl_total_estudiantes.pack(pady=10)
        
        # Aprobados
        self.aprobados_frame = ttk.LabelFrame(self.contador_frame, text="Aprobados")
        self.aprobados_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.lbl_aprobados = ttk.Label(self.aprobados_frame, text="0", font=('Arial', 16, 'bold'))
        self.lbl_aprobados.pack(pady=10)
        
        # Desaprobados
        self.desaprobados_frame = ttk.LabelFrame(self.contador_frame, text="Desaprobados")
        self.desaprobados_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.lbl_desaprobados = ttk.Label(self.desaprobados_frame, text="0", font=('Arial', 16, 'bold'))
        self.lbl_desaprobados.pack(pady=10)
        
        # Promedio general
        self.promedio_frame = ttk.LabelFrame(self.estadisticas_frame, text="Promedio General", padding=10)
        self.promedio_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_promedio_general = ttk.Label(self.promedio_frame, text="Promedio general: 0.00", font=('Arial', 12))
        self.lbl_promedio_general.pack(pady=5)
        
        self.progress_promedio = ttk.Progressbar(self.promedio_frame, length=100, mode='determinate')
        self.progress_promedio.pack(fill=tk.X, pady=5)
        
        # Lista de los 5 mejores estudiantes
        self.mejores_frame = ttk.LabelFrame(self.estadisticas_frame, text="Mejores Promedios", padding=10)
        self.mejores_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview para los mejores estudiantes
        self.mejores_tree_frame = ttk.Frame(self.mejores_frame)
        self.mejores_tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns_mejores = ("posicion", "nombre", "carrera", "promedio")
        self.tree_mejores = ttk.Treeview(self.mejores_tree_frame, columns=columns_mejores, show="headings")
        
        self.tree_mejores.heading("posicion", text="#")
        self.tree_mejores.heading("nombre", text="Nombre Completo")
        self.tree_mejores.heading("carrera", text="Carrera")
        self.tree_mejores.heading("promedio", text="Promedio")
        
        self.tree_mejores.column("posicion", width=50, anchor=tk.CENTER)
        self.tree_mejores.column("nombre", width=200)
        self.tree_mejores.column("carrera", width=150)
        self.tree_mejores.column("promedio", width=100, anchor=tk.CENTER)
        
        self.tree_mejores.pack(fill=tk.BOTH, expand=True)
        
        # Botón para actualizar estadísticas
        self.btn_actualizar_stats = ttk.Button(self.estadisticas_frame, text="Actualizar Estadísticas", 
                                             command=self.actualizar_estadisticas)
        self.btn_actualizar_stats.pack