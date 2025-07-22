"""class Suma:
    def __init__(self):
        self.a = int(input("ingrese el vlor de a :"))
        self.b = int(input("ingrese el vlor de b :"))
        self.resultado = self.a + self.b
        print(f"construtctor :se creo la suma de {self.a} + {self.b} = {self.resultado}")

    def mostrar_resultado(self):
        print(f"el resulado de la suma es {self.resultado}")

    def __del__(self):
        print(f"destructor: se elimino la suma de {self.a} + {self.b}")

suma = Suma()
suma.mostrar_resultado()
suma.__del__()
yo ise 
class Triangulo:
    def __init__(self):
        self.a = int(input("ingrese el vlor de base :"))
        self.b = int(input("ingrese el vlor de altiura :"))
        self.perimetro = ((((self.a **2)+(self.b **2))**0.5))+self.a+self.b
        self.area = (self.a * self.b)/2
        print(f"construtctor :se creo el perimetro de {self.a}*{self.b} = {self.perimetro}")
        print(f"construtctor :se creo el area de {self.a}/{self.b} = {self.area}")

    def mostrar_resultado1(self):
        print(f"el resulado de el perimetro es {self.perimetro}")
    def mostrar_resultado2(self):
        print(f"el resulado de el area es {self.area}")

    def __del1__(self):
        print(f"destructor: se elimino el perimetro de {self.a} * {self.b}")
    def __del2__(self):
        print(f"destructor: se elimino el area de {self.a} / {self.b}")

suma = Triangulo()
suma.mostrar_resultado1()
suma.mostrar_resultado2()
suma.__del1__()
suma.__del2__()

#esto es de agureea

class Triangulo:
    def __init__(self):
        self.base = int(input("Ingrese el valor de la base: "))
        self.altura = int(input("Ingrese el valor de la altura: "))
        # Se asume triángulo rectángulo: perimetro = base + altura + hipotenusa
        self.hipotenusa = ((self.base ** 2 + self.altura ** 2) ** 0.5)
        self.perimetro = self.base + self.altura + self.hipotenusa
        self.area = (self.base * self.altura) / 2

        print(f"Constructor: se creó el perímetro con lados {self.base}, {self.altura}, hipotenusa {self.hipotenusa:.2f} = {self.perimetro:.2f}")
        print(f"Constructor: se creó el área = ({self.base} * {self.altura}) / 2 = {self.area:.2f}")

    def mostrar_resultado1(self):
        print(f"El resultado del perímetro es {self.perimetro:.2f}")

    def mostrar_resultado2(self):
        print(f"El resultado del área es {self.area:.2f}")

    def __del__(self):
        print(f"Destructor: se eliminó el triángulo con base {self.base} y altura {self.altura}")

# Crear objeto y mostrar resultados
triangulo = Triangulo()
triangulo.mostrar_resultado1()
triangulo.mostrar_resultado2()
# El destructor se llama automáticamente al final o cuando se elimina el objeto.
"""

