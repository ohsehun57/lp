from abc import ABC, abstractmethod
from typing import List

# ----- S: Producto tiene una sola responsabilidad -----
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

# ----- I y D: Abstracción para cálculo de total -----
class CalculadoraTotal(ABC):
    @abstractmethod
    def calcular_total(self, productos: List[Producto]) -> float:
        pass

# ----- O y L: Implementación concreta que puede cambiar -----
class CalculadoraTotalSimple(CalculadoraTotal):
    def calcular_total(self, productos: List[Producto]) -> float:
        return sum(p.precio for p in productos)

# ----- S: Factura gestiona productos y delega cálculos -----
class Factura:
    def __init__(self, calculadora: CalculadoraTotal):
        self.productos = []
        self.calculadora = calculadora  # D: depende de una abstracción

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def obtener_total(self) -> float:
        return self.calculadora.calcular_total(self.productos)

# ----- S: Muestra la factura (no calcula, no almacena) -----
class ImpresoraFactura:
    def imprimir(self, factura: Factura):
        print("🧾 FACTURA")
        for producto in factura.productos:
            print(f"- {producto.nombre}: ${producto.precio:.2f}")
        print(f"TOTAL: ${factura.obtener_total():.2f}")

# ----- S: Orquesta todo el proceso -----
class SistemaFacturacion:
    def __init__(self, factura: Factura, impresora: ImpresoraFactura):
        self.factura = factura
        self.impresora = impresora

    def agregar_producto(self, nombre: str, precio: float):
        producto = Producto(nombre, precio)
        self.factura.agregar_producto(producto)

    def facturar(self):
        self.impresora.imprimir(self.factura)

# ----- USO -----
calculadora = CalculadoraTotalSimple()
factura = Factura(calculadora)
impresora = ImpresoraFactura()
sistema = SistemaFacturacion(factura, impresora)

sistema.agregar_producto("Guitarra", 250.00)
sistema.agregar_producto("Cable de audio", 20.00)
sistema.agregar_producto("Pedal de efectos", 75.00)

sistema.facturar()
