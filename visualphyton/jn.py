class CuentaBancaria:
    def __init__(self):
        self.__titular = input("Ingrese el nombre del titular: ")
        self.__saldo = float(input("Ingrese el saldo inicial: "))
        print("Cuenta creada correctamente.")

    # Getter del saldo
    def get_saldo(self):
        return self.__saldo

    # Setter del saldo
    def set_saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self.__saldo = nuevo_saldo
        else:
            print("Error: el saldo no puede ser negativo.")

    # Consultar saldo
    def consultar_saldo(self):
        print(f"Saldo actual de {self.__titular}: S/ {self.__saldo:.2f}")

    # Método para depositar dinero
    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            print(f"Depósito de S/ {monto:.2f} realizado con éxito.")
        else:
            print("El monto a depositar debe ser positivo.")

    # Método para retirar dinero
    def retirar(self, monto):
        if 0 < monto <= self.__saldo:
            self.__saldo -= monto
            print(f"Retiro de S/ {monto:.2f} realizado con éxito.")
        else:
            print("Saldo insuficiente o monto inválido.")

    # Mostrar toda la información
    def mostrar_informacion(self):
        print(f"Titular: {self.__titular}")
        print(f"Saldo actual: S/ {self.__saldo:.2f}")


# Programa principal
cuenta = CuentaBancaria()

while True:
    print("\nSeleccione una opción:")
    print("1. Depositar dinero")
    print("2. Retirar dinero")
    print("3. Mostrar información")
    print("4. Salir")

    opcion = input("Ingrese opción: ")

    if opcion == "1":
        monto = float(input("Ingrese monto a depositar: "))
        cuenta.depositar(monto)
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
