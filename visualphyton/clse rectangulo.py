class rectangulo:
    def __init__(self,base,altura):
        self._base = base
        self._altura= altura
    
    def area(self):
        return self._base*self._altura
    def perimetro(self):
        return ((self._altura)*2 + (self._base)*2)
    def mostrar(self):
        print(f"la base es:{self._base}")
        print(f"la altura es :{self._altura}")
        print(f"el area es :{self.area()}")
        print(f"el perimetro es :{self.perimetro()}")

#uso de setter
    def establecer_base(self,nueva_base):
        if nueva_base > 0 :
            self._base=nueva_base
        else:
            print("numero no valida")

    def establecer_altura(self,nueva_altura):
        if nueva_altura > 0 :
            self._altura=nueva_altura
        else:
            print("numero no valida")

    
resultado1 = rectangulo(5, 3)
resultado1.mostrar()
print("\nnueva altura y nueva base ")
resultado1.establecer_base(-5)
resultado1.establecer_altura(0)
resultado1.mostrar()






