from abc import ABC, abstractmethod

class Vehiculo(ABC):
    RANGO_MIN = 1980
    RANGO_MAX = 2025

    def __init__(self, marca, modelo, anio):
        self.valido = False 

        if not str(marca).strip():
            print("⚠️  Marca vacía:", marca)
            return
        if not str(modelo).strip():
            print("⚠️  Modelo vacío:", modelo)
            return

        try:
            anio_int = int(anio)
        except (ValueError, TypeError):
            print(f"⚠️  Año no numérico para {marca} {modelo}: {anio}")
            return

        if anio_int < 0:
            print(f"⚠️  Año negativo para {marca} {modelo}: {anio_int}")
            return
        if not (Vehiculo.RANGO_MIN <= anio_int <= Vehiculo.RANGO_MAX):
            print(f"⚠️  Año fuera de rango ({Vehiculo.RANGO_MIN}-{Vehiculo.RANGO_MAX}) "
                  f"para {marca} {modelo}: {anio_int}")
            return

        self.marca = str(marca).strip()
        self.modelo = str(modelo).strip()
        self.anio = anio_int
        self.valido = True 

    @abstractmethod
    def calcular_impuesto(self):
        pass

    def mostrar_info(self):
        print(f"{self.__class__.__name__}: {self.marca} {self.modelo} ({self.anio})")



class Auto(Vehiculo):
    def calcular_impuesto(self):
        return 0.05 * (Vehiculo.RANGO_MAX - self.anio)

class Motocicleta(Vehiculo):
    def calcular_impuesto(self):
        return 0.03 * (Vehiculo.RANGO_MAX - self.anio)

class Camioneta(Vehiculo):
    def calcular_impuesto(self):
        return 500 if self.anio > 2015 else 300


def main():
    datos = [
        ("Toyota",    "Yaris",     2016,  Auto),
        ("Ducati",    "MY21",      2024,  Motocicleta),
        ("Ford",      "Maverick",  2014,  Camioneta),
        ("Chevrolet", "Camaro",    2026,  Auto),        
        ("Nissan",    "Sentra",   -1990,  Auto),        
        ("Honda",     "",          2010,  Auto),        
        ("BMW",       "1200GS",  "dosmil", Motocicleta) 
    ]
    vehiculos = []
    for marca, modelo, anio, clase in datos:
        v = clase(marca, modelo, anio)
        if v.valido:
            vehiculos.append(v)

    if not vehiculos:
        print("\nNo hay vehículos válidos.")
        return

    print("\n*** Impuestos ***")
    for v in vehiculos:
        v.mostrar_info()
        print("Impuesto a pagar:", round(v.calcular_impuesto(), 2), "soles\n")


if __name__ == "__main__":
    main()

from 