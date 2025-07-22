"""class Animal:
    def hablar (self):
        return " hace un sonido "
class perro (Animal):
    def hablar (self):
        return "dice !wauu! "
p = perro ()
print(p.hablar())
#clase sin cosntructor

class mamifero:
    def caracteristica (self):
        return "tiene pelo"
class acuatico:
    def vivir (self):
        return "viven en el agua"
class delfin (mamifero,acuatico):
    pass 
d = delfin()
print (d.caracteristica())
print (d.vivir())

class persona:
    def __init__1(self,nombre):
        self.nombre = nombre
class estudiante(persona):
    def __init__(self,nombre,carrera):
        super() .__init__(nombre)
        self.carrera = carrera
a = estudiante ("maria","ingenieria")
print(a.nombre)
print(a.carrera)


class vehiculo:
    def __init__(self,marca,modelo):
        self.marca = marca
        self.modelo = modelo
    def descripcion(self):
        return f"vehiculo:{self.marca} {self.modelo}"
class auto(vehiculo):
    def __init__(self,marca,modelo,puertas):
        super().__init__(marca,modelo)
        self.puertas = puertas
    def descripcion(self):
        return super().descripcion()+f"puertas: {self.puertas}"
auto1 = auto ("toyota","corolla ",4)
print(auto1.descripcion())

class computadora:
    def encender(self):
        return "computadora encendida"
class telefono:
    def llamadas(self,numero):
        return f"llamando al numero {numero}....."
class smartphone(computadora,telefono):
    def usar_aplicacion(self,app):
        return f"abriendo tu app :{app}"
mi_telefono=smartphone()
print(mi_telefono.encender())
print(mi_telefono.llamadas("951085350"))
print(mi_telefono.usar_aplicacion("whatsapp"))

class figura:
    pass 
class triangulo(figura):
    def resolver_area(self,base,altura):
        return f"el area es: {base * altura / 2}"
    def resolver_perimetro(self,cat1,cat2):
        return f"el perimetro es: {cat1 + cat2 + ((cat1**2 + cat2 **2)**0.5)}"
resultado = triangulo()
print(resultado.resolver_area(3,4))
print(resultado.resolver_perimetro(3,4))
"""
class figura:
    def es_lafigu(self,nombre):
        return f"la figura es:{nombre}"
class color:
    def es_lacolor(self,color):
        return f"el color  es:{color}"
class textura:
    def es_textu(self,nombre):
        return f"la textura es:{nombre}"
class cuadrado(figura,color,textura):
    def resolver_area(self,base):
        return f"el area es: {base * base}\nel perimetro es:{base *4}"
resultado = cuadrado()
print(f"{resultado.es_lafigu("cuadrado")}\n{resultado.es_lacolor("verde")}\n{resultado.resolver_area(4)}\n{resultado.es_textu("enmallado")}")


