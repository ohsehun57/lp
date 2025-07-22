"""#clase base o interfaz
class curso:
    def clacular_nota_final(self):
        pass
#clase son comportaientos diferentes
class cursoteorico(curso):
    def __init__(self,examen,tareas):
     self.examen=examen
     self.tareas=tareas
    def calcular_nota_final(self):
        return 0.7 * self.examen + 0.3 * self.tareas

class cursopractico(curso):
    def __init__(self,practicas,asistencia):
      self.asistencia=asistencia
      self.practicas=practicas
    def calcular_nota_final(self):
       return 0.8 * self.practicas + 0.2 * self.asistencia
class cursoproyecto(curso):
    def __init__(self,exposicion,proyecto):
      self.exposicion=exposicion
      self.proyecto=proyecto
    def calcular_nota_final(self):
      return 0.6 * self.proyecto + 0.4 * self.exposicion
   
#uso polimorfico
cursos = [cursoteorico(examen=16,tareas=18),
          cursopractico(practicas=17,asistencia=19),
          cursoproyecto(exposicion=17,proyecto=18)]
for curso in cursos:
   print("nota final",curso.calcular_nota_final())





import math

# 1. Clase interfaz
class Figura:
    def dibujar_figura(self):
        print("No se puede dibujar una figura geométrica.")

# 2. Clases concretas con comportamientos diferentes
class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def dibujar_figura(self):
        for _ in range(self.lado):
            print("▄ " * self.lado)

class Triangulo(Figura):
    def __init__(self, altura):
        self.altura = altura

    def dibujar_figura(self):
        for i in range(1, self.altura + 1):
            print("▲ " * i)

class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def dibujar_figura(self):
        for _ in range(self.radio):
            print("⚫"+" "*(self.radio)+"⚫")
# 3. Uso de polimorfismo
figuras = [
    Cuadrado(3),
    Triangulo(4),
    Circulo(5)
]

for figura in figuras:
    print("Figura:",figura.dibujar_figura())
"""


# 1. Clase interfaz
class Figura:
    def calcular_figura(self):
        print("no se puede calcular el perimetro")

# 2. Clases concretas con comportamientos diferentes
class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado
    def calcular_figura(self):
        return 4 * self.lado
class Triangulo(Figura):
    def __init__(self, altura,base):
        self.altura = altura
        self.base = base
    def calcular_figura(self):
        return self.base + self.altura + (self.base**2+self.altura**2)**0.5
class Rectangulo(Figura):
    def __init__(self, altura,base):
        self.altura = altura
        self.base = base
    def calcular_figura(self):
        return 2*self.base + 2*self.altura
class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio

    def calcular_figura(self):
        return 3.1416*2*self.radio
# 3. Uso de polimorfismo
figuras = [
    Cuadrado(5),
    Triangulo(5,4),
    Rectangulo(4,7),
    Circulo(3)
]

for figura in figuras:
    print("el perimetro es:",figura.calcular_figura())


