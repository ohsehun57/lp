class estudiante:
    def __init__(self,nombre,edad,carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.notas = []

    def agregar_notas(self,nota):
        self.notas.append(nota)
    
    def promedio_notas(self):
        if len(self.notas) == 0:
            return 0
        return sum(self.notas)/len(self.notas)
        
    def es_aprobado(self):
        promedio = self.promedio_notas()
        if promedio >=11:
            return True
        return False
  
    def mostrar_informacion(self):
        info = f"Nombre: {self.nombre}\nEdad: {self.edad}\nCarrera:{self.carrera}\nNotas:{self.notas}"
        info += f"Nombre: {self.promedio_notas():2f}\nAprobado:{"Si"if self.es_aprobado()else "no"}"
        return info
estudiante1 = estudiante("juan perez",20,"ingenieriaestadistica")
estudiante1.agregar_notas(18)
estudiante1.agregar_notas(18)
estudiante1.agregar_notas(18)
estudiante1.agregar_notas(18)
print(estudiante1.mostrar_informacion())
        