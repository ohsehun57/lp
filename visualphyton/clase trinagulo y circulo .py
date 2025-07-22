"""class pitagoras:
    def __init__(self,cateto1,cateto2):
        self._cateto1 = cateto1
        self._cateto2= cateto2
    
    def hipotenusa(self):
        return (self._cateto1**2+self._cateto2**2)**0.5

    def mostrar(self):
        print(f"el cateto 1  es:{self._cateto1}")
        print(f"el cateto2  es :{self._cateto2}")
        print(f"la hipotenusa es:{self.hipotenusa()}")

#uso de setter

    def establecer_cateto1 (self,nuevo_cateto1):
        if nuevo_cateto1 > 0 :
            self._cateto1=nuevo_cateto1
        else:
            print("numero no valida")

    def establecer_cateto2(self,nuevo_cateto2):
        if nuevo_cateto2 > 0 :
            self._cateto2=nuevo_cateto2
        else:
            print("numero no valida")
    
resultado1 = pitagoras(3, 4)
resultado1.mostrar()

print("\nnueva altura y nueva base ")
resultado1.establecer_cateto1(8)
resultado1.establecer_cateto2(7)
resultado1.mostrar()
"""


import math
class circulo:
    def __init__(self,radio):
        self._radio = radio
    
    def area(self):
        return (math.pi*(self._radio**2))
    def perimetro(self):
        return(math.pi*(self._radio*2))

    def mostrar(self):
        print(f"el radio  es:{self._radio}")
        print(f"el area es:{self.area()}")
        print(f"el perimetro es:{self.perimetro()}")

#uso de setter

    def establecer_radio (self,nuevo_radio):
        if nuevo_radio > 0 :
            self._radio=nuevo_radio
        else:
            print("numero no valida")
    
resultado1 = circulo(4)
resultado1.mostrar()

print("\nnuevo radio  ")

resultado1.establecer_radio(6)

resultado1.mostrar()