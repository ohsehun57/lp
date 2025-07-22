"""class Persona:
    def __init__(self,nombre):

        self.nombre=nombre

p1= Persona("maria")

p2=p1

p2.nombre="carla"

print(p1.nombre)


class Producto:
    def __init__(self,precio):
        self.precio=precio
    
    def aplicar_descuento(self,porcentaje):
        self.precio -=self.precio*(porcentaje/100)


p= Producto(100)

p.aplicar_descuento(10)

print(p.precio)





class ciudad:
    def __init__(self,nombre,x,y):
        self.nombre = nombre
        self.x=x
        self.y=y
    

    def distancia(self,otra_ciudad):
        dx = self.x - otra_ciudad.x
        dy = self.y - otra_ciudad.y
        return (dx**2 + dy**2)**0.5
    
nombre1 = input("ingrese su punto de partida")
x1 = int(input("ingrese la coordenada 1: "))
y1 = int(input("ingrese la coordenada 2: "))

nombre2 = input("ingrese su punto de llegada: ")
x2 = int(input("ingrese la coordenada  "))
y2 = int(input("ingrese la coordenada 2 "))

ciudad1 = ciudad(nombre1,x1,y1)
ciudad2 = ciudad(nombre2,x2,y2)

distancia_km = ciudad1.distancia(ciudad2)

print(f"dstancia entre {ciudad1.nombre} y {ciudad2.nombre}: {distancia_km:.2f} unidades")




class rectangulo:
    def __init__(self,base,altura,color):
        self.base=base
        self.altura=altura
        self.color=color

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2*self.base + 2*self.altura

    def mostrar(self):
        print(f"el rectangulo de base :{self.base} y altura:{self.altura} y color  :{self.color}")
  
resultado1 = rectangulo(10,6,"verde")
resultado2 = rectangulo(7,3,"naranja")
referencia1 =resultado1
referencia2 =resultado2
referencia1.mostrar()
print(f"area:{referencia1.calcular_area()} y perimetro:{referencia1.calcular_perimetro()}")
referencia2.mostrar()
print(f"area:{referencia2.calcular_area()} y perimetro:{referencia2.calcular_perimetro()}")



class rectangulo:
    def __init__(self,base,altura,color):
        self.base=base
        self.altura=altura
        self.color=color

    def calcular_area(self):
        return self.base * self.altura

    def calcular_perimetro(self):
        return 2*self.base + 2*self.altura

    def mostrar(self):
        print(f"el rectangulo de base :{self.base} y altura:{self.altura} y color  :{self.color}")
        print(f"area{self.calcular_area()} y perimetro: {self.calcular_perimetro()}")

class cuadrado (rectangulo):

    def __init__(self,lado,color):
        super() .__init__(lado,lado,color)
    def mostrar(self):
        print(f"\n cuadrado de lado :{self.base}  y color  :{self.color}")
        print(f"area{self.calcular_area()} y perimetro: {self.calcular_perimetro()}")


resultado1 = rectangulo(10,6,"verde")
resultado2 = cuadrado(7,"naranja")
referencia1 =resultado1
referencia2 =resultado2
referencia1.mostrar()
referencia2.mostrar()
"""


import math


class Figuras:
    def __init__(self, color):
        self.color = color

class circulo(Figuras):
    def __init__(self, radio, color):
        super().__init__(color)
        self.radio = radio

    def calcular_area(self):
        return math.pi * (self.radio ** 2)

    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

    def mostrar(self):
        print(f"\n el círculo de radio: {self.radio} y color: {self.color}")
        print(f"area{self.calcular_area()} y perimetro: {self.calcular_perimetro()}")

referncia1 = circulo(7, "naranja")
referncia1.mostrar()
        



