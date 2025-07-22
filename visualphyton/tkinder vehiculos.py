import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
import hashlib
import uuid
import re

# =====================================================================
# == CLASES DE VEHÍCULOS (LÓGICA DEL NEGOCIO)
# =====================================================================

# Clase base: Vehiculo
class Vehiculo:
    """Clase base para cualquier tipo de vehículo."""
    def __init__(self, marca, modelo, annio):
        self.marca = marca
        self.modelo = modelo
        self.annio = annio

    def calcular_impuesto(self):
        """Método que será sobrescrito en las subclases para calcular el impuesto."""
        pass

    def to_dict(self):
        """Convierte el objeto a un diccionario para poder guardarlo en JSON."""
        return {
            "tipo": self.__class__.__name__,
            "marca": self.marca,
            "modelo": self.modelo,
            "annio": self.annio
        }

# Subclase: Moto
# Herencia: Hereda de Vehiculo
class Moto(Vehiculo):
    """Representa un vehículo de tipo Moto."""
    def __init__(self, marca, modelo, annio, impuesto_base):
        super().__init__(marca, modelo, annio)
        # Encapsulamiento: El impuesto base es un atributo privado.
        self.__impuesto_base = impuesto_base

    def get_impuesto_base(self):
        return self.__impuesto_base

    # Polimorfismo: Sobrescribe el método de la clase padre.
    def calcular_impuesto(self):
        """Calcula el impuesto para una moto, que es simplemente su impuesto base."""
        return self.__impuesto_base

    def to_dict(self):
        """Extiende el diccionario del padre con los atributos específicos de Moto."""
        data = super().to_dict()
        data["impuesto_base"] = self.__impuesto_base
        return data

# Subclase: Auto
# Herencia: Hereda de Vehiculo
class Auto(Vehiculo):
    """Representa un vehículo de tipo Auto."""
    def __init__(self, marca, modelo, annio, impuesto_base, numero_puertas):
        super().__init__(marca, modelo, annio)
        # Encapsulamiento
        self.__impuesto_base = impuesto_base
        self.__numero_puertas = numero_puertas

    def get_impuesto_base(self):
        return self.__impuesto_base

    def get_numero_puertas(self):
        return self.__numero_puertas

    # Polimorfismo: Sobrescribe el método de la clase padre.
    def calcular_impuesto(self):
        """
        Calcula el impuesto para un auto.
        Los autos con más de 2 puertas pagan un 10% extra.
        """
        if self.__numero_puertas > 2:
            return self.__impuesto_base * 1.10
        return self.__impuesto_base

    def to_dict(self):
        """Extiende el diccionario del padre con los atributos específicos de Auto."""
        data = super().to_dict()
        data["impuesto_base"] = self.__impuesto_base
        data["numero_puertas"] = self.__numero_puertas
        return data

# =====================================================================
# == CLASES DE LA INTERFAZ GRÁFICA (PRESENTACIÓN)
# =====================================================================

