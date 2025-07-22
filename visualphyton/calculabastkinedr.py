import tkinter as tk
from tkinter import ttk
import math

class CalculadoraTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#e0e0e0")
        
        # Variables
        self.expresion = ""
        self.resultado_actual = "0"
        self.mostrar_texto = tk.StringVar(value="0")
        self.operacion_anterior = ""
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear widgets
        self.crear_widgets()
    
    def configurar_estilo(self):
        self.estilo = ttk.Style()
        self.estilo.configure('TFrame', background='#e0e0e0')
        self.estilo.configure('Display.TLabel', 
                             font=('Arial', 24, 'bold'), 
                             background='#f8f8f8',
                             foreground='#333333', 
                             anchor='e',
                             padding=10)
        
        # Estilos de botones
        self.estilo.configure('Numero.TButton', 
                             font=('Arial', 14, 'bold'),
                             padding=5)
        
        self.estilo.configure('Operacion.TButton', 
                             font=('Arial', 14, 'bold'),
                             background='#f0ad4e',
                             padding=5)
        
        self.estilo.configure('Igual.TButton', 
                             font=('Arial', 14, 'bold'),
                             background='#5cb85c',
                             padding=5)
        
        self.estilo.configure('Limpiar.TButton', 
                             font=('Arial', 14, 'bold'),
                             background='#d9534f',
                             padding=5)
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pantalla
        pantalla_frame = ttk.Frame(main_frame)
        pantalla_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pantalla = ttk.Label(pantalla_frame, 
                                textvariable=self.mostrar_texto, 
                                style='Display.TLabel',
                                width=20)
        self.pantalla.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de filas y columnas
        for i in range(6):
            botones_frame.rowconfigure(i, weight=1)
        for i in range(4):
            botones_frame.columnconfigure(i, weight=1)
        
        # Primera fila - Botones especiales
        self.crear_boton('C', 0, 0, botones_frame, self.limpiar, 'Limpiar.TButton')
        self.crear_boton('⌫', 0, 1, botones_frame, self.borrar_ultimo, 'Operacion.TButton')
        self.crear_boton('±', 0, 2, botones_frame, self.cambiar_signo, 'Operacion.TButton')
        self.crear_boton('√', 0, 3, botones_frame, lambda: self.operacion_especial('sqrt'), 'Operacion.TButton')
        
        # Segunda fila
        self.crear_boton('7', 1, 0, botones_frame, lambda: self.presionar_numero('7'), 'Numero.TButton')
        self.crear_boton('8', 1, 1, botones_frame, lambda: self.presionar_numero('8'), 'Numero.TButton')
        self.crear_boton('9', 1, 2, botones_frame, lambda: self.presionar_numero('9'), 'Numero.TButton')
        self.crear_boton('÷', 1, 3, botones_frame, lambda: self.presionar_operacion('/'), 'Operacion.TButton')
        
        # Tercera fila
        self.crear_boton('4', 2, 0, botones_frame, lambda: self.presionar_numero('4'), 'Numero.TButton')
        self.crear_boton('5', 2, 1, botones_frame, lambda: self.presionar_numero('5'), 'Numero.TButton')
        self.crear_boton('6', 2, 2, botones_frame, lambda: self.presionar_numero('6'), 'Numero.TButton')
        self.crear_boton('×', 2, 3, botones_frame, lambda: self.presionar_operacion('*'), 'Operacion.TButton')
        
        # Cuarta fila
        self.crear_boton('1', 3, 0, botones_frame, lambda: self.presionar_numero('1'), 'Numero.TButton')
        self.crear_boton('2', 3, 1, botones_frame, lambda: self.presionar_numero('2'), 'Numero.TButton')
        self.crear_boton('3', 3, 2, botones_frame, lambda: self.presionar_numero('3'), 'Numero.TButton')
        self.crear_boton('-', 3, 3, botones_frame, lambda: self.presionar_operacion('-'), 'Operacion.TButton')
        
        # Quinta fila
        self.crear_boton('0', 4, 0, botones_frame, lambda: self.presionar_numero('0'), 'Numero.TButton', columnspan=2)
        self.crear_boton('.', 4, 2, botones_frame, lambda: self.presionar_punto(), 'Numero.TButton')
        self.crear_boton('+', 4, 3, botones_frame, lambda: self.presionar_operacion('+'), 'Operacion.TButton')
        
        # Sexta fila
        self.crear_boton('%', 5, 0, botones_frame, lambda: self.presionar_operacion('%'), 'Operacion.TButton')
        self.crear_boton('x²', 5, 1, botones_frame, lambda: self.operacion_especial('sqr'), 'Operacion.TButton')
        self.crear_boton('1/x', 5, 2, botones_frame, lambda: self.operacion_especial('inv'), 'Operacion.TButton')
        self.crear_boton('=', 5, 3, botones_frame, self.calcular_resultado, 'Igual.TButton')
        
        # Bindear eventos de teclado
        self.root.bind('<Key>', self.presionar_tecla)
    
    def crear_boton(self, texto, fila, columna, frame, comando, estilo, columnspan=1):
        boton = ttk.Button(frame, text=texto, command=comando, style=estilo)
        boton.grid(row=fila, column=columna, padx=3, pady=3, sticky='nsew', columnspan=columnspan)
        return boton
    
    def presionar_numero(self, numero):
        if self.resultado_actual == "0" or self.resultado_actual == "Error":
            self.resultado_actual = numero
        else:
            self.resultado_actual += numero
        self.actualizar_pantalla()
    
    def presionar_punto(self):
        if "." not in self.resultado_actual:
            self.resultado_actual += "."
            self.actualizar_pantalla()
    
    def presionar_operacion(self, operacion):
        if self.resultado_actual != "Error":
            # Si ya tenemos una expresión, calcular primero
            if self.expresion:
                self.calcular_resultado()
            
            # Guardar la expresión actual
            self.expresion = self.resultado_actual + operacion
            self.resultado_actual = "0"
            self.actualizar_pantalla()
    
    def calcular_resultado(self):
        if not self.expresion or self.resultado_actual == "Error":
            return
        
        try:
            # Formar la expresión completa
            expresion_completa = self.expresion + self.resultado_actual
            
            # Tratar el caso especial del porcentaje
            if self.expresion[-1] == '%':
                num1 = float(self.expresion[:-1])
                num2 = float(self.resultado_actual)
                resultado = num1 * num2 / 100
            else:
                # Evaluar la expresión
                resultado = eval(expresion_completa)
            
            # Mostrar resultado
            if resultado == int(resultado):
                self.resultado_actual = str(int(resultado))
            else:
                self.resultado_actual = str(resultado)
            
            self.expresion = ""
            self.actualizar_pantalla()
        except Exception as e:
            self.resultado_actual = "Error"
            self.expresion = ""
            self.actualizar_pantalla()
    
    def operacion_especial(self, tipo):
        if self.resultado_actual == "Error":
            return
        
        try:
            num = float(self.resultado_actual)
            
            if tipo == 'sqrt':
                if num >= 0:
                    resultado = math.sqrt(num)
                else:
                    raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
            elif tipo == 'sqr':
                resultado = num ** 2
            elif tipo == 'inv':
                if num != 0:
                    resultado = 1 / num
                else:
                    raise ValueError("No se puede dividir por cero")
            
            # Formatear resultado
            if resultado == int(resultado):
                self.resultado_actual = str(int(resultado))
            else:
                self.resultado_actual = str(resultado)
            
            self.actualizar_pantalla()
        except Exception as e:
            self.resultado_actual = "Error"
            self.actualizar_pantalla()
    
    def cambiar_signo(self):
        if self.resultado_actual != "0" and self.resultado_actual != "Error":
            if self.resultado_actual[0] == '-':
                self.resultado_actual = self.resultado_actual[1:]
            else:
                self.resultado_actual = '-' + self.resultado_actual
            self.actualizar_pantalla()
    
    def limpiar(self):
        self.expresion = ""
        self.resultado_actual = "0"
        self.actualizar_pantalla()
    
    def borrar_ultimo(self):
        if self.resultado_actual != "Error":
            if len(self.resultado_actual) > 1:
                self.resultado_actual = self.resultado_actual[:-1]
            else:
                self.resultado_actual = "0"
            self.actualizar_pantalla()
    
    def actualizar_pantalla(self):
        self.mostrar_texto.set(self.resultado_actual)
    
    def presionar_tecla(self, evento):
        key = evento.char
        
        # Números
        if key in '0123456789':
            self.presionar_numero(key)
        # Operaciones
        elif key == '+':
            self.presionar_operacion('+')
        elif key == '-':
            self.presionar_operacion('-')
        elif key == '*':
            self.presionar_operacion('*')
        elif key == '/':
            self.presionar_operacion('/')
        elif key == '%':
            self.presionar_operacion('%')
        elif key == '.':
            self.presionar_punto()
        elif evento.keysym == 'Return':
            self.calcular_resultado()
        elif evento.keysym == 'BackSpace':
            self.borrar_ultimo()
        elif evento.keysym == 'Escape':
            self.limpiar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraTkinter(root)
    root.mainloop()