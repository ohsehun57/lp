"""
#pitagoras cle

import sys
import math

class pitqgoras:
    def __init__(self,c1,c2):
        self.c1=c1
        self.c2=c2

    def calcular_hipotenusa(self):
        return math.sqrt(self.c1**2 +self.c2**2)
t1 =pitqgoras(3,4)
print(f"hipotenusa{t1.calcular_hipotenusa()}")
print(f"tamaño en memoria(bytes)")
tamaño_objeto=sys.getsizeof(t1)
tamaño_objeto1=sys.getsizeof(t1.c1)
tamaño_objeto2=sys.getsizeof(t1.c2)
tam_metodo=sys.getsizeof(t1.calcular_hipotenusa)
tam_tamaño_class=sys.getsizeof(pitqgoras)


print(f"objeto triangulo:  {tamaño_objeto} bytes")
print(f"objeto c1:  {tamaño_objeto1} bytes")
print(f"objeto c2:  {tamaño_objeto2} bytes")
print(f"metodo calcular_hipotenusa:  {tam_metodo} bytes")
print(f"clase :  {tam_tamaño_class} bytes")

suma_total = tamaño_objeto + tamaño_objeto1 + tamaño_objeto2 + tam_metodo + tam_tamaño_class

print(f"suma total del total de la memoria :{suma_total} bytes ")

"""
#triangulo rectangulo

import sys
import math

class triangulo:
    def __init__(self,base,altura):
        self.base=base
        self.altura=altura

    def calcular_area(self):
        return (self.base * self.altura)/2
    
    def calcular_hipotenusa(self):
        return math.sqrt(self.base**2 +self.altura**2)
    
    def calcular_perimetro(self):
        return (self.base + self.altura + self.calcular_hipotenusa())


t1 =triangulo(3,4)
print(f"hipotenusa : {t1.calcular_hipotenusa()}")
print(f"area : {t1.calcular_area()}")
print(f"perimetro : {t1.calcular_perimetro()}")
print(f"tamaño en memoria(bytes)")

tamaño_objeto=sys.getsizeof(t1)
tamaño_objeto1=sys.getsizeof(t1.base)
tamaño_objeto2=sys.getsizeof(t1.altura)
tam_metodo=sys.getsizeof(t1.calcular_hipotenusa)
tam_metodo1=sys.getsizeof(t1.calcular_area)
tam_metodo2=sys.getsizeof(t1.calcular_perimetro)
tam_tamaño_class=sys.getsizeof(triangulo)


print(f"objeto triangulo:  {tamaño_objeto} bytes")
print(f"objeto base:  {tamaño_objeto1} bytes")
print(f"objeto altura:  {tamaño_objeto2} bytes")
print(f"metodo calcular_hipotenusa:  {tam_metodo} bytes")
print(f"metodo calcular_area:  {tam_metodo1} bytes")
print(f"metodo calcular_perimetro:  {tam_metodo2} bytes")
print(f"clase :  {tam_tamaño_class} bytes")

suma_total = tamaño_objeto + tamaño_objeto1 + tamaño_objeto2 + tam_metodo + tam_metodo1 + tam_metodo2 + tam_tamaño_class

print(f"suma total del total de la memoria :{suma_total} bytes ")
