import tkinter as tk
from tkinter import ttk, messagebox, font
import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# ==============================================================================
# 1. CLASES DE FIGURAS (2D y 3D)
# ==============================================================================

# --- Clase Base (Superclase) ---
class Figura:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_nombre(self):
        return self.__nombre

    def get_fecha_creacion(self):
        return self.__fecha_creacion

    def calcular_area(self):
        return 0

    def calcular_perimetro(self):
        return 0

    def calcular_area_superficial(self):
        return 0

    def calcular_volumen(self):
        return 0

    def get_info_completa(self):
        return {
            'nombre': self.get_nombre(),
            'area': self.calcular_area(),
            'perimetro': self.calcular_perimetro(),
            'area_superficial': self.calcular_area_superficial(),
            'volumen': self.calcular_volumen(),
            'fecha': self.get_fecha_creacion()
        }

# --- Subclases 2D ---
class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.__radio = radio

    def get_radio(self):
        return self.__radio

    def calcular_area(self):
        return math.pi * self.__radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.__radio

    def get_info_completa(self):
        info = super().get_info_completa()
        info['radio'] = self.__radio
        return info

class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.__base = base
        self.__altura = altura

    def get_base(self):
        return self.__base

    def get_altura(self):
        return self.__altura

    def calcular_area(self):
        return self.__base * self.__altura

    def calcular_perimetro(self):
        return 2 * (self.__base + self.__altura)

    def get_info_completa(self):
        info = super().get_info_completa()
        info['base'] = self.__base
        info['altura'] = self.__altura
        return info

class Triangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Triángulo")
        self.__base = base
        self.__altura = altura

    def calcular_area(self):
        return (self.__base * self.__altura) / 2

    def calcular_perimetro(self):
        # Asumiendo triángulo rectángulo para simplicidad del perímetro
        hipotenusa = math.sqrt(self.__base**2 + self.__altura**2)
        return self.__base + self.__altura + hipotenusa

    def get_info_completa(self):
        info = super().get_info_completa()
        info['base'] = self.__base
        info['altura'] = self.__altura
        return info

# --- Clase Base para Figuras 3D ---
class Figura3D(Figura):
    def __init__(self, nombre):
        super().__init__(nombre)
    
    # Las figuras 3D no tienen área o perímetro 2D
    def calcular_area(self):
        return 0

    def calcular_perimetro(self):
        return 0

# --- Subclases 3D ---
class Esfera(Figura3D):
    def __init__(self, radio):
        super().__init__("Esfera")
        self.__radio = radio
    
    def get_radio(self):
        return self.__radio

    def calcular_area_superficial(self):
        return 4 * math.pi * self.__radio**2
    
    def calcular_volumen(self):
        return (4/3) * math.pi * self.__radio**3

    def get_info_completa(self):
        info = super().get_info_completa()
        info['radio'] = self.__radio
        return info

class Cubo(Figura3D):
    def __init__(self, lado):
        super().__init__("Cubo")
        self.__lado = lado

    def get_lado(self):
        return self.__lado
    
    def calcular_area_superficial(self):
        return 6 * self.__lado**2
    
    def calcular_volumen(self):
        return self.__lado**3

    def get_info_completa(self):
        info = super().get_info_completa()
        info['lado'] = self.__lado
        return info

class Cilindro(Figura3D):
    def __init__(self, radio, altura):
        super().__init__("Cilindro")
        self.__radio = radio
        self.__altura = altura
    
    def get_radio(self):
        return self.__radio
        
    def get_altura(self):
        return self.__altura

    def calcular_area_superficial(self):
        return (2 * math.pi * self.__radio * self.__altura) + (2 * math.pi * self.__radio**2)
    
    def calcular_volumen(self):
        return math.pi * self.__radio**2 * self.__altura
    
    def get_info_completa(self):
        info = super().get_info_completa()
        info['radio'] = self.__radio
        info['altura'] = self.__altura
        return info


