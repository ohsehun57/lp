class calculadorabasica:
    def __init__(self,numero1,numero2):
        self.__numero1 = numero1 
        self.__numero2 = numero2
#getter
    def obtener_numero1 (self):
        return self.__numero1
    def obtener_numero2 (self):
        return self.__numero2
#ssetters:
    def establecer_numero1 (self,nuevo_valor):
        self.__numero1 = nuevo_valor 
    def establecer_numero2 (self,nuevo_valor):
        self.__numero2 = nuevo_valor 
#opercaiones 
    def suma (self):
        return self.__numero1 + self.__numero2
    
    def resta (self):
        return self.__numero1 - self.__numero2
    
    def multiplicacion (self):
        return self.__numero1 * self.__numero2
    
    def division (self):

        if self.__numero2 != 0:
            return self.__numero1 / self.__numero2
        else:
            return "error:division entre cero"
    
    def mostrar_resultado (self):
        print(f"numero1:{self.__numero1}")
        print(f"numero2:{self.__numero2}")
        print(f"la suma es :{self.suma()}")
        print(f"la resta es :{self.resta()}")
        print(f"la multiplicacion es :{self.multiplicacion()}")
        print(f"la division es :{self.division()}")
# uso de a clase calculador basica
try:

    a=int(input(f"ingrese el numero 1 : "))
    b=int(input(f"ingrese el numero 2 : "))
    calcula = calculadorabasica(a,b)
    calcula.mostrar_resultado()

    print("\n cambiando valores")
    
    c=float(input(f"ingrese el nuevo valor numero 1 : "))
    d=float(input(f"ingrese el nuevo valor numero 2 : "))
    calcula.establecer_numero1(c)
    calcula.establecer_numero2(d)
    calcula.mostrar_resultado()


except ValueError:
    print("error: ingrese un numero valido")    