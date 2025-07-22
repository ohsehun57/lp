import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.notas = []
        self.fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def agregar_nota(self, nota):
        if 0 <= nota <= 20:
            self.notas.append(nota)
            return True
        return False
    
    def eliminar_nota(self, indice):
        if 0 <= indice < len(self.notas):
            self.notas.pop(indice)
            return True
        return False
    
    def editar_nota(self, indice, nueva_nota):
        if 0 <= indice < len(self.notas) and 0 <= nueva_nota <= 20:
            self.notas[indice] = nueva_nota
            return True
        return False
    
    def calcular_promedio(self):
        return sum(self.notas) / len(self.notas) if self.notas else 0
    
    def esta_aprobado(self):
        return self.calcular_promedio() >= 10.5
    
    def mostrar_informacion(self):
        promedio = self.calcular_promedio()
        aprobado = "Sí" if self.esta_aprobado() else "No"
        
        info = f"\nInformación del Estudiante\n"
        info += f"Nombre: {self.nombre}\n"
        info += f"Edad: {self.edad}\n"
        info += f"Carrera: {self.carrera}\n"
        info += f"Notas: {self.notas}\n"
        info += f"Promedio: {round(promedio, 2)}\n"
        info += f"Aprobado: {aprobado}\n"
        info += f"Fecha de registro: {self.fecha_registro}"
        
        return info