# ==============================================================================
# 2. CLASE DE LA INTERFAZ GRÁFICA (GUI)
# ==============================================================================
class FigurasGeometricasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Figuras Geométricas 3D Pro")
        self.root.geometry("1280x850")
        self.root.configure(bg='#eaf2f8')
        self.root.resizable(True, True)

        self.lista_figuras = []
        self.tipo_figura_actual = None

        self.configurar_estilos_y_fuentes()
        self.crear_interfaz_principal()
        self.centrar_ventana()

    def configurar_estilos_y_fuentes(self):
        # Fuentes
        self.font_titulo = font.Font(family='Segoe UI', size=24, weight='bold')
        self.font_subtitulo = font.Font(family='Segoe UI', size=14, weight='bold')
        self.font_normal = font.Font(family='Segoe UI', size=11)
        self.font_boton = font.Font(family='Segoe UI', size=10, weight='bold')

        # Estilos ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Notebook y Pestañas
        style.configure('TNotebook', background='#eaf2f8', borderwidth=0)
        style.configure('TNotebook.Tab', 
                        background='#aed6f1', 
                        foreground='#1b4f72', 
                        padding=[10, 5],
                        font=self.font_normal,
                        borderwidth=0)
        style.map('TNotebook.Tab', 
                  background=[('selected', '#ffffff')],
                  foreground=[('selected', '#1a5276')])

        # Estilo para Botones
        style.configure('Accent.TButton',
                        background='#3498db',
                        foreground='white',
                        font=self.font_boton,
                        padding=(12, 8),
                        borderwidth=0,
                        relief='flat')
        style.map('Accent.TButton',
                  background=[('active', '#5dade2'), ('disabled', '#aed6f1')])

        # Estilo para Frames tipo "Card"
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)

    def centrar_ventana(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y-30}') # Mover un poco hacia arriba

    def crear_interfaz_principal(self):
        # Layout principal con grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header_frame = tk.Frame(self.root, bg='#1a5276', padx=20, pady=15)
        header_frame.grid(row=0, column=0, sticky='ew')
        
        titulo_label = tk.Label(header_frame,
                                text="🔷 Sistema de Figuras Geométricas 3D Pro",
                                font=self.font_titulo,
                                fg='white',
                                bg='#1a5276')
        titulo_label.pack()

        # --- Contenido Principal (Notebook) ---
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=1, column=0, sticky='nsew')
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        
        # --- Pestañas ---
        self.crear_pestaña_creacion_2d()
        self.crear_pestaña_creacion_3d()
        self.crear_pestaña_visualizacion()
        self.crear_pestaña_estadisticas()
        
        # --- Footer (Información en tiempo real) ---
        footer_frame = ttk.Frame(self.root, style='Card.TFrame', padding=10)
        footer_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        self.info_label = tk.Label(footer_frame,
                                   text="💡 Total de figuras: 0",
                                   font=self.font_normal,
                                   fg='#34495e',
                                   bg='white')
        self.info_label.pack()
        self.actualizar_info_tiempo_real()

    def crear_pestaña_creacion_2d(self):
        pestaña = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(pestaña, text="➕ Crear Figuras 2D")
        
        # Contenedor principal para la creación
        crear_frame = ttk.Frame(pestaña, style='Card.TFrame', padding=20)
        crear_frame.pack(fill=tk.BOTH, expand=True)

        # Botones de selección de figura
        botones_frame = ttk.Frame(crear_frame, style='Card.TFrame')
        botones_frame.pack(fill=tk.X, pady=(0, 20))
        
        btn_circulo = ttk.Button(botones_frame, text="🔴 Círculo", style='Accent.TButton', command=lambda: self.preparar_creacion('circulo', frame_2d))
        btn_circulo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        
        btn_rectangulo = ttk.Button(botones_frame, text="🔳 Rectángulo", style='Accent.TButton', command=lambda: self.preparar_creacion('rectangulo', frame_2d))
        btn_rectangulo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        btn_triangulo = ttk.Button(botones_frame, text="🔺 Triángulo", style='Accent.TButton', command=lambda: self.preparar_creacion('triangulo', frame_2d))
        btn_triangulo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        # Frame para la entrada de datos
        frame_2d = ttk.LabelFrame(crear_frame, text="Datos de la Figura 2D", padding=20)
        frame_2d.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.entrada_frame_2d = frame_2d

    def crear_pestaña_creacion_3d(self):
        pestaña = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(pestaña, text="🧊 Crear Figuras 3D")
        
        crear_frame = ttk.Frame(pestaña, style='Card.TFrame', padding=20)
        crear_frame.pack(fill=tk.BOTH, expand=True)

        botones_frame = ttk.Frame(crear_frame, style='Card.TFrame')
        botones_frame.pack(fill=tk.X, pady=(0, 20))

        btn_esfera = ttk.Button(botones_frame, text="🌐 Esfera", style='Accent.TButton', command=lambda: self.preparar_creacion('esfera', frame_3d))
        btn_esfera.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        btn_cubo = ttk.Button(botones_frame, text="📦 Cubo", style='Accent.TButton', command=lambda: self.preparar_creacion('cubo', frame_3d))
        btn_cubo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        btn_cilindro = ttk.Button(botones_frame, text="🥫 Cilindro", style='Accent.TButton', command=lambda: self.preparar_creacion('cilindro', frame_3d))
        btn_cilindro.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        frame_3d = ttk.LabelFrame(crear_frame, text="Datos de la Figura 3D", padding=20)
        frame_3d.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.entrada_frame_3d = frame_3d

    def preparar_creacion(self, tipo_figura, frame_destino):
        # Limpiar ambos frames de entrada
        for widget in self.entrada_frame_2d.winfo_children():
            widget.destroy()
        for widget in self.entrada_frame_3d.winfo_children():
            widget.destroy()
            
        self.tipo_figura_actual = tipo_figura
        self.entries = {}

        # Crear campos de entrada dinámicamente
        campos = {
            'circulo': ['Radio'], 'rectangulo': ['Base', 'Altura'], 'triangulo': ['Base', 'Altura'],
            'esfera': ['Radio'], 'cubo': ['Lado'], 'cilindro': ['Radio', 'Altura']
        }
        
        for i, campo in enumerate(campos[tipo_figura]):
            tk.Label(frame_destino, text=f"{campo}:", font=self.font_normal, bg='white').grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame_destino, font=self.font_normal)
            entry.grid(row=i, column=1, sticky=tk.EW, pady=5, padx=5)
            self.entries[campo.lower()] = entry
            entry.bind('<Return>', lambda e: self.calcular_figura())

        frame_destino.grid_columnconfigure(1, weight=1)
        list(self.entries.values())[0].focus()

        # Botones de acción
        accion_frame = ttk.Frame(frame_destino, style='Card.TFrame')
        accion_frame.grid(row=len(campos[tipo_figura]), column=0, columnspan=2, pady=(20, 0), sticky='ew')
        
        btn_calcular = ttk.Button(accion_frame, text="📊 Calcular y Agregar", style='Accent.TButton', command=self.calcular_figura)
        btn_calcular.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_limpiar = ttk.Button(accion_frame, text="🧹 Limpiar", command=self.limpiar_campos)
        btn_limpiar.pack(side=tk.LEFT, padx=10, pady=10)

    def calcular_figura(self):
        try:
            figura = None
            if self.tipo_figura_actual == 'circulo':
                radio = float(self.entries['radio'].get())
                if radio <= 0: raise ValueError("El radio debe ser positivo.")
                figura = Circulo(radio)
            elif self.tipo_figura_actual == 'rectangulo':
                base = float(self.entries['base'].get())
                altura = float(self.entries['altura'].get())
                if base <= 0 or altura <= 0: raise ValueError("Base y altura deben ser positivos.")
                figura = Rectangulo(base, altura)
            elif self.tipo_figura_actual == 'triangulo':
                base = float(self.entries['base'].get())
                altura = float(self.entries['altura'].get())
                if base <= 0 or altura <= 0: raise ValueError("Base y altura deben ser positivos.")
                figura = Triangulo(base, altura)
            elif self.tipo_figura_actual == 'esfera':
                radio = float(self.entries['radio'].get())
                if radio <= 0: raise ValueError("El radio debe ser positivo.")
                figura = Esfera(radio)
            elif self.tipo_figura_actual == 'cubo':
                lado = float(self.entries['lado'].get())
                if lado <= 0: raise ValueError("El lado debe ser positivo.")
                figura = Cubo(lado)
            elif self.tipo_figura_actual == 'cilindro':
                radio = float(self.entries['radio'].get())
                altura = float(self.entries['altura'].get())
                if radio <= 0 or altura <= 0: raise ValueError("Radio y altura deben ser positivos.")
                figura = Cilindro(radio, altura)

            if figura:
                self.lista_figuras.append(figura)
                messagebox.showinfo("Éxito", f"{figura.get_nombre()} agregado exitosamente!")
                self.actualizar_lista()
                self.actualizar_info_tiempo_real()
                self.limpiar_campos()
                if isinstance(figura, Figura3D):
                    self.visualizar_3d(figura)
        
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Dato inválido: {e}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ha ocurrido un error: {e}")

    def limpiar_campos(self):
        for widget in self.entrada_frame_2d.winfo_children():
            widget.destroy()
        for widget in self.entrada_frame_3d.winfo_children():
            widget.destroy()
        self.tipo_figura_actual = None

    def crear_pestaña_visualizacion(self):
        pestaña = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(pestaña, text="👁️ Visualización de Datos")
        
        control_frame = ttk.Frame(pestaña)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        btn_actualizar = ttk.Button(control_frame, text="🔄 Actualizar", command=self.actualizar_lista)
        btn_actualizar.pack(side=tk.LEFT, padx=(0, 10))
        btn_eliminar = ttk.Button(control_frame, text="🗑️ Eliminar", command=self.eliminar_figura)
        btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        btn_limpiar_todo = ttk.Button(control_frame, text="🧹 Limpiar Todo", command=self.limpiar_todo)
        btn_limpiar_todo.pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(pestaña)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('Tipo', 'Parámetros', 'Área', 'Perímetro', 'Área Superficial', 'Volumen', 'Fecha')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=font.Font().measure(col) + 20, anchor='center')
        
        self.tree.column('Parámetros', width=180)
        self.tree.column('Fecha', width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def actualizar_lista(self):
        self.tree.delete(*self.tree.get_children())
        for figura in self.lista_figuras:
            info = figura.get_info_completa()
            parametros = ""
            if isinstance(figura, Circulo): parametros = f"Radio: {info['radio']:.2f}"
            elif isinstance(figura, Rectangulo): parametros = f"Base: {info['base']:.2f}, Altura: {info['altura']:.2f}"
            elif isinstance(figura, Triangulo): parametros = f"Base: {info['base']:.2f}, Altura: {info['altura']:.2f}"
            elif isinstance(figura, Esfera): parametros = f"Radio: {info['radio']:.2f}"
            elif isinstance(figura, Cubo): parametros = f"Lado: {info['lado']:.2f}"
            elif isinstance(figura, Cilindro): parametros = f"Radio: {info['radio']:.2f}, Altura: {info['altura']:.2f}"

            area_str = f"{info['area']:.2f}" if info['area'] > 0 else "N/A"
            perimetro_str = f"{info['perimetro']:.2f}" if info['perimetro'] > 0 else "N/A"
            area_sup_str = f"{info['area_superficial']:.2f}" if info['area_superficial'] > 0 else "N/A"
            volumen_str = f"{info['volumen']:.2f}" if info['volumen'] > 0 else "N/A"
            
            self.tree.insert('', 'end', values=(
                info['nombre'], parametros, area_str, perimetro_str,
                area_sup_str, volumen_str, info['fecha']
            ))

    def eliminar_figura(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una figura para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro?"):
            item = seleccion[0]
            index = self.tree.index(item)
            del self.lista_figuras[index]
            self.actualizar_lista()
            self.actualizar_info_tiempo_real()
            messagebox.showinfo("Éxito", "Figura eliminada.")

    def limpiar_todo(self):
        if not self.lista_figuras:
            messagebox.showinfo("Información", "No hay figuras para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar TODAS las figuras?"):
            self.lista_figuras.clear()
            self.actualizar_lista()
            self.actualizar_info_tiempo_real()
            messagebox.showinfo("Éxito", "Todas las figuras han sido eliminadas.")

    def actualizar_info_tiempo_real(self):
        total = len(self.lista_figuras)
        fig_2d = [f for f in self.lista_figuras if not isinstance(f, Figura3D)]
        fig_3d = [f for f in self.lista_figuras if isinstance(f, Figura3D)]

        area_total = sum(f.calcular_area() for f in fig_2d)
        volumen_total = sum(f.calcular_volumen() for f in fig_3d)

        info_text = (f"💡 Total: {total} figuras | Figuras 2D: {len(fig_2d)} | Figuras 3D: {len(fig_3d)} | "
                     f"Área 2D Total: {area_total:.2f} | Volumen 3D Total: {volumen_total:.2f}")
        self.info_label.config(text=info_text)

    def crear_pestaña_estadisticas(self):
        pestaña = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(pestaña, text="📈 Estadísticas")
        
        btn_actualizar_stats = ttk.Button(pestaña, text="📊 Actualizar Estadísticas", command=self.actualizar_estadisticas)
        btn_actualizar_stats.pack(pady=10)

        stats_frame = ttk.Frame(pestaña)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)

        # Gráficos
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.fig.patch.set_facecolor('white')
        self.canvas = FigureCanvasTkAgg(self.fig, stats_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew', padx=(0,10))

        # Texto de estadísticas
        self.stats_text = tk.Text(stats_frame, height=10, wrap=tk.WORD, font=self.font_normal, relief='flat', bg='#fdfefe')
        self.stats_text.grid(row=0, column=1, sticky='nsew')
        
    def actualizar_estadisticas(self):
        if not self.lista_figuras:
            messagebox.showinfo("Información", "No hay figuras para generar estadísticas.")
            return

        tipos_count = {}
        areas = [f.calcular_area() for f in self.lista_figuras if not isinstance(f, Figura3D) and f.calcular_area() > 0]
        perimetros = [f.calcular_perimetro() for f in self.lista_figuras if not isinstance(f, Figura3D) and f.calcular_perimetro() > 0]
        volumenes = [f.calcular_volumen() for f in self.lista_figuras if isinstance(f, Figura3D)]
        areas_sup = [f.calcular_area_superficial() for f in self.lista_figuras if isinstance(f, Figura3D)]

        for figura in self.lista_figuras:
            tipos_count[figura.get_nombre()] = tipos_count.get(figura.get_nombre(), 0) + 1

        self.ax1.clear()
        self.ax2.clear()

        # Gráfico de barras de tipos
        if tipos_count:
            self.ax1.bar(tipos_count.keys(), tipos_count.values(), color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FED766', '#2AB7CA', '#F0CF65'])
            self.ax1.set_title('Distribución de Tipos de Figuras')
            self.ax1.set_ylabel('Cantidad')
            self.ax1.tick_params(axis='x', rotation=30)
        
        # Gráfico de dispersión
        if volumenes and areas_sup:
            self.ax2.scatter(volumenes, areas_sup, c='#3498db', alpha=0.7, s=100)
            self.ax2.set_title('Volumen vs. Área Superficial (3D)')
            self.ax2.set_xlabel('Volumen')
            self.ax2.set_ylabel('Área Superficial')
        elif areas and perimetros:
            self.ax2.scatter(areas, perimetros, c='#e74c3c', alpha=0.7, s=100)
            self.ax2.set_title('Área vs. Perímetro (2D)')
            self.ax2.set_xlabel('Área')
            self.ax2.set_ylabel('Perímetro')

        self.fig.tight_layout()
        self.canvas.draw()
        
        # Estadísticas de texto
        self.stats_text.delete(1.0, tk.END)
        stats_info = f"--- Estadísticas Generales ---\n"
        stats_info += f"• Total de figuras: {len(self.lista_figuras)}\n\n"
        if areas:
            stats_info += "--- Figuras 2D ---\n"
            stats_info += f"• Área Promedio: {np.mean(areas):.2f}\n"
            stats_info += f"• Perímetro Promedio: {np.mean(perimetros):.2f}\n"
        if volumenes:
            stats_info += "\n--- Figuras 3D ---\n"
            stats_info += f"• Volumen Promedio: {np.mean(volumenes):.2f}\n"
            stats_info += f"• Área Superficial Promedio: {np.mean(areas_sup):.2f}\n"
        
        self.stats_text.insert(tk.END, stats_info)

    def visualizar_3d(self, figura):
        win = tk.Toplevel(self.root)
        win.title(f"Visualización 3D: {figura.get_nombre()}")
        win.geometry("600x600")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('white')
        ax.grid(True)
        
        # Configurar límites iguales para una mejor proporción
        def set_axes_equal(ax, limits):
            ax.set_xlim(limits)
            ax.set_ylim(limits)
            ax.set_zlim(limits)

        if isinstance(figura, Esfera):
            r = figura.get_radio()
            u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
            x = r * np.cos(u) * np.sin(v)
            y = r * np.sin(u) * np.sin(v)
            z = r * np.cos(v)
            ax.plot_surface(x, y, z, color='#3498db', alpha=0.7)
            set_axes_equal(ax, [-r, r])

        elif isinstance(figura, Cubo):
            l = figura.get_lado()
            p = l / 2
            v = np.array([[-p,-p,-p], [p,-p,-p], [p,p,-p], [-p,p,-p], [-p,-p,p], [p,-p,p], [p,p,p], [-p,p,p]])
            ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
            verts = [ [v[0],v[1],v[2],v[3]], [v[4],v[5],v[6],v[7]], [v[0],v[1],v[5],v[4]],
                      [v[2],v[3],v[7],v[6]], [v[1],v[2],v[6],v[5]], [v[4],v[7],v[3],v[0]] ]
            ax.add_collection3d(Poly3DCollection(verts, facecolors='#3498db', linewidths=1, edgecolors='k', alpha=.5))
            set_axes_equal(ax, [-p, p])

        elif isinstance(figura, Cilindro):
            r, h = figura.get_radio(), figura.get_altura()
            # Cuerpo del cilindro
            u = np.linspace(0, 2 * np.pi, 50)
            z = np.linspace(-h/2, h/2, 2)
            u, z = np.meshgrid(u, z)
            x = r * np.cos(u)
            y = r * np.sin(u)
            ax.plot_surface(x, y, z, color='#3498db', alpha=0.7)
            # Tapas
            u = np.linspace(0, 2 * np.pi, 50)
            x_t = r * np.cos(u)
            y_t = r * np.sin(u)
            ax.fill(x_t, y_t, h/2, color='#3498db', alpha=0.7)
            ax.fill(x_t, y_t, -h/2, color='#3498db', alpha=0.7)
            limit = max(r, h/2)
            set_axes_equal(ax, [-limit, limit])


        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# ==============================================================================
# 3. FUNCIÓN PRINCIPAL
# ==============================================================================
def main():
    root = tk.Tk()
    app = FigurasGeometricasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()