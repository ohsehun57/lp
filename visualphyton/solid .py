from abc import ABC, abstractmethod
import math

# ----- D - Dependency Inversion -----
class HipotenusaCalculator(ABC):
    """Abstracción: cualquier algoritmo que calcule la hipotenusa."""
    @abstractmethod
    def calcular(self, cateto_a: float, cateto_b: float) -> float: ...

# ----- S / O / L / I -----
class PythagorasCalculator(HipotenusaCalculator):
    """Implementación concreta del Teorema de Pitágoras."""
    def calcular(self, cateto_a: float, cateto_b: float) -> float:
        return math.sqrt(cateto_a ** 2 + cateto_b ** 2)

class TrianguloRectangulo:
    """Orquesta el cálculo usando la calculadora inyectada."""
    def __init__(self, calculadora: HipotenusaCalculator) -> None:
        self._calculadora = calculadora          # DIP: depende de la abstracción

    def hipotenusa(self, a: float, b: float) -> float:
        return self._calculadora.calcular(a, b)

# ---------------------------------------------------------------
# Ejecutar: (sin usar if __name__ == '__main__')
# ---------------------------------------------------------------
calculadora = PythagorasCalculator()             # LSP: podría cambiarse por otra clase hija
triangulo   = TrianguloRectangulo(calculadora)

a = float(input("Ingrese cateto a: "))
b = float(input("Ingrese cateto b: "))

c = triangulo.hipotenusa(a, b)
print(f"La hipotenusa es: {c:.2f}")
