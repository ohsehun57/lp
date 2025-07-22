"""#clase 1 figura 
class figura:
    def __init__(self,nombre):
        self.nombre = nombre
    def mostrar_nombre(self):
        print(f"el nombre de la figura es:{self.nombre}")
#clase 2 color 
class color:
    def __init__(self,color):
        self.color = color
    def nombre_color(self):
        print(f"el color es:{self.color}")
        
#clase 3 dimension
class dimension:
    def __init__(self,base,altura):
        self.base = base
        self.altura = altura
    def mostrar_dimension (self)
        print (f"la base es : {self.base}")
        print (f"la altura  es : {self.altura}")

#clase 4 cuadrado(fuhura color y dimencion)




















#clase base 1
class Base:
    def __init__(self,base):
        self.base = base 

#clase base 2
class Altura:
    def __init__(self,altura):
        self.altura = altura

#clase hija hereda de base y altura

class triangulo(Base,Altura):
    def __init__(self,base,altura):
        Base.__init__(self,base)
        Altura.__init__(self,altura)
    def area(self):
        return (self.base * self.altura)/2
    
trian = triangulo(10,5)
print(f"base es : {trian.base}")
print(f"altura es : {trian.altura}")
print(f"el area del triangulo es  : {trian.area()} unidades al cuadrado")

"""

#clase base : figura 
class figura:
    def __init__(self,nombre):
        self.nombre=nombre
    def mostrar_nombre(self):
        print(f"la figura es :{self.nombre}")

#sub clase 1:cuadrado
class cuadrado(figura):
    def __init__(self,lado):
        super().__init__("cuadrado")
        self.lado =lado
    def area(self):
        return self.lado**2

#sub clase 2:triangulo
class triangulo(figura):
    def __init__(self,base,altura):
        super().__init__("triangulo")
        self.base=base
        self.altura=altura
    def area(self):
        return (self.base* self.altura)/2


#sub clase 3:circulo
class circulo(figura):
    def __init__(self,radio):
        super().__init__("circulo")
        self.radio=radio
    def area(self):
        return (3.14*self.radio**2)
    
figuras = [cuadrado(4),triangulo(3,4),circulo(5)]

for figura in figuras:
    figura.mostrar_nombre()

    print(f"area es: {figura.area()} unidades cuadradas\n")