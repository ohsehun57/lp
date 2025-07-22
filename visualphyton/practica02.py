from abc import ABC, abstractmethod
import math

# Interfaz base (S, L, I, D)

class FiguraGeometrica(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass
# Clases concretas (S, L, O)

class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio

    def descripcion(self):
        return f"Círculo de radio {self.radio}"


class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2

    def perimetro(self):
        return 4 * self.lado

    def descripcion(self):
        return f"Cuadrado de lado {self.lado}"


class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)

    def descripcion(self):
        return f"Rectángulo de base {self.base} y altura {self.altura}"


class Triangulo(FiguraGeometrica):
    def __init__(self, lado1, lado2, lado3, base, altura):
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3
        self.base = base
        self.altura = altura

    def area(self):
        return (self.base * self.altura) / 2

    def perimetro(self):
        return self.lado1 + self.lado2 + self.lado3

    def descripcion(self):
        return f"Triángulo con lados {self.lado1}, {self.lado2}, {self.lado3}, base {self.base}, altura {self.altura}"


# Clase Visualizadora (S, D)
# Lista de objetos FiguraGeometrica
class VisualizadorFiguras:
    def __init__(self, figuras):
        self.figuras = figuras  

    def mostrar_figuras(self):
        for figura in self.figuras:
            print("------")
            print(figura.descripcion())
            print(f"Área: {figura.area():.2f}")
            print(f"Perímetro: {figura.perimetro():.2f}")
            print("------\n")

# Simulación de uso

if __name__ == "__main__":
    figuras = [
        Circulo(5),
        Cuadrado(4),
        Rectangulo(3, 6),
        Triangulo(3, 4, 5, 4, 3)
    ]

    visualizador = VisualizadorFiguras(figuras)
    visualizador.mostrar_figuras()
