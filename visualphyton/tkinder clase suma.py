import tkinter as tk
from tkinter import ttk, messagebox
import math

class TrianguloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Triángulo")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables para almacenar los valores
        self.base = tk.DoubleVar()
        self.altura = tk.DoubleVar()
        self.perimetro = tk.DoubleVar()
        self.area = tk.DoubleVar()
        self.hipotenusa = tk.DoubleVar()
        
        # Crear el triángulo actual
        self.triangulo_actual = None
        
        # Crear la estructura de la aplicación
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estilo para los widgets
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TEntry", font=("Arial", 12), padding=5)
        
        # Frame para los inputs
        input_frame = ttk.LabelFrame(main_frame, text="Datos del Triángulo", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Entrada para la base
        ttk.Label(input_frame, text="Base:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.base, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="unidades").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Entrada para la altura
        ttk.Label(input_frame, text="Altura:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.altura, width=15).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="unidades").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Botón para calcular
        ttk.Button(input_frame, text="Calcular", command=self.calcular).grid(row=0, column=3, rowspan=2, padx=20, pady=10)
        
        # Frame para mostrar resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        result_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Mostrar hipotenusa
        ttk.Label(result_frame, text="Hipotenusa:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.hipotenusa_label = ttk.Label(result_frame, text="0.00 unidades")
        self.hipotenusa_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Mostrar perímetro
        ttk.Label(result_frame, text="Perímetro:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.perimetro_label = ttk.Label(result_frame, text="0.00 unidades")
        self.perimetro_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Mostrar área
        ttk.Label(result_frame, text="Área:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.area_label = ttk.Label(result_frame, text="0.00 unidades²")
        self.area_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Canvas para dibujar el triángulo
        canvas_frame = ttk.LabelFrame(main_frame, text="Visualización", padding="10")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=600, height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para mostrar información adicional
        info_frame = ttk.Frame(main_frame, padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Etiqueta para información
        self.info_label = ttk.Label(info_frame, text="Ingrese los valores de base y altura para calcular", 
                                  font=("Arial", 10), wraplength=700, justify=tk.LEFT)
        self.info_label.pack(fill=tk.X)
        
    def calcular(self):
        try:
            # Obtener valores
            base = self.base.get()
            altura = self.altura.get()
            
            # Validar que sean números positivos
            if base <= 0 or altura <= 0:
                messagebox.showerror("Error", "La base y la altura deben ser valores positivos")
                return
            
            # Calcular resultados
            hipotenusa = math.sqrt(base**2 + altura**2)
            perimetro = base + altura + hipotenusa
            area = (base * altura) / 2
            
            # Actualizar variables
            self.hipotenusa.set(hipotenusa)
            self.perimetro.set(perimetro)
            self.area.set(area)
            
            # Actualizar etiquetas
            self.hipotenusa_label.config(text=f"{hipotenusa:.2f} unidades")
            self.perimetro_label.config(text=f"{perimetro:.2f} unidades")
            self.area_label.config(text=f"{area:.2f} unidades²")
            
            # Actualizar información
            self.info_label.config(text=f"Triángulo rectángulo creado con base {base} y altura {altura}. "
                                     f"La hipotenusa es {hipotenusa:.2f}, el perímetro es {perimetro:.2f} "
                                     f"y el área es {area:.2f}.")
            
            # Dibujar el triángulo
            self.dibujar_triangulo(base, altura)
            
            # Crear objeto
            self.triangulo_actual = Triangulo(base, altura)
            
        except tk.TclError:
            messagebox.showerror("Error", "Los valores ingresados deben ser números")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def dibujar_triangulo(self, base, altura):
        # Limpiar canvas
        self.canvas.delete("all")
        
        # Dimensiones del canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Margen
        margin = 50
        
        # Escalar para que el triángulo ocupe el espacio disponible
        # manteniendo la proporción
        scale = min(
            (canvas_width - 2 * margin) / base,
            (canvas_height - 2 * margin) / altura
        )
        
        # Calcular las coordenadas escaladas
        scaled_base = base * scale
        scaled_altura = altura * scale
        
        # Puntos del triángulo (comenzando desde abajo izquierda)
        x1 = margin
        y1 = canvas_height - margin
        
        x2 = x1 + scaled_base
        y2 = y1
        
        x3 = x1
        y3 = y1 - scaled_altura
        
        # Dibujar el triángulo
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, 
                                fill="#e0f0ff", outline="#0077cc", width=2)
        
        # Dibujar líneas de referencia (punteadas)
        self.canvas.create_line(x3, y3, x2, y2, dash=(4, 2), fill="#ff6600", width=2)
        
        # Añadir etiquetas
        # Base
        self.canvas.create_text((x1 + x2) / 2, y1 + 15, 
                              text=f"Base: {base}", font=("Arial", 10))
        
        # Altura
        self.canvas.create_text(x1 - 15, (y1 + y3) / 2, 
                              text=f"Altura: {altura}", angle=90, font=("Arial", 10))
        
        # Hipotenusa
        hipotenusa = math.sqrt(base**2 + altura**2)
        self.canvas.create_text((x2 + x3) / 2 - 20, (y2 + y3) / 2 - 20, 
                              text=f"Hipotenusa: {hipotenusa:.2f}", angle=-math.degrees(math.atan(altura/base)), 
                              font=("Arial", 10))
        
        # Dibujar los ángulos
        radio = 30
        
        # Ángulo recto (90°)
        self.canvas.create_arc(x1 - radio, y1 - radio, x1 + radio, y1 + radio, 
                             start=0, extent=90, style="arc", outline="#ff0000", width=2)
        self.canvas.create_text(x1 + radio/2, y1 - radio/2, text="90°", font=("Arial", 8))
        
        # Calcular otros ángulos
        angulo_base = math.degrees(math.atan(altura/base))
        angulo_altura = 90 - angulo_base
        
        # Ángulo en la base
        self.canvas.create_arc(x2 - radio, y2 - radio, x2 + radio, y2 + radio, 
                             start=180 - angulo_base, extent=angulo_base, style="arc", outline="#ff0000", width=2)
        self.canvas.create_text(x2 - radio/2, y2 - radio/2, text=f"{angulo_altura:.1f}°", font=("Arial", 8))
        
        # Ángulo en la altura
        self.canvas.create_arc(x3 - radio, y3 - radio, x3 + radio, y3 + radio, 
                             start=270, extent=angulo_base, style="arc", outline="#ff0000", width=2)
        self.canvas.create_text(x3 + radio/2, y3 + radio/2, text=f"{angulo_base:.1f}°", font=("Arial", 8))

class Triangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
        self.hipotenusa = ((self.base ** 2 + self.altura ** 2) ** 0.5)
        self.perimetro = self.base + self.altura + self.hipotenusa
        self.area = (self.base * self.altura) / 2
        print(f"Constructor: se creó el triángulo con base {self.base}, altura {self.altura}")
        print(f"Constructor: hipotenusa {self.hipotenusa:.2f}, perímetro {self.perimetro:.2f}, área {self.area:.2f}")
    
    def mostrar_resultado1(self):
        print(f"El resultado del perímetro es {self.perimetro:.2f}")
        return self.perimetro
    
    def mostrar_resultado2(self):
        print(f"El resultado del área es {self.area:.2f}")
        return self.area
    
    def __del__(self):
        print(f"Destructor: se eliminó el triángulo con base {self.base} y altura {self.altura}")

def main():
    root = tk.Tk()
    app = TrianguloApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()