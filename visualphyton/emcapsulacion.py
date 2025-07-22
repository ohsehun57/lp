class persona:
    def __init__(self,nombre,edad):
        self.__nombre = nombre   #atributo privado
        self.__edad = edad            #atributo privado

    #getter para nombre
    def obtener_nombre(self):
        return self.__nombre
        
    #getter para edad
    def obtener_edad(self):
        return self.__edad
    
    #setter para edad

    def establecer_edad(self,nueva_edad):
        if nueva_edad > 0 :
            self.__edad=nueva_edad
        else:
            print("edad no valida")
    def es_mayor_de_edad(self):
        return self.__edad>=18
    
    def mostrar_datos(self):
        print(f"nombre: {self.__nombre}, \nedad: {self.__edad}")

    def cumplir_años(self):
        self.__edad+=1
        print(f"feliz cumpleaños, {self.__nombre},ahora tienes :{self.__edad} años")

persona1 = persona ("pedro", 15)
persona1.mostrar_datos()

if persona1.es_mayor_de_edad():
    print("es mayor de edad")
else:
    print("es menor de edad")

persona1.cumplir_años()
