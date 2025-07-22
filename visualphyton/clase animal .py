# Clase base: Animal
class Animal:
    def __init__(self, nombre, edad, especie):
        self.nombre = nombre
        self.edad = edad
        self.especie = especie

    def obtener_info(self):
        pass  # Método polimórfico


# Subclase: Felino
# Herencia: Hereda Animal
class Felino(Animal):
    def __init__(self, nombre, edad, especie, color_pelaje):
        super().__init__(nombre, edad, especie)
        # Encapsulamiento
        self.__color_pelaje = color_pelaje

    def get_color_pelaje(self):
        return self.__color_pelaje

    # Polimorfismo
    def obtener_info(self):
        return f"Felino - Nombre: {self.nombre}, Edad: {self.edad}, Especie: {self.especie}, Color de pelaje: {self.__color_pelaje}"


# Subclase: Ave
# Herencia: Hereda Animal
class Ave(Animal):
    def __init__(self, nombre, edad, especie, tipo_pico):
        super().__init__(nombre, edad, especie)
        # Encapsulamiento
        self.__tipo_pico = tipo_pico

    def get_tipo_pico(self):
        return self.__tipo_pico

    # Polimorfismo
    def obtener_info(self):
        return f"Ave - Nombre: {self.nombre}, Edad: {self.edad}, Especie: {self.especie}, Tipo de pico: {self.__tipo_pico}"


# Menú Principal
def main():
    lista_animales = []

    while True:
        print("\n****** SISTEMA DE ANIMALES ******")
        print("1. Registrar Felino")
        print("2. Registrar Ave")
        print("3. Mostrar Animales")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            especie = input("Especie: ")
            color_pelaje = input("Color del pelaje: ")
            felino = Felino(nombre, edad, especie, color_pelaje)
            lista_animales.append(felino)
            print("Felino registrado correctamente.")

        elif opcion == '2':
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            especie = input("Especie: ")
            tipo_pico = input("Tipo de pico: ")
            ave = Ave(nombre, edad, especie, tipo_pico)
            lista_animales.append(ave)
            print("Ave registrada correctamente.")

        elif opcion == '3':
            if not lista_animales:
                print("No hay animales registrados.")
            else:
                print("\nListado de Animales:")
                for idx, animal in enumerate(lista_animales):
                    print(f"{idx+1}. {animal.obtener_info()}")

        elif opcion == '4':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


# Ejecutar programa
if __name__ == "__main__":
    main()



