# 1. Clase base (interfaz)
class formadepago:
    def realizar_pago(self, monto):
        print("No se puede procesar el pago con forma genérica.")

# 2. Clase Pago por Tarjeta
class PagoPorTarjeta(formadepago):
    def __init__(self, numero_tarjeta):
        self.numero_tarjeta = numero_tarjeta

    def realizar_pago(self, monto):
        print(f"Pago de ${monto:.2f} realizado con tarjeta {self.numero_tarjeta}.")

# 3. Clase Pago por PayPal
class PagoPorPayPal(formadepago):
    def __init__(self, correo):
        self.correo = correo

    def realizar_pago(self, monto):
        print(f"Pago de ${monto:.2f} realizado con cuenta PayPal ({self.correo}).")

# 4. Clase Pago por Criptomoneda
class PagoPorCripto(formadepago):
    def __init__(self, cripto):
        self.cripto = cripto

    def realizar_pago(self, monto):
        print(f"Pago de ${monto:.2f} realizado desde  cripto moneda: {self.cripto}.")

# 5. Lista de pagos (polimorfismo)
pagos = [
    PagoPorTarjeta("1234-5678-9012-3456"),
    PagoPorPayPal("usuario@example.com"),
    PagoPorCripto("0xABCDEF1234567890")
]

# 6. Probar polimorfismo
for pago in pagos:
    pago.realizar_pago(20)