class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect('estudiantes.db')
        self.cursor = self.conexion.cursor()
        self.crear_tablas()
    
    def crear_tablas(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            carrera TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
        )
        ''')
        
        self.conexion.commit()
    
    def guardar_estudiante(self, estudiante):
        self.cursor.execute(
            "INSERT INTO estudiantes (nombre, edad, carrera, fecha_registro) VALUES (?, ?, ?, ?)",
            (estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.fecha_registro)
        )
        estudiante_id = self.cursor.lastrowid
        
        for nota in estudiante.notas:
            self.cursor.execute(
                "INSERT INTO notas (estudiante_id, valor) VALUES (?, ?)",
                (estudiante_id, nota)
            )
        
        self.conexion.commit()
        return estudiante_id
    
    def cargar_estudiantes(self):
        estudiantes = []
        self.cursor.execute("SELECT id, nombre, edad, carrera, fecha_registro FROM estudiantes")
        
        for est_row in self.cursor.fetchall():
            est_id, nombre, edad, carrera, fecha_registro = est_row
            estudiante = Estudiante(nombre, edad, carrera)
            estudiante.fecha_registro = fecha_registro
            
            self.cursor.execute("SELECT valor FROM notas WHERE estudiante_id = ?", (est_id,))
            for nota_row in self.cursor.fetchall():
                estudiante.notas.append(nota_row[0])
            
            estudiantes.append(estudiante)
        
        return estudiantes
    
    def cerrar(self):
        self.conexion.close()

class EstiloApp:
    def __init__(self, root):
        self.configurar_tema(root)
    
    def configurar_tema(self, root):
        # Configurar estilo global
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Colores
        color_primario = "#2c3e50"
        color_secundario = "#3498db"
        color_fondo = "#ecf0f1"
        color_texto = "#2c3e50"
        color_boton = "#3498db"
        color_boton_hover = "#2980b9"
        color_resaltar = "#e74c3c"
        
        # Configurar estilos específicos
        estilo.configure(".", 
                        font=("Segoe UI", 10),
                        background=color_fondo)
        
        estilo.configure("TFrame", background=color_fondo)
        estilo.configure("Header.TFrame", background=color_primario)
        
        estilo.configure("TLabel", 
                        background=color_fondo, 
                        foreground=color_texto)
        
        estilo.configure("Header.TLabel", 
                        background=color_primario, 
                        foreground="white",
                        font=("Segoe UI", 14, "bold"))
        
        estilo.configure("Title.TLabel", 
                        background=color_fondo, 
                        foreground=color_primario,
                        font=("Segoe UI", 12, "bold"))
        
        estilo.configure("TButton", 
                        background=color_boton, 
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))
        
        estilo.map("TButton", 
                background=[("active", color_boton_hover), ("pressed", color_boton_hover)])
        
        estilo.configure("Danger.TButton", 
                        background=color_resaltar)
        
        estilo.map("Danger.TButton", 
                background=[("active", "#c0392b"), ("pressed", "#c0392b")])
        
        estilo.configure("TEntry", 
                        background="white", 
                        foreground=color_texto,
                        fieldbackground="white")
        
        estilo.configure("Treeview", 
                        background="white", 
                        foreground=color_texto,
                        fieldbackground="white")
        
        estilo.map("Treeview", 
                background=[("selected", color_secundario)],
                foreground=[("selected", "white")])
        
        estilo.configure("Treeview.Heading", 
                        background=color_primario, 
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))
        
        # Configurar ventana principal
        root.configure(background=color_fondo)
        root.option_add("*TCombobox*Listbox*Background", "white")
        root.option_add("*TCombobox*Listbox*Foreground", color_texto)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Estudiantes")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Inicializar estilos
        self.estilo = EstiloApp(root)
        
        # Inicializar base de datos
        self.db = BaseDatos()
        
        # Lista de estudiantes
        self.lista_estudiantes = self.db.cargar_estudiantes()
        
        # Crear interfaz principal
        self.crear_interfaz()
        
        # Cargar estudiantes en la tabla
        self.actualizar_tabla_estudiantes()
    
    def crear_interfaz(self):
        # Panel principal con divisiones
        self.panel_principal = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (formulario y tabla de estudiantes)
        self.panel_izquierdo = ttk.Frame(self.panel_principal)
        self.panel_principal.add(self.panel_izquierdo, weight=3)
        
        # Panel derecho (detalles y estadísticas)
        self.panel_derecho = ttk.Frame(self.panel_principal)
        self.panel_principal.add(self.panel_derecho, weight=2)
        
        # Crear componentes de cada panel
        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
    
    def crear_panel_izquierdo(self):
        # Encabezado
        self.header_frame = ttk.Frame(self.panel_izquierdo, style="Header.TFrame")
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        self.header_label = ttk.Label(self.header_frame, 
                                     text="Sistema de Gestión Académica", 
                                     style="Header.TLabel")
        self.header_label.pack(padx=20, pady=10)
        
        # Frame para el formulario de registro
        self.frame_registro = ttk.LabelFrame(self.panel_izquierdo, text="Registro de Estudiante")
        self.frame_registro.pack(fill=tk.X, padx=10, pady=10)
        
        # Contenido del formulario en grid
        self.crear_formulario_registro()
        
        # Frame para la tabla de estudiantes
        self.frame_tabla = ttk.LabelFrame(self.panel_izquierdo, text="Lista de Estudiantes")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.crear_tabla_estudiantes()
        
        # Frame para botones de acción
        self.frame_acciones = ttk.Frame(self.panel_izquierdo)
        self.frame_acciones.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_ver_detalles = ttk.Button(self.frame_acciones, text="Ver Detalles", 
                                         command=self.mostrar_detalles_estudiante)
        self.btn_ver_detalles.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar", 
                                     style="Danger.TButton",
                                     command=self.eliminar_estudiante)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = ttk.Button(self.frame_acciones, text="Limpiar Selección", 
                                    command=self.limpiar_seleccion)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
    
    def crear_formulario_registro(self):
        frame_form = ttk.Frame(self.frame_registro)
        frame_form.pack(fill=tk.X, padx=10, pady=10)
        
        # Primera fila: Nombre y edad
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_nombre = ttk.Entry(frame_form, width=30)
        self.entrada_nombre.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(frame_form, text="Edad:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entrada_edad = ttk.Entry(frame_form, width=10)
        self.entrada_edad.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Segunda fila: Carrera
        ttk.Label(frame_form, text="Carrera:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Lista de carreras de ejemplo
        carreras = ["Ingeniería de Sistemas", "Ingeniería Civil", "Administración", 
                  "Contabilidad", "Medicina", "Derecho", "Psicología", "Otra"]
        
        self.combo_carrera = ttk.Combobox(frame_form, values=carreras, width=28)
        self.combo_carrera.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botón para agregar notas
        self.btn_agregar_notas = ttk.Button(frame_form, text="Agregar Notas", 
                                          command=self.agregar_notas)
        self.btn_agregar_notas.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Tercera fila: Notas y botón de registro
        self.label_notas = ttk.Label(frame_form, text="Notas: []")
        self.label_notas.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        
        self.btn_registrar = ttk.Button(frame_form, text="Registrar Estudiante", 
                                      command=self.registrar_estudiante)
        self.btn_registrar.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Inicializar notas temporales
        self.notas_temp = []
    
    def crear_tabla_estudiantes(self):
        # Frame para la tabla y scrollbar
        frame_tabla = ttk.Frame(self.frame_tabla)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar_y = ttk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tabla (Treeview)
        columnas = ("nombre", "edad", "carrera", "promedio", "estado")
        self.tabla_estudiantes = ttk.Treeview(frame_tabla, columns=columnas, 
                                            yscrollcommand=scrollbar_y.set,
                                            xscrollcommand=scrollbar_x.set)
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.tabla_estudiantes.yview)
        scrollbar_x.config(command=self.tabla_estudiantes.xview)
        
        # Configurar columnas
        self.tabla_estudiantes.column("#0", width=50, minwidth=50)
        self.tabla_estudiantes.column("nombre", width=200, minwidth=150)
        self.tabla_estudiantes.column("edad", width=80, minwidth=80)
        self.tabla_estudiantes.column("carrera", width=200, minwidth=150)
        self.tabla_estudiantes.column("promedio", width=100, minwidth=100)
        self.tabla_estudiantes.column("estado", width=100, minwidth=100)
        
        # Configurar encabezados
        self.tabla_estudiantes.heading("#0", text="ID", anchor=tk.W)
        self.tabla_estudiantes.heading("nombre", text="Nombre", anchor=tk.W)
        self.tabla_estudiantes.heading("edad", text="Edad", anchor=tk.W)
        self.tabla_estudiantes.heading("carrera", text="Carrera", anchor=tk.W)
        self.tabla_estudiantes.heading("promedio", text="Promedio", anchor=tk.W)
        self.tabla_estudiantes.heading("estado", text="Estado", anchor=tk.W)
        
        # Empaquetar tabla
        self.tabla_estudiantes.pack(fill=tk.BOTH, expand=True)
        
        # Evento de selección
        self.tabla_estudiantes.bind("<<TreeviewSelect>>", self.seleccionar_estudiante)
    
    def crear_panel_derecho(self):
        # Frame para detalles del estudiante
        self.frame_detalles = ttk.LabelFrame(self.panel_derecho, text="Detalles del Estudiante")
        self.frame_detalles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text widget para mostrar detalles
        self.text_detalles = tk.Text(self.frame_detalles, wrap=tk.WORD, height=10, 
                                   font=("Segoe UI", 10))
        self.text_detalles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_detalles.insert(tk.END, "Seleccione un estudiante para ver sus detalles.")
        self.text_detalles.config(state=tk.DISABLED)
        
        # Frame para gráficos
        self.frame_graficos = ttk.LabelFrame(self.panel_derecho, text="Estadísticas")
        self.frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para gráfico
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graficos)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inicializar gráfico
        self.actualizar_grafico_estadisticas()
    
    def agregar_notas(self):
        # Ventana para agregar notas
        self.ventana_notas = tk.Toplevel(self.root)
        self.ventana_notas.title("Agregar Notas")
        self.ventana_notas.geometry("400x400")
        self.ventana_notas.transient(self.root)
        self.ventana_notas.grab_set()
        
        # Frame para la cantidad de notas
        frame_cantidad = ttk.Frame(self.ventana_notas)
        frame_cantidad.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_cantidad, text="Cantidad de notas:").pack(side=tk.LEFT, padx=5)
        
        self.entrada_cantidad = ttk.Entry(frame_cantidad, width=5)
        self.entrada_cantidad.pack(side=tk.LEFT, padx=5)
        self.entrada_cantidad.insert(0, "1")
        
        btn_generar = ttk.Button(frame_cantidad, text="Generar campos", 
                               command=self.generar_campos_notas)
        btn_generar.pack(side=tk.LEFT, padx=5)
        
        # Frame para las entradas de notas
        self.frame_entradas_notas = ttk.Frame(self.ventana_notas)
        self.frame_entradas_notas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para botones
        frame_botones = ttk.Frame(self.ventana_notas)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        btn_aceptar = ttk.Button(frame_botones, text="Aceptar", 
                               command=self.guardar_notas_temp)
        btn_aceptar.pack(side=tk.RIGHT, padx=5)
        
        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", 
                                command=self.ventana_notas.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=5)
        
        # Si ya hay notas cargadas, mostrarlas
        if self.notas_temp:
            self.entrada_cantidad.delete(0, tk.END)
            self.entrada_cantidad.insert(0, str(len(self.notas_temp)))
            self.generar_campos_notas()
    
    def generar_campos_notas(self):
        # Limpiar frame de entradas
        for widget in self.frame_entradas_notas.winfo_children():
            widget.destroy()
        
        try:
            cantidad = max(1, min(20, int(self.entrada_cantidad.get())))
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de notas.")
            return
        
        # Scrollable frame para muchas notas
        canvas = tk.Canvas(self.frame_entradas_notas)
        scrollbar = ttk.Scrollbar(self.frame_entradas_notas, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Lista para almacenar las entradas
        self.entradas_notas = []
        
        # Crear entradas para cada nota
        for i in range(cantidad):
            frame_nota = ttk.Frame(scrollable_frame)
            frame_nota.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame_nota, text=f"Nota {i+1}:").pack(side=tk.LEFT, padx=5)
            
            entrada = ttk.Entry(frame_nota, width=10)
            entrada.pack(side=tk.LEFT, padx=5)
            
            # Si hay un valor previo, cargarlo
            if i < len(self.notas_temp):
                entrada.insert(0, str(self.notas_temp[i]))
            
            self.entradas_notas.append(entrada)
    
    def guardar_notas_temp(self):
        # Validar y guardar las notas
        notas = []
        for entrada in self.entradas_notas:
            try:
                nota = float(entrada.get())
                if 0 <= nota <= 20:
                    notas.append(nota)
                else:
                    messagebox.showerror("Error", "Las notas deben estar entre 0 y 20.")
                    return
            except ValueError:
                if entrada.get().strip():  # Solo mostrar error si hay algo escrito
                    messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
                    return
        
        # Guardar notas temporales
        self.notas_temp = notas
        
        # Actualizar etiqueta de notas
        self.label_notas.config(text=f"Notas: {[round(n, 2) for n in self.notas_temp]}")
        
        # Cerrar ventana
        self.ventana_notas.destroy()
    
    def registrar_estudiante(self):
        # Validar campos
        nombre = self.entrada_nombre.get().strip()
        carrera = self.combo_carrera.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar el nombre del estudiante.")
            return
        
        if not carrera:
            messagebox.showerror("Error", "Debe seleccionar una carrera.")
            return
        
        try:
            edad = int(self.entrada_edad.get())
            if edad <= 0:
                messagebox.showerror("Error", "La edad debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingrese una edad válida.")
            return
        
        # Crear estudiante
        estudiante = Estudiante(nombre, edad, carrera)
        
        # Agregar notas
        for nota in self.notas_temp:
            estudiante.agregar_nota(nota)
        
        # Guardar en base de datos
        self.db.guardar_estudiante(estudiante)
        
        # Agregar a la lista
        self.lista_estudiantes.append(estudiante)
        
        # Actualizar tabla
        self.actualizar_tabla_estudiantes()
        
        # Actualizar gráfico
        self.actualizar_grafico_estadisticas()
        
        # Limpiar formulario
        self.limpiar_formulario()
        
        # Mostrar mensaje
        messagebox.showinfo("Éxito", "Estudiante registrado correctamente.")
    
    def limpiar_formulario(self):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_edad.delete(0, tk.END)
        self.combo_carrera.set("")
        self.notas_temp = []
        self.label_notas.config(text="Notas: []")
    
    def actualizar_tabla_estudiantes(self):
        # Limpiar tabla
        for item in self.tabla_estudiantes.get_children():
            self.tabla_estudiantes.delete(item)
        
        # Agregar estudiantes a la tabla
        for i, estudiante in enumerate(self.lista_estudiantes):
            promedio = round(estudiante.calcular_promedio(), 2)
            estado = "Aprobado" if estudiante.esta_aprobado() else "Desaprobado"
            
            self.tabla_estudiantes.insert("", tk.END, text=str(i+1),
                                        values=(estudiante.nombre, estudiante.edad, 
                                               estudiante.carrera, promedio, estado))
    
    def seleccionar_estudiante(self, event):
        # Obtener ítem seleccionado
        seleccion = self.tabla_estudiantes.selection()
        if seleccion:
            # Obtener índice
            indice = int(self.tabla_estudiantes.item(seleccion[0], "text")) - 1
            
            # Mostrar detalles
            self.mostrar_detalles(indice)
    
    def mostrar_detalles(self, indice):
        if 0 <= indice < len(self.lista_estudiantes):
            estudiante = self.lista_estudiantes[indice]
            
            # Actualizar text widget
            self.text_detalles.config(state=tk.NORMAL)
            self.text_detalles.delete(1.0, tk.END)
            self.text_detalles.insert(tk.END, estudiante.mostrar_informacion())
            self.text_detalles.config(state=tk.DISABLED)
            
            # Actualizar gráfico de notas
            self.actualizar_grafico_notas(estudiante)
    
    def mostrar_detalles_estudiante(self):
        seleccion = self.tabla_estudiantes.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Seleccione un estudiante para ver sus detalles.")
            return
        
        indice = int(self.tabla_estudiantes.item(seleccion[0], "text")) - 1
        self.mostrar_detalles(indice)
    
    def eliminar_estudiante(self):
        seleccion = self.tabla_estudiantes.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Seleccione un estudiante para eliminar.")
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?"):
            return
        
        indice = int(self.tabla_estudiantes.item(seleccion[0], "text")) - 1
        
        # Eliminar de la lista
        if 0 <= indice < len(self.lista_estudiantes):
            self.lista_estudiantes.pop(indice)
            
            # Actualizar tabla
            self.actualizar_tabla_estudiantes()
            
            # Actualizar gráfico
            self.actualizar_grafico_estadisticas()
            
            # Limpiar detalles
            self.text_detalles.config(state=tk.NORMAL)
            self.text_detalles.delete(1.0, tk.END)
            self.text_detalles.insert(tk.END, "Seleccione un estudiante para ver sus detalles.")
            self.text_detalles.config(state=tk.DISABLED)
            
            # Mostrar mensaje
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
    
    def limpiar_seleccion(self):
        # Deseleccionar en la tabla
        for item in self.tabla_estudiantes.selection():
            self.tabla_estudiantes.selection_remove(item)
        
        # Limpiar detalles
        self.text_detalles.config(state=tk.NORMAL)
        self.text_detalles.delete(1.0, tk.END)
        self.text_detalles.insert(tk.END, "Seleccione un estudiante para ver sus detalles.")
        self.text_detalles.config(state=tk.DISABLED)
        
        # Restaurar gráfico general
        self.actualizar_grafico_estadisticas()
    
    def actualizar_grafico_notas(self, estudiante):
        # Limpiar gráfico
        self.ax.clear()
        
        if not estudiante.notas:
            self.ax.text(0.5, 0.5, "No hay notas registradas", 
                       ha='center', va='center', transform=self.ax.transAxes)
        else:
            # Preparar datos
            notas = estudiante.notas
            evaluaciones = [f"Eval {i+1}" for i in range(len(notas))]
            
            # Crear gráfico de barras
            bars = self.ax.bar(evaluaciones, notas, color=#3498