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
        aprobado = "Sí" if promedio >= 11 else "No"
        
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Carrera:", self.carrera)
        print("Notas:", self.notas)
        print("Promedio:", round(promedio, 2))
        print("Aprobado:", aprobado)



estudiante1 = Estudiante("Juan Pérez", 20, "Ingeniería Estadística")
estudiante1.agregar_nota(18)
estudiante1.agregar_nota(18)
estudiante1.agregar_nota(18)
estudiante1.agregar_nota(18)

estudiante1.mostrar_informacion()
