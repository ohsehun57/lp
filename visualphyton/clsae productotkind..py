import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore

# Clase Producto
class Producto:
    def __init__(self, nombre, precio, stock, unidad):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.unidad = unidad  # Unidades de medida (ejemplo: "kg", "litros")

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def actualizar_stock(self, nuevo_stock):
        self.stock = nuevo_stock

    def valor_total(self):
        return self.precio * self.stock

# Función principal de la aplicación
class SistemaProductosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Productos")
        self.root.geometry("900x600")
        self.root.config(bg="#e8f4f8")

        self.productos = [
            Producto("Arroz", 3.50, 100, "kg"),
            Producto("Azúcar", 4.50, 50, "kg"),
            Producto("Aceite", 8.00, 80, "litros"),
            Producto("Leche", 4.50, 60, "litros")
        ]
        self.historial = []

        # Variable para el producto editado
        self.producto_editado = None

        # Estilo de fuente
        self.font_header = tkFont.Font(family="Arial", size=14, weight="bold")
        self.font_body = tkFont.Font(family="Arial", size=12)

        # Tab control
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Crear pestañas
        self.tab_tabla = ttk.Frame(self.notebook, bg="#e8f4f8")
        self.tab_graficos = ttk.Frame(self.notebook, bg="#e8f4f8")
        self.tab_historial = ttk.Frame(self.notebook, bg="#e8f4f8")

        self.notebook.add(self.tab_tabla, text="Productos")
        self.notebook.add(self.tab_graficos, text="Gráficos")
        self.notebook.add(self.tab_historial, text="Historial de Cambios")

        # Inicializar las pestañas
        self.crear_tabla(self.tab_tabla)
        self.crear_historial(self.tab_historial)
        self.crear_graficos(self.tab_graficos)

    def crear_tabla(self, parent):
        # Tabla de productos
        self.tree = ttk.Treeview(parent, columns=("ID", "Nombre", "Precio", "Stock", "Unidad", "Valor Total", "Acciones"), show="headings")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nombre", text="Nombre", anchor="center")
        self.tree.heading("Precio", text="Precio", anchor="center")
        self.tree.heading("Stock", text="Stock", anchor="center")
        self.tree.heading("Unidad", text="Unidad", anchor="center")
        self.tree.heading("Valor Total", text="Valor Total", anchor="center")
        self.tree.heading("Acciones", text="Acciones", anchor="center")

        self.tree.column("ID", anchor="center", width=60)
        self.tree.column("Nombre", anchor="center", width=150)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Stock", anchor="center", width=80)
        self.tree.column("Unidad", anchor="center", width=80)
        self.tree.column("Valor Total", anchor="center", width=100)
        self.tree.column("Acciones", anchor="center", width=80)

        self.tree.pack(fill="both", expand=True)

        # Agregar productos a la tabla
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, producto in enumerate(self.productos, 1):
            valor_total = f"${producto.valor_total():.2f}"
            self.tree.insert("", "end", values=(i, producto.nombre, f"${producto.precio:.2f}", producto.stock, producto.unidad, valor_total, "Editar"))
        
        # Bind el clic en el árbol para editar
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

    def on_item_click(self, event):
        item = self.tree.selection()[0]
        producto_index = int(self.tree.item(item, "values")[0]) - 1
        producto = self.productos[producto_index]
        self.editar_producto(producto)

    def editar_producto(self, producto):
        # Crear una ventana para editar el producto
        self.producto_editado = producto
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title(f"Editar Producto: {producto.nombre}")
        self.edit_window.geometry("300x300")
        self.edit_window.config(bg="#e8f4f8")

        # Estilo de fuente
        label_font = tkFont.Font(family="Arial", size=12, weight="normal")

        # Nombre del producto
        tk.Label(self.edit_window, text="Nombre:", font=label_font, bg="#e8f4f8").pack(pady=5)
        tk.Label(self.edit_window, text=producto.nombre, font=self.font_body, bg="#e8f4f8").pack(pady=5)

        # Precio
        tk.Label(self.edit_window, text="Precio:", font=label_font, bg="#e8f4f8").pack(pady=5)
        self.precio_entry = tk.Entry(self.edit_window, font=self.font_body)
        self.precio_entry.insert(0, str(producto.precio))
        self.precio_entry.pack(pady=5)

        # Stock
        tk.Label(self.edit_window, text="Stock:", font=label_font, bg="#e8f4f8").pack(pady=5)
        self.stock_entry = tk.Entry(self.edit_window, font=self.font_body)
        self.stock_entry.insert(0, str(producto.stock))
        self.stock_entry.pack(pady=5)

        # Unidad
        tk.Label(self.edit_window, text="Unidad:", font=label_font, bg="#e8f4f8").pack(pady=5)
        self.unidad_label = tk.Label(self.edit_window, text=producto.unidad, font=self.font_body, bg="#e8f4f8")
        self.unidad_label.pack(pady=5)

        # Botón de guardar
        save_button = tk.Button(self.edit_window, text="Guardar", font=self.font_body, bg="#4CAF50", fg="white", command=self.guardar_edicion)
        save_button.pack(pady=10)

    def guardar_edicion(self):
        try:
            nuevo_precio = float(self.precio_entry.get())
            nuevo_stock = int(self.stock_entry.get())
            # Actualizar producto
            self.producto_editado.actualizar_precio(nuevo_precio)
            self.producto_editado.actualizar_stock(nuevo_stock)
            
            # Guardar en el historial
            self.historial.append(f"Producto '{self.producto_editado.nombre}' actualizado. Precio: ${nuevo_precio} - Stock: {nuevo_stock} {self.producto_editado.unidad}")
            
            self.edit_window.destroy()
            self.actualizar_tabla()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

    def crear_historial(self, parent):
        # Mostrar historial de cambios
        self.historial_text = tk.Text(parent, wrap=tk.WORD, height=15, font=self.font_body, bg="#e8f4f8", fg="black")
        self.historial_text.pack(fill="both", expand=True)

        # Mostrar los cambios
        self.mostrar_historial()

    def mostrar_historial(self):
        self.historial_text.delete(1.0, tk.END)
        for cambio in self.historial:
            self.historial_text.insert(tk.END, f"{cambio}\n")

    def crear_graficos(self, parent):
        # Crear gráfico de barras (por ejemplo, productos más vendidos)
        fig, ax = plt.subplots(figsize=(6, 4))

        # Datos para el gráfico
        nombres = [producto.nombre for producto in self.productos]
        valores = [producto.valor_total() for producto in self.productos]

        ax.bar(nombres, valores, color="#66b3ff")
        ax.set_xlabel("Productos")
        ax.set_ylabel("Valor Total ($)")
        ax.set_title("Valor Total de Productos")

        # Insertar gráfico en la ventana Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaProductosApp(root)
    root.mainloop()
