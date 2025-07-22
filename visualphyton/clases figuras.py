import math

# Clase base (superclase)
class Figura:
    def __init__(self, nombre):
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

    def calcular_area(self):
        pass

    def calcular_perimetro(self):
        pass

    def mostrar_info(self):
        print(f"\nFigura: {self.get_nombre()}")
        print(f"Área: {self.calcular_area():.2f}")
        print(f"Perímetro: {self.calcular_perimetro():.2f}")

# Subclase Circulo
class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.__radio = radio

    def get_radio(self):
        return self.__radio

    def calcular_area(self):
        return math.pi * self.__radio ** 2

    def calcular_perimetro(self):
        return 2 * math.pi * self.__radio

# Subclase Rectángulo
class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.__base = base
        self.__altura = altura

    def get_base(self):
        return self.__base

    def get_altura(self):
        return self.__altura

    def calcular_area(self):
        return self.__base * self.__altura

    def calcular_perimetro(self):
        return 2 * (self.__base + self.__altura)

# Menú principal
def main():
    lista_figuras = [] 
    while True:
        print("\n----- SISTEMA DE FIGURAS GEOMÉTRICAS -----")
        print("1. Calcular Círculo")
        print("2. Calcular Rectángulo")
        print("3. Mostrar figuras registradas")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                radio = float(input("Ingrese el radio del círculo: "))
                c = Circulo(radio)
                lista_figuras.append(c)
                print("Círculo registrado exitosamente.")
            except ValueError:
                print("Error: Ingrese un número válido.")
        elif opcion == '2':
            try:
                base = float(input("Ingrese la base del rectángulo: "))
                altura = float(input("Ingrese la altura del rectángulo: "))
                r = Rectangulo(base, altura)
                lista_figuras.append(r)
                print("Rectángulo registrado exitosamente.")
            except ValueError:
                print("Error: Ingrese números válidos.")
        elif opcion == '3':
            if len(lista_figuras) == 0:
                print("No hay figuras registradas aún.")
            else:
                for f in lista_figuras:
                    f.mostrar_info()
        elif opcion == '4':
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú
if __name__ == "__main__":
    main()
