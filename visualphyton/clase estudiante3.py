"""class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)

    def mostrar_informacion(self):
        promedio = sum(self.notas) / len(self.notas) if self.notas else 0
        aprobado = "Sí" if promedio >= 10.5 else "No"

        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Carrera:", self.carrera)
        print("Notas:", self.notas)
        print("Promedio:", round(promedio, 2))
        print("Aprobado:", aprobado)



nombre = input("Ingrese el nombre del estudiante: ")
edad = int(input("Ingrese la edad: "))
carrera = input("Ingrese la carrera: ")

estudiante = Estudiante(nombre, edad, carrera)

cantidad_notas = int(input("¿Cuántas notas desea ingresar?: "))
for i in range(cantidad_notas):
    nota = float(input(f"Ingrese la nota {i+1}: "))
    estudiante.agregar_nota(nota)

print("informacion del estudiante")
estudiante.mostrar_informacion()"""



class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)

    def mostrar_informacion(self):
        promedio = sum(self.notas) / len(self.notas) if self.notas else 0
        aprobado = "Sí" if promedio >= 10.5 else "No"

        print("\nInformación del Estudiante ")
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Carrera:", self.carrera)
        print("Notas:", self.notas)
        print("Promedio:", round(promedio, 2))
        print("Aprobado:", aprobado)

ista_estudiantes = []

n = int(input("¿Cuántos estudiantes?: "))

for i in range(n):
    print(f"\n  datos del estudiante {i+1}")
    nombre = input("Nombre: ")
    edad = int(input("Edad: "))
    carrera = input("Carrera: ")

    estudiante = Estudiante(nombre, edad, carrera)

    cantidad_notas = int(input("¿Cuántas notas ?: "))
    for j in range(cantidad_notas):
        nota = float(input(f"Ingrese la nota {j+1}: "))
        if 0<=nota<=20:
            estudiante.agregar_nota(nota)

    ista_estudiantes.append(estudiante)

print("\n todod elc ontenido ")
for estudiante in ista_estudiantes:

    estudiante.mostrar_informacion()      
















