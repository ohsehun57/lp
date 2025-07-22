"""class Rectangulo:
    def __init__(self):
        self.longitud = int(input("Ingrese la longitud: "))
        self.ancho = int(input("Ingrese el ancho: "))
        self.perimetro = ((self.longitud)*2 + (self.ancho)*2)
        self.area = (self.longitud * self.ancho)
        print(f"Constructor: Rectangulo creado con longitud {self.longitud:.1f} y ancho {self.ancho:.1f}")
    def mostrar_resultado1(self):
        print(f"El resultado del perímetro es {self.perimetro:.1f}")
    def mostrar_resultado2(self):
        print(f"El resultado del área es {self.area:.1f}")
    def __del__(self):
        print(f"Destructor: Rectangulo eliminado")
triangulo = Rectangulo()
triangulo.mostrar_resultado1()
triangulo.mostrar_resultado2()
triangulo.__del__()
"""

class cuenta_bancaria:
    def __init__(self):
        self.__titular = (input("Ingrese el nombre del titular: "))
        self.__saldo_inicial = float(input("ingrese el saldo inicial"))
    def consultar_saldo(self):
        print(f"saldo actual de {self.__titular}: s/ {self.__saldo_inicial: .2f}")

    def nuevo_saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self._saldo = nuevo_saldo
        else:
            print("Error: el saldo no puede ser negativo.")

    def depositar_cash(self,monto):
        if monto>0:
            self.__saldo_inicial+=monto
            print(f"deposito de s/. {monto: .2f} realizado con exito")
        else:
            print("el monto ha realizar debe ser positivo")

    def retirar(self,monto):
        if 0 < monto <=self.__saldo_inicial:
            self.__saldo_inicial-=monto
            print(f"retiro de s/, {monto: .2f} realizado con exito.")
        else:
            print("saldo insuficiente o monto invalido")

    def mostrar_informacion(self):
        print(f"Titular: {self.__titular}")
        print(f"Saldo actual: {self.__saldo_inicial:.2f}")

cuenta = cuenta_bancaria()

while True:
    print("\nSeleccione una opción:")
    print("1. Depositar dinero")
    print("2. Retirar dinero")
    print("3. Mostrar información")
    print("4. Salir")

    opcion = input("Ingrese opción: ")

    if opcion == "1":
        monto = float(input("Ingrese monto a depositar: "))
        cuenta.depositar_cash(monto)
    elif opcion == "2":
        monto = float(input("Ingrese monto a retirar: "))
        cuenta.retirar(monto)
    elif opcion == "3":
        cuenta.mostrar_informacion()
    elif opcion == "4":
        print("Gracias por usar el sistema.")
        break
    else:
        print("Opción inválida.")
