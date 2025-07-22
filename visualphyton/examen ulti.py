import os

class Libro:
    def __init__(self, codigo, titulo, autor):
        self.__codigo = codigo
        self.__titulo = titulo
        self.__autor = autor
        self.__reservado = False

    def __del__(self):
        print(f"Libro eliminado: {self.__titulo}")

    def reservar(self):
        if not self.__reservado:
            self.__reservado = True
            return True
        return False

    def cancelar_reserva(self):
        self.__reservado = False

    def esta_reservado(self):
        return self.__reservado

    def get_codigo(self):
        return self.__codigo

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def mostrar_info(self):
        estado = "Reservado" if self.__reservado else "Disponible"
        print(f"{self.__codigo} - {self.__titulo} - {self.__autor} - {estado}")

    def to_txt(self):
        estado = "Reservado" if self.__reservado else "Disponible"
        return f"Código: {self.__codigo} | Título: {self.__titulo} | Autor: {self.__autor} | Estado: {estado}"

    @staticmethod
    def from_txt(linea):
        try:
            partes = linea.strip().split(" | ")
            codigo = partes[0].split(": ")[1]
            titulo = partes[1].split(": ")[1]
            autor = partes[2].split(": ")[1]
            estado = partes[3].split(": ")[1]
            libro = Libro(codigo, titulo, autor)
            libro.__reservado = (estado == "Reservado")
            return libro
        except:
            print("Error al leer un libro del archivo.")
            return None


class Usuario:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__reservas = []

    def __del__(self):
        print(f"Usuario eliminado: {self.__nombre}")

    def get_nombre(self):
        return self.__nombre

    def reservar_libro(self, libro):
        if libro.get_codigo() in self.__reservas:
            print("Ya reservaste este libro.")
            return False
        if libro.reservar():
            self.__reservas.append(libro.get_codigo())
            print("Reserva realizada correctamente.")
            return True
        else:
            print("Este libro ya está reservado.")
            return False

    def cancelar_reserva(self, libro):
        if libro.get_codigo() in self.__reservas:
            libro.cancelar_reserva()
            self.__reservas.remove(libro.get_codigo())
            print("Reserva cancelada correctamente.")
            return True
        print("No tienes este libro reservado.")
        return False

    def mostrar_reservas(self):
        if self.__reservas:
            print(f"\nReservas de {self.__nombre}:")
            for codigo in self.__reservas:
                print(f"- {codigo}")
        else:
            print(f"{self.__nombre} no tiene reservas.")

    def to_txt(self):
        return f"{self.__nombre}|{','.join(self.__reservas)}"


