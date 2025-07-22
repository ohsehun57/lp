from abc import ABC, abstractmethod
import math

class Figura(ABC):
    @abstractmethod
    def calcular_area(self):
        pass

class Cuadrado(Figura):
    def __init__(self, lado):
        if lado <= 0:
            raise ValueError("El lado debe ser mayor que cero")
        self.lado = lado

    def calcular_area(self):
        return self.lado**2

class Triangulo(Figura):
    def __init__(self, base, altura):
        if base <= 0 or altura <= 0:
            raise ValueError("Base y altura deben ser mayores que cero")
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return (self.base * self.altura) / 2

class Rectangulo(Figura):
    def __init__(self, base, altura):
        if base <= 0 or altura <= 0:
            raise ValueError("Base y altura deben ser mayores que cero")
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

class Circulo(Figura):
    def __init__(self, radio):
        if radio <= 0:
            raise ValueError("El radio debe ser mayor que cero")
        self.radio = radio

    def calcular_area(self):
        return math.pi * self.radio**2

def calcular_area_figura():
    try:
        figura = input("Ingrese cuadrado, triangulo, rectangulo o circulo: ").lower()
        if figura == "cuadrado":
            lado = float(input("Lado del cuadrado: "))
            c = Cuadrado(lado)
            print("Área del cuadrado:", c.calcular_area())
        elif figura == "triangulo":
            base = float(input("Base del triángulo: "))
            altura = float(input("Altura del triángulo: "))
            t = Triangulo(base, altura)
            print("Área del triángulo:", t.calcular_area())
        elif figura == "rectangulo":
            base = float(input("Base del rectángulo: "))
            altura = float(input("Altura del rectángulo: "))
            r = Rectangulo(base, altura)
            print("Área del rectángulo:", r.calcular_area())
        elif figura == "circulo":
            radio = float(input("Radio del círculo: "))
            ci = Circulo(radio)
            print("Área del círculo:", ci.calcular_area())
        else:
            print("Figura no reconocida")
    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

# Ejecutar la función
calcular_area_figura()
