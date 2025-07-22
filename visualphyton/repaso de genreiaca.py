"""#programacion generica 
from typing import TypeVar,Generic
T = TypeVar("T",int,float )
class operacionmatematica (Generic[T]):
    def calcular (self,a:T,b:T) ->T:
        raise  NotImplementedError ("metodo calcular() no implementDO")
class suma (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        return a + b
def main():
    operacion = suma ()
    num1 = 5
    num2 = 7
    resultado = operacion.calcular(num1,num2)
    print(f"la suma {num1} + {num2} es {resultado}")
if __name__=="__main__":
    main()

# calcular pitagoras


#programacion generica 
from typing import TypeVar,Generic
T = TypeVar("T",int,float )
class operacionmatematica (Generic[T]):
    def calcular (self,a:T,b:T) ->T:
        raise  NotImplementedError ("metodo calcular() no implementDO")
class hallarhipotenusa (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        return ((a**2 + b**2)**0.5)
def main():
    operacion = hallarhipotenusa ()
    cat1 = 3
    cat2 = 4
    resultado = operacion.calcular(cat1,cat2)
    print(f"la hipotenusa de {cat1} y {cat2} es {resultado}")
if __name__=="__main__":
    main()




#programacion de factorial
from typing import TypeVar,Generic
T = TypeVar("T",int,float )
class operacionmatematica (Generic[T]):
    def calcular (self,a:T) ->T:
        raise  NotImplementedError ("metodo calcular() no implementDO")
class hallarhipotenusa (operacionmatematica[T]):
    def calcular (self,a:T) ->T:
        if a < 1:
            print("ingrese un numero positivo")
        else:
            resultado = 1
            for i in range (1,a+1):
                resultado *= i
            return resultado
def main():
    operacion = hallarhipotenusa ()
    cat1 = 5
    resultado = operacion.calcular(cat1)
    print(f"el factorial de {cat1} es {resultado}")
if __name__=="__main__":
    main()



#calculadora

from typing import TypeVar,Generic
T = TypeVar("T",int,float )
class operacionmatematica (Generic[T]):
    def calcular (self,a:T,b:T) ->T:
        raise  NotImplementedError ("metodo calcular() no implementDO")
class suma (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        return a + b
class resta (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        return a - b
class multiplicacion (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        return a * b
class division (operacionmatematica[T]):
    def calcular (self,a:T,b:T) ->T:
        if b < 1:
            print("el numero debe ser mayor a cero")
        else:
            return a / b
def main():
    operacion1 = suma ()
    num1 = 8
    num2 = 0
    operacion2 = resta ()
    num3 = 1
    num4 = 2
    operacion3 = multiplicacion ()
    num5 = 2
    num6 = 2
    operacion4 = division ()
    num7 = 4
    num8 = 0
    resultado1 = operacion1.calcular(num1,num2)
    resultado2 = operacion2.calcular(num3,num4)
    resultado3 = operacion3.calcular(num5,num6)
    resultado4 = operacion4.calcular(num7,num8)
    print(f"la suma {num1} + {num2} es {resultado1}")
    print(f"la resta {num3} - {num4} es {resultado2}")
    print(f"la multiplicacion {num5} * {num6} es {resultado3}")
    print(f"la division {num7} / {num8} es {resultado4}")
if __name__=="__main__":
    main()

"""
from typing import TypeVar, Generic

T = TypeVar("T", int, float)

class operacionmatematica(Generic[T]):
    def calcular(self, a: T, b: T) -> T: 
        raise NotImplementedError("Método calcular() no implementado")

class suma(operacionmatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        return a + b

class resta(operacionmatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        return a - b

class multiplicacion(operacionmatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        return a * b

class division(operacionmatematica[T]):
    def calcular(self, a: T, b: T) -> T:
        if b == 0:
            print("Error: el divisor debe ser distinto de cero.")
            return None
        else:
            return a / b

def main():
    while True:
        print("\n****** Calculadora ******")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Ingrese el número a: "))
                num2 = float(input("Ingrese el número b: "))
            except ValueError:
                print("Error: debe ingresar números válidos.")
                continue

            if opcion == '1':
                operacion = suma()
                resultado = operacion.calcular(num1, num2)
                print(f"La suma {num1} + {num2} es {resultado}")
            elif opcion == '2':
                operacion = resta()
                resultado = operacion.calcular(num1, num2)
                print(f"La resta {num1} - {num2} es {resultado}")
            elif opcion == '3':
                operacion = multiplicacion()
                resultado = operacion.calcular(num1, num2)
                print(f"La multiplicación {num1} * {num2} es {resultado}")
            elif opcion == '4':
                operacion = division()
                resultado = operacion.calcular(num1, num2)
                if resultado is not None:
                    print(f"La división {num1} / {num2} es {resultado}")

        elif opcion == '5':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
