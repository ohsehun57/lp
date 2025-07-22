# Clase base: Empleado
class Empleado:
    def __init__(self, nombre, dni, salario_base):
        self.nombre = nombre
        self.dni = dni
        self.salario_base = salario_base

    def calcular_salario(self):
        pass  # Método polimórfico

    def calcular_impuesto(self):
        return self.calcular_salario() * 0.10  # 10% de impuesto

    def obtener_info(self):
        pass  # Método polimórfico


# Subclase: Administrativo
class Administrativo(Empleado):
    def __init__(self, nombre, dni, salario_base):
        super().__init__(nombre, dni, salario_base)
        self.__salario_base = salario_base  # Encapsulamiento

    def get_salario_base(self):
        return self.__salario_base

    def calcular_salario(self):
        return self.__salario_base

    def obtener_info(self):
        salario = self.calcular_salario()
        impuesto = self.calcular_impuesto()
        salario_neto = salario - impuesto
        return (
            f"Administrativo - Nombre: {self.nombre}, DNI: {self.dni}, "
            f"Salario Bruto: {salario}, Impuesto (10%): {impuesto}, "
            f"Salario Neto: {salario_neto}"
        )


# Subclase: Operario
class Operario(Empleado):
    def __init__(self, nombre, dni, salario_base, bono_produccion):
        super().__init__(nombre, dni, salario_base)
        self.__bono_produccion = bono_produccion  # Encapsulamiento

    def get_bono_produccion(self):
        return self.__bono_produccion

    def calcular_salario(self):
        return self.salario_base + self.__bono_produccion

    def obtener_info(self):
        salario = self.calcular_salario()
        impuesto = self.calcular_impuesto()
        salario_neto = salario - impuesto
        return (
            f"Operario - Nombre: {self.nombre}, DNI: {self.dni}, "
            f"Salario Bruto: {salario}, Impuesto (10%): {impuesto}, "
            f"Salario Neto: {salario_neto}"
        )


# Menú Principal
def main():
    lista_empleados = []

    while True:
        print("\n****** SISTEMA DE EMPLEADOS ******")
        print("1. Registrar Administrativo")
        print("2. Registrar Operario")
        print("3. Mostrar Empleados")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            dni = input("DNI: ")
            salario_base = float(input("Salario base: "))
            admin = Administrativo(nombre, dni, salario_base)
            lista_empleados.append(admin)
            print("Administrativo registrado correctamente.")

        elif opcion == '2':
            nombre = input("Nombre: ")
            dni = input("DNI: ")
            salario_base = float(input("Salario base: "))
            bono = float(input("Bono de producción: "))
            operario = Operario(nombre, dni, salario_base, bono)
            lista_empleados.append(operario)
            print("Operario registrado correctamente.")

        elif opcion == '3':
            if not lista_empleados:
                print("No hay empleados registrados.")
            else:
                print("\nListado de Empleados:")
                for idx, empleado in enumerate(lista_empleados):
                    print(f"{idx+1}. {empleado.obtener_info()}")

        elif opcion == '4':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


# Ejecutar programa
if __name__ == "__main__":
    main()
