"""class estudiante:
    def __init__(self,nombre,edad,notas):
        nombre = nombre
        edad = edad 
        notas = notas 
    def mostrar_info(self):
        print("nombre:",self.nombre)
        print("edad:",self.edad)
        print("promedio:",sum(self.notas)/len(self.notas))
    def agregar_notas(notas):
        self.notas.append(notas)
e = estudiante("ana",20[15,18,17])
e.mostrar_info()
e.agregar_notas(20)
"""
#correccion de errores d este codigo

class estudiante:
    def __init__(self,nombre,edad,notas):
        self._nombre = nombre
        self._edad = edad 
        self._notas = notas 

    def mostrar_info(self):
        print("nombre:",self._nombre)
        print("edad:",self._edad)
        print(f"promedio:,{sum(self._notas) / len(self._notas):.2f}")

    def agregar_notas(self,nota):
        self._notas.append(nota)

e= estudiante("ana",20,[20,18,17])
e.mostrar_info()
e.agregar_notas(20)
