from abc import ABC, abstractmethod
class Vehiculo(ABC):
    def __init__(self, marca, modelo, año):
        if 1980 <= año <= 2025:
            self.marca = marca
            self.modelo = modelo
            self.año = año
            self.valido = True
        else:
            print("⚠️ Año inválido para", marca, modelo, ":", año)
            self.valido = False
    @abstractmethod
    def calcular_impuesto(self):
        pass

    def mostrar_info(self):
        print(self.__class__.__name__ + ":", self.marca, self.modelo, "(", self.año, ")")
class Auto(Vehiculo):
    def calcular_impuesto(self):
        return 0.05 * (2025 - self.año)

class Motocicleta(Vehiculo):
    def calcular_impuesto(self):
        return 0.03 * (2025 - self.año)

class Camioneta(Vehiculo):
    def calcular_impuesto(self):
        return 500 if self.año > 2015 else 300
    
def main():
    datos = [
        ("Toyota", "Yaris", 2016, Auto),
        ("Ducati", "MY21", 2024, Motocicleta),
        ("Ford ", "Maverick", 2014, Camioneta),
        ("Chevrolet", "Camaro", 2026, Auto)  
    ]
    vehiculos = []
    for marca, modelo, año, clase in datos:
        carro = clase(marca, modelo, año)
        if carro.valido:
            vehiculos.append(carro)
    print("\n los impuestos son :")
    for carro in vehiculos:
        carro.mostrar_info()
        print("Impuesto a pagar:", round(carro.calcular_impuesto(), 2), "soles\n")
main()