class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.cargar_libros()
        self.cargar_usuarios()

    def __del__(self):
        self.guardar_libros()
        self.guardar_usuarios()

    def registrar_libro(self, libro):
        if any(l.get_codigo() == libro.get_codigo() for l in self.libros):
            print("Ya existe un libro con ese código.")
        else:
            self.libros.append(libro)
            print("Libro registrado correctamente.")
            self.guardar_libros()  # 🔄 Guardar inmediatamente


    def agregar_usuario(self, usuario):
        if any(u.get_nombre() == usuario.get_nombre() for u in self.usuarios):
            print("El usuario ya existe.")
        else:
            self.usuarios.append(usuario)
            print("Usuario agregado correctamente.")
            self.guardar_usuarios()  # 🔄 Guardar inmediatamente

    def reservar_libro_para_usuario(self, nombre_usuario, codigo_libro):
        usuario = self.obtener_usuario(nombre_usuario)
        if not usuario:
            print("Usuario no encontrado.")
            return
        libro = self.buscar_libro(codigo_libro)
        if not libro:
            print("Libro no encontrado.")
            return
        if usuario.reservar_libro(libro):
            self.guardar_libros()
            self.guardar_usuarios()

    def cancelar_reserva_para_usuario(self, nombre_usuario, codigo_libro):
        usuario = self.obtener_usuario(nombre_usuario)
        if not usuario:
            print("Usuario no encontrado.")
            return
        libro = self.buscar_libro(codigo_libro)
        if not libro:
            print("Libro no encontrado.")
            return
        if usuario.cancelar_reserva(libro):
            self.guardar_libros()
            self.guardar_usuarios()
            

    def obtener_usuario(self, nombre):
        for usuario in self.usuarios:
            if usuario.get_nombre() == nombre:
                return usuario
        return None

    def buscar_libro(self, codigo):
        for libro in self.libros:
            if libro.get_codigo() == codigo:
                return libro
        return None

    def listar_libros_disponibles(self):
        print("\nLibros disponibles:")
        encontrados = False
        for libro in self.libros:
            if not libro.esta_reservado():
                libro.mostrar_info()
                encontrados = True
        if not encontrados:
            print("No hay libros disponibles.")

    def listar_libros_reservados(self):
        print("\nLibros reservados:")
        encontrados = False
        for libro in self.libros:
            if libro.esta_reservado():
                libro.mostrar_info()
                encontrados = True
        if not encontrados:
            print("No hay libros reservados.")

    def guardar_libros(self):
        with open("libros.txt", "w", encoding="utf-8") as f:
            for libro in self.libros:
                f.write(libro.to_txt() + "\n")

    def cargar_libros(self):
        if os.path.exists("libros.txt"):
            with open("libros.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    libro = Libro.from_txt(linea)
                    if libro:
                        self.libros.append(libro)

    def guardar_usuarios(self):
        with open("usuarios.txt", "w", encoding="utf-8") as f:
            for usuario in self.usuarios:
                f.write(usuario.to_txt() + "\n")

    def cargar_usuarios(self):
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split("|")
                    if len(partes) >= 1:
                        nombre = partes[0]
                        reservas = partes[1].split(",") if len(partes) > 1 and partes[1] else []
                        usuario = Usuario(nombre)
                        for cod in reservas:
                            libro = self.buscar_libro(cod)
                            if libro and not libro.esta_reservado():
                                libro.reservar()
                                usuario.reservar_libro(libro)
                            elif libro and libro.esta_reservado():
                                usuario._Usuario__reservas.append(cod)  # Acceso forzado para carga
                        self.usuarios.append(usuario)



# ============================
# Menú principal interactivo
# ============================

def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Menú ---")
        print("1. Registrar libro")
        print("2. Hacer reserva")
        print("3. Cancelar reserva")
        print("4. Mostrar libros disponibles")
        print("5. Mostrar libros reservados")
        print("6. Mostrar reservas de un usuario")
        print("7. Agregar usuario")
        print("8. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            codigo = input("Código del libro: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            libro = Libro(codigo, titulo, autor)
            biblioteca.registrar_libro(libro)

        elif opcion == "2":
            nombre = input("Nombre del usuario: ")
            codigo = input("Código del libro a reservar: ")
            biblioteca.reservar_libro_para_usuario(nombre, codigo)

        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            codigo = input("Código del libro a cancelar reserva: ")
            biblioteca.cancelar_reserva_para_usuario(nombre, codigo)


        elif opcion == "4":
            biblioteca.listar_libros_disponibles()

        elif opcion == "5":
            biblioteca.listar_libros_reservados()

        elif opcion == "6":
            nombre = input("Nombre del usuario: ")
            usuario = biblioteca.obtener_usuario(nombre)
            if usuario:
                usuario.mostrar_reservas()
            else:
                print("Usuario no encontrado.")

        elif opcion == "7":
            nombre = input("Nombre del nuevo usuario: ")
            nuevo_usuario = Usuario(nombre)
            biblioteca.agregar_usuario(nuevo_usuario)

        elif opcion == "8":
            print("Saliendo y guardando datos...")
            break

        else:
            print("Opción no válida.")

# Ejecutar directamente sin if __name__ == "__main__"
menu()
