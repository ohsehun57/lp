import sys
import math

class trianguloazar:
    def __init__(self, a, b, c):
        
        if not self.lados_validos(a, b, c):
            raise ValueError("no forman un triangulo")
        self.a = a
        self.b = b
        self.c = c

    def calcular_perimetro(self):
        return self.a + self.b + self.c

    def calcular_area(self):
        
        s = self.calcular_perimetro() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def lados_validos(self, a, b, c):
        return (a + b > c) , (a + c > b) , (b + c > a)
    
    def trinagulo_recto(self):
        lados = sorted([self.a, self.b, self.c])
        return math.isclose(lados[0]**2 + lados[1]**2, lados[2]**2)

    def calcular_hipotenusa(self):
        if self.trinagulo_recto():
            return max(self.a, self.b, self.c)
        else:
            return None


try:
    t1 = trianguloazar(3, 4, 5)  

    print(f"perimetro: {t1.calcular_perimetro()}")
    print(f"erea: {t1.calcular_area()}")
    if t1.trinagulo_recto():
        print(f"es trian rectangulo. hipotenuis: {t1.calcular_hipotenusa()}")
    else:
        print("no es triangulo recto")

 
    print("\nla memoria es bytes:")
    tamaño_objeto = sys.getsizeof(t1)
    tamaño_lado1 = sys.getsizeof(t1.a)
    tamaño_lado2 = sys.getsizeof(t1.b)
    tamaño_lado3 = sys.getsizeof(t1.c)
    tam_metodo1 = sys.getsizeof(t1.calcular_perimetro)
    tam_metodo2 = sys.getsizeof(t1.calcular_area)
    tam_metodo3 = sys.getsizeof(t1.calcular_hipotenusa)
    tam_clase = sys.getsizeof(trianguloazar)

    print(f"Objeto triangulo: {tamaño_objeto}")
    print(f"lado a: {tamaño_lado1}")
    print(f"lado b: {tamaño_lado2}")
    print(f"lado c: {tamaño_lado3}")
    print(f"metodo calcular perimerto: {tam_metodo1}")
    print(f"metodo calcular area: {tam_metodo2}")
    print(f"metodo calcular hipotenusa: {tam_metodo3}")
    print(f"clase triangulo: {tam_clase}")

    suma_total = (tamaño_objeto + tamaño_lado1 + tamaño_lado2 + tamaño_lado3 + tam_metodo1 + tam_metodo2 + tam_metodo3 + tam_clase)

    print(f"\nsuma  del uso de memoria: {suma_total} bytes")

except ValueError as e:
    print(f"error: {e}")