class FinanceManager(tk.Tk):
    """
    Gestor principal que integra Finanzas y Vehículos.
    """
    def __init__(self):
        super().__init__()
        self.title("🚗 Gestor Integral v2.0")
        self.geometry("1200x700")
        self.configure(bg="#0f172a")

        # Datos de la aplicación
        self.vehicles = [] # Lista para almacenar objetos de vehículos

        self.setup_styles()
        self.create_main_interface()
        self.load_data() # Carga tanto finanzas como vehículos
        self.update_vehicle_display() # Actualiza la UI de vehículos

    def setup_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style(self)
        style.theme_use('clam')
        colors = {
            'bg_primary': '#0f172a', 'bg_secondary': '#1e293b', 'bg_tertiary': '#334155',
            'accent': '#3b82f6', 'accent_hover': '#2563eb', 'success': '#10b981',
            'danger': '#ef4444', 'text_primary': '#f8fafc', 'text_secondary': '#cbd5e1',
            'border': '#475569'
        }
        style.configure('Dark.TFrame', background=colors['bg_secondary'])
        style.configure('Primary.TFrame', background=colors['bg_primary'])
        style.configure('Dark.TLabel', background=colors['bg_secondary'], foreground=colors['text_primary'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=colors['bg_primary'], foreground=colors['text_primary'], font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=colors['bg_secondary'], foreground=colors['text_secondary'], font=('Segoe UI', 12, 'bold'))
        style.configure('Total.TLabel', background=colors['bg_secondary'], foreground=colors['success'], font=('Segoe UI', 16, 'bold'))
        style.configure('Dark.TEntry', fieldbackground=colors['bg_tertiary'], foreground=colors['text_primary'], bordercolor=colors['border'], font=('Segoe UI', 10))
        style.configure('Dark.TCombobox', fieldbackground=colors['bg_tertiary'], foreground=colors['text_primary'], bordercolor=colors['border'], font=('Segoe UI', 10))
        style.map('Dark.TCombobox', fieldbackground=[('readonly', colors['bg_tertiary'])])
        style.configure('Accent.TButton', background=colors['accent'], foreground='white', font=('Segoe UI', 10, 'bold'), padding=(15, 8))
        style.map('Accent.TButton', background=[('active', colors['accent_hover'])])
        style.configure("Dark.Treeview", background=colors['bg_tertiary'], foreground=colors['text_primary'], fieldbackground=colors['bg_tertiary'], font=('Segoe UI', 9))
        style.configure("Dark.Treeview.Heading", background=colors['bg_secondary'], foreground=colors['text_primary'], font=('Segoe UI', 9, 'bold'))
        style.map('Dark.Treeview', background=[('selected', colors['accent'])])

    def create_main_interface(self):
        """Crea la estructura principal de la GUI con pestañas."""
        main_frame = ttk.Frame(self, style='Primary.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(main_frame, text="🚗 Gestor Integral", style='Title.TLabel').pack(pady=(0, 20), anchor="w")

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        self.create_vehicles_tab() # Crear la nueva pestaña de vehículos

    def create_vehicles_tab(self):
        """Crea la pestaña para la gestión de vehículos."""
        vehicles_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding=20)
        self.notebook.add(vehicles_frame, text=' GESTIÓN DE VEHÍCULOS 🚗 ')

        # --- Panel Principal (Izquierda: Formulario, Derecha: Lista) ---
        main_panel = tk.PanedWindow(vehicles_frame, orient=tk.HORIZONTAL, bg="#1e293b", sashwidth=10)
        main_panel.pack(fill=tk.BOTH, expand=True)

        # --- Formulario de Registro (Panel Izquierdo) ---
        form_frame = ttk.Frame(main_panel, style='Dark.TFrame', width=350)
        main_panel.add(form_frame, stretch="never")

        ttk.Label(form_frame, text="Registrar Nuevo Vehículo", style='Subtitle.TLabel').pack(pady=(0, 20), anchor='w')

        # Tipo de Vehículo
        ttk.Label(form_frame, text="Tipo de Vehículo:", style='Dark.TLabel').pack(anchor='w', padx=5, pady=(0, 5))
        self.vehicle_type_var = tk.StringVar()
        self.vehicle_type_combo = ttk.Combobox(form_frame, textvariable=self.vehicle_type_var, values=["Moto", "Auto"], state="readonly", style='Dark.TCombobox')
        self.vehicle_type_combo.pack(fill='x', padx=5, pady=(0, 10))
        self.vehicle_type_combo.bind("<<ComboboxSelected>>", self.toggle_door_entry)

        # Campos comunes
        fields = {"Marca": "marca", "Modelo": "modelo", "Año": "annio", "Impuesto Base (S/.)": "impuesto_base"}
        self.vehicle_entries = {}
        for label_text, key in fields.items():
            ttk.Label(form_frame, text=label_text, style='Dark.TLabel').pack(anchor='w', padx=5, pady=(0, 5))
            entry = ttk.Entry(form_frame, style='Dark.TEntry')
            entry.pack(fill='x', padx=5, pady=(0, 10))
            self.vehicle_entries[key] = entry

        # Campo dinámico para Número de Puertas
        self.doors_label = ttk.Label(form_frame, text="Número de Puertas:", style='Dark.TLabel')
        self.doors_entry = ttk.Entry(form_frame, style='Dark.TEntry')
        self.vehicle_entries["numero_puertas"] = self.doors_entry

        # Botón de registro
        ttk.Button(form_frame, text="Registrar Vehículo", command=self.register_vehicle, style='Accent.TButton').pack(fill='x', padx=5, pady=20)

        # --- Visualización de Vehículos (Panel Derecho) ---
        display_frame = ttk.Frame(main_panel, style='Dark.TFrame')
        main_panel.add(display_frame)

        ttk.Label(display_frame, text="Listado de Vehículos Registrados", style='Subtitle.TLabel').pack(pady=(0, 20), anchor='w')

        # Treeview para mostrar vehículos
        cols = ("#", "Tipo", "Marca", "Modelo", "Año", "Impuesto (S/.)")
        self.vehicle_tree = ttk.Treeview(display_frame, columns=cols, show='headings', style='Dark.Treeview')
        for col in cols:
            self.vehicle_tree.heading(col, text=col)
        self.vehicle_tree.column("#", width=50, anchor='center')
        self.vehicle_tree.column("Impuesto (S/.)", anchor='e')
        self.vehicle_tree.pack(fill='both', expand=True)

        # Resumen de Impuestos
        summary_frame = ttk.Frame(display_frame, style='Dark.TFrame', padding=(0, 10))
        summary_frame.pack(fill='x', side='bottom')
        ttk.Label(summary_frame, text="Impuesto Total a Pagar:", style='Dark.TLabel', font=('Segoe UI', 12, 'bold')).pack(side='left')
        self.total_tax_label = ttk.Label(summary_frame, text="S/. 0.00", style='Total.TLabel')
        self.total_tax_label.pack(side='right')

    def toggle_door_entry(self, event=None):
        """Muestra u oculta el campo 'Número de Puertas' según el tipo de vehículo."""
        if self.vehicle_type_var.get() == "Auto":
            self.doors_label.pack(anchor='w', padx=5, pady=(0, 5))
            self.doors_entry.pack(fill='x', padx=5, pady=(0, 10))
        else:
            self.doors_label.pack_forget()
            self.doors_entry.pack_forget()

    def register_vehicle(self):
        """Valida los datos del formulario y registra un nuevo vehículo."""
        # Validación de datos de entrada
        try:
            tipo = self.vehicle_type_var.get()
            if not tipo:
                raise ValueError("Debe seleccionar un tipo de vehículo.")
            
            marca = self.vehicle_entries["marca"].get()
            modelo = self.vehicle_entries["modelo"].get()
            if not marca or not modelo:
                raise ValueError("La marca y el modelo no pueden estar vacíos.")

            annio = int(self.vehicle_entries["annio"].get())
            impuesto_base = float(self.vehicle_entries["impuesto_base"].get())
            
            if annio <= 1900 or impuesto_base < 0:
                raise ValueError("Año o impuesto base inválido.")

            # Creación del objeto según el tipo
            if tipo == "Moto":
                nuevo_vehiculo = Moto(marca, modelo, annio, impuesto_base)
            elif tipo == "Auto":
                numero_puertas = int(self.vehicle_entries["numero_puertas"].get())
                if numero_puertas <= 0:
                     raise ValueError("El número de puertas debe ser positivo.")
                nuevo_vehiculo = Auto(marca, modelo, annio, impuesto_base, numero_puertas)
            
            self.vehicles.append(nuevo_vehiculo)
            self.update_vehicle_display()
            self.save_data() # Guardar después de registrar

            messagebox.showinfo("Éxito", f"{tipo} registrado correctamente.")
            
            # Limpiar formulario
            for entry in self.vehicle_entries.values():
                entry.delete(0, tk.END)
            self.vehicle_type_combo.set('')
            self.toggle_door_entry()

        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Dato inválido: {e}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")


    def update_vehicle_display(self):
        """Actualiza la tabla de vehículos y el cálculo total de impuestos."""
        # Limpiar la tabla antes de actualizar
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)

        total_tax = 0
        for i, vehiculo in enumerate(self.vehicles, start=1):
            impuesto = vehiculo.calcular_impuesto()
            total_tax += impuesto
            
            # Insertar datos en la tabla
            tipo = vehiculo.__class__.__name__
            self.vehicle_tree.insert("", "end", values=(
                i, tipo, vehiculo.marca, vehiculo.modelo, vehiculo.annio, f"{impuesto:,.2f}"
            ))
        
        # Actualizar la etiqueta del total
        self.total_tax_label.config(text=f"S/. {total_tax:,.2f}")

    def get_data_filename(self):
        """Genera un nombre de archivo único para los datos del 'usuario'."""
        # Simulación de un nombre de usuario para el archivo de datos
        username = "default_user" 
        return f"data_{username}.json"

    def save_data(self):
        """Guarda todos los datos de la aplicación (incluidos los vehículos) en un archivo JSON."""
        filename = self.get_data_filename()
        
        # Serializar la lista de objetos de vehículos a una lista de diccionarios
        vehicles_data = [v.to_dict() for v in self.vehicles]
        
        all_data = {
            "vehicles": vehicles_data,
            # Aquí se podrían añadir otros datos como finanzas, etc.
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)

    def load_data(self):
        """Carga los datos desde un archivo JSON al iniciar la aplicación."""
        filename = self.get_data_filename()
        if not os.path.exists(filename):
            return # No hay datos que cargar

        with open(filename, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        # Cargar y reconstruir los objetos de vehículo
        vehicles_data = all_data.get("vehicles", [])
        self.vehicles = []
        for v_data in vehicles_data:
            if v_data["tipo"] == "Moto":
                vehiculo = Moto(v_data["marca"], v_data["modelo"], v_data["annio"], v_data["impuesto_base"])
            elif v_data["tipo"] == "Auto":
                vehiculo = Auto(v_data["marca"], v_data["modelo"], v_data["annio"], v_data["impuesto_base"], v_data["numero_puertas"])
            else:
                continue # Omitir tipos desconocidos
            self.vehicles.append(vehiculo)

# =====================================================================
# == PUNTO DE ENTRADA DE LA APLICACIÓN
# =====================================================================

if __name__ == "__main__":
    app = FinanceManager()
    app.mainloop()
