import tkinter as tk
from tkinter import ttk, messagebox
import random

class Producto:
    def __init__(self, nombre, precio):
        self.__nombre = nombre
        self.__precio = precio
    
    def obtener_nombre(self):
        return self.__nombre
        
    def obtener_precio(self):
        return self.__precio
        
    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self.__precio = nuevo_precio
            return True
        else:
            return False
    
    def calcular_el_igv(self):
        return self.__precio * 0.18
        
    def precio_con_igv(self):
        return self.__precio + self.calcular_el_igv()


class AplicacionProductos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Productos")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Colores
        self.color_fondo = "#f5f5f5"
        self.color_titulo = "#2c3e50"
        self.color_boton_principal = "#3498db"
        self.color_boton_secundario = "#2ecc71"
        self.color_boton_peligro = "#e74c3c"
        self.color_texto = "#34495e"
        
        # Configurar estilo
        self.root.configure(bg=self.color_fondo)
        self.estilo = ttk.Style()
        self.estilo.configure("TLabel", background=self.color_fondo, foreground=self.color_texto)
        self.estilo.configure("Titulo.TLabel", font=("Arial", 14, "bold"), foreground=self.color_titulo)
        self.estilo.configure("Subtitulo.TLabel", font=("Arial", 12, "bold"), foreground=self.color_titulo)
        self.estilo.configure("Info.TLabel", font=("Arial", 11), foreground=self.color_texto)
        
        # Variables para guardar productos
        self.productos = []
        self.producto_seleccionado = None
        
        # Crear el marco principal
        self.crear_interfaz()
        
        # Inicializar con un producto ejemplo (similar al código original)
        self.inicializar_producto_ejemplo()
        
    def crear_interfaz(self):
        # Marco principal con grid layout
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título principal
        ttk.Label(main_frame, text="SISTEMA DE GESTIÓN DE PRODUCTOS", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # Crear los paneles
        self.panel_registro = self.crear_panel_registro(main_frame)
        self.panel_registro.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        self.panel_listado = self.crear_panel_listado(main_frame)
        self.panel_listado.grid(row=1, column=1, sticky="nsew")
        
        self.panel_detalles = self.crear_panel_detalles(main_frame)
        self.panel_detalles.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # Configurar pesos para que los paneles se ajusten al tamaño
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def crear_panel_registro(self, parent):
        panel = ttk.LabelFrame(parent, text="Registro de Producto", padding=15)
        
        # Campos para nombre y precio
        ttk.Label(panel, text="Nombre del producto:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_nombre = ttk.Entry(panel, width=25)
        self.entrada_nombre.grid(row=0, column=1, sticky="we", pady=5)
        
        ttk.Label(panel, text="Precio (S/.):").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_precio = ttk.Entry(panel, width=25)
        self.entrada_precio.grid(row=1, column=1, sticky="we", pady=5)
        
        # Botones de acción
        frame_botones = ttk.Frame(panel)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.btn_registrar = tk.Button(frame_botones, text="Registrar Producto", 
                                     bg=self.color_boton_principal, fg="white",
                                     padx=10, pady=5, command=self.registrar_producto)
        self.btn_registrar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = tk.Button(frame_botones, text="Limpiar", 
                                    bg=self.color_boton_secundario, fg="white",
                                    padx=10, pady=5, command=self.limpiar_entradas)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        return panel
        
    def crear_panel_listado(self, parent):
        panel = ttk.LabelFrame(parent, text="Listado de Productos", padding=15)
        
        # Crear tabla de productos
        columnas = ("nombre", "precio", "igv", "total")
        self.tabla_productos = ttk.Treeview(panel, columns=columnas, show="headings", height=8)
        
        # Configurar encabezados
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("precio", text="Precio Base")
        self.tabla_productos.heading("igv", text="IGV (18%)")
        self.tabla_productos.heading("total", text="Precio con IGV")
        
        # Configurar anchos
        self.tabla_productos.column("nombre", width=150)
        self.tabla_productos.column("precio", width=100)
        self.tabla_productos.column("igv", width=100)
        self.tabla_productos.column("total", width=120)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.tabla_productos.pack(side="left", fill="both", expand=True, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Enlazar evento de selección
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)
        
        return panel
        
    def crear_panel_detalles(self, parent):
        panel = ttk.LabelFrame(parent, text="Detalles del Producto", padding=15)
        
        # Marco para mostrar los detalles del producto seleccionado
        detalles_frame = ttk.Frame(panel)
        detalles_frame.pack(fill="both", expand=True)
        
        # Información del producto
        self.lbl_detalle_nombre = ttk.Label(detalles_frame, text="Nombre: ", style="Info.TLabel")
        self.lbl_detalle_nombre.grid(row=0, column=0, sticky="w", pady=5)
        
        self.lbl_detalle_precio = ttk.Label(detalles_frame, text="Precio Base: ", style="Info.TLabel")
        self.lbl_detalle_precio.grid(row=1, column=0, sticky="w", pady=5)
        
        self.lbl_detalle_igv = ttk.Label(detalles_frame, text="IGV (18%): ", style="Info.TLabel")
        self.lbl_detalle_igv.grid(row=2, column=0, sticky="w", pady=5)
        
        self.lbl_detalle_total = ttk.Label(detalles_frame, text="Precio con IGV: ", style="Info.TLabel")
        self.lbl_detalle_total.grid(row=3, column=0, sticky="w", pady=5)
        
        # Sección para actualizar precio
        ttk.Separator(detalles_frame, orient="horizontal").grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)
        
        ttk.Label(detalles_frame, text="Actualizar Precio", style="Subtitulo.TLabel").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(detalles_frame, text="Nuevo precio (S/.): ").grid(row=6, column=0, sticky="w", pady=5)
        self.entrada_nuevo_precio = ttk.Entry(detalles_frame, width=15)
        self.entrada_nuevo_precio.grid(row=6, column=1, sticky="w", pady=5)
        
        self.btn_actualizar = tk.Button(detalles_frame, text="Actualizar Precio", 
                                      bg=self.color_boton_principal, fg="white",
                                      padx=10, pady=5, command=self.actualizar_precio)
        self.btn_actualizar.grid(row=6, column=2, padx=5, pady=5)
        
        # Botones adicionales
        botones_frame = ttk.Frame(detalles_frame)
        botones_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.btn_eliminar = tk.Button(botones_frame, text="Eliminar Producto", 
                                     bg=self.color_boton_peligro, fg="white",
                                     padx=10, pady=5, command=self.eliminar_producto)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_generar = tk.Button(botones_frame, text="Generar Producto Aleatorio", 
                                    bg=self.color_boton_secundario, fg="white",
                                    padx=10, pady=5, command=self.generar_producto_aleatorio)
        self.btn_generar.pack(side=tk.LEFT, padx=5)
        
        return panel
    
    def inicializar_producto_ejemplo(self):
        # Crear el producto inicial (como en el código original)
        self.entrada_nombre.insert(0, "Laptop")
        self.entrada_precio.insert(0, "2500")
        self.registrar_producto()
        
    def registrar_producto(self):
        try:
            nombre = self.entrada_nombre.get().strip()
            precio = float(self.entrada_precio.get().strip())
            
            if not nombre:
                messagebox.showerror("Error", "Debe ingresar un nombre para el producto")
                return
                
            if precio < 0:
                messagebox.showerror("Error", "El precio no puede ser negativo")
                return
                
            # Crear el producto
            producto = Producto(nombre, precio)
            self.productos.append(producto)
            
            # Actualizar la tabla
            self.actualizar_tabla()
            
            # Limpiar entradas
            self.limpiar_entradas()
            
            messagebox.showinfo("Éxito", f"Producto '{nombre}' registrado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico")
            
    def limpiar_entradas(self):
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_precio.delete(0, tk.END)
        self.entrada_nombre.focus()
        
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
            
        # Insertar productos
        for producto in self.productos:
            nombre = producto.obtener_nombre()
            precio = producto.obtener_precio()
            igv = producto.calcular_el_igv()
            total = producto.precio_con_igv()
            
            self.tabla_productos.insert("", "end", values=(
                nombre, 
                f"S/. {precio:.2f}", 
                f"S/. {igv:.2f}", 
                f"S/. {total:.2f}"
            ))
            
    def seleccionar_producto(self, event):
        seleccion = self.tabla_productos.selection()
        if seleccion:
            item = seleccion[0]
            nombre = self.tabla_productos.item(item, "values")[0]
            
            # Buscar el producto seleccionado
            for producto in self.productos:
                if producto.obtener_nombre() == nombre:
                    self.producto_seleccionado = producto
                    self.mostrar_detalles()
                    break
                    
    def mostrar_detalles(self):
        if self.producto_seleccionado:
            nombre = self.producto_seleccionado.obtener_nombre()
            precio = self.producto_seleccionado.obtener_precio()
            igv = self.producto_seleccionado.calcular_el_igv()
            total = self.producto_seleccionado.precio_con_igv()
            
            self.lbl_detalle_nombre.config(text=f"Nombre: {nombre}")
            self.lbl_detalle_precio.config(text=f"Precio Base: S/. {precio:.2f}")
            self.lbl_detalle_igv.config(text=f"IGV (18%): S/. {igv:.2f}")
            self.lbl_detalle_total.config(text=f"Precio con IGV: S/. {total:.2f}")
            
    def actualizar_precio(self):
        if not self.producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto primero")
            return
            
        try:
            nuevo_precio = float(self.entrada_nuevo_precio.get().strip())
            
            if self.producto_seleccionado.actualizar_precio(nuevo_precio):
                self.actualizar_tabla()
                self.mostrar_detalles()
                self.entrada_nuevo_precio.delete(0, tk.END)
                messagebox.showinfo("Éxito", f"Precio actualizado a S/. {nuevo_precio:.2f}")
            else:
                messagebox.showerror("Error", "El precio no puede ser negativo")
                
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico")
            
    def eliminar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto primero")
            return
            
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{self.producto_seleccionado.obtener_nombre()}'?")
        
        if confirmar:
            self.productos.remove(self.producto_seleccionado)
            self.producto_seleccionado = None
            
            self.actualizar_tabla()
            self.limpiar_detalles()
            
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            
    def limpiar_detalles(self):
        self.lbl_detalle_nombre.config(text="Nombre: ")
        self.lbl_detalle_precio.config(text="Precio Base: ")
        self.lbl_detalle_igv.config(text="IGV (18%): ")
        self.lbl_detalle_total.config(text="Precio con IGV: ")
        self.entrada_nuevo_precio.delete(0, tk.END)
        
    def generar_producto_aleatorio(self):
        # Lista de productos para generar ejemplos aleatorios
        nombres = ["Monitor LED", "Teclado Mecánico", "Mouse Inalámbrico", "Disco SSD", "Memoria RAM", 
                  "Impresora", "Webcam HD", "Audífonos Bluetooth", "Altavoces", "Tablet", 
                  "Smartphone", "Router WiFi", "Switch de Red", "Cable HDMI", "Tarjeta Gráfica"]
        
        nombre = random.choice(nombres)
        precio = round(random.uniform(100, 5000), 2)
        
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_precio.delete(0, tk.END)
        
        self.entrada_nombre.insert(0, nombre)
        self.entrada_precio.insert(0, str(precio))


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionProductos(root)
    root.mainloop()