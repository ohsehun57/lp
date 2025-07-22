class cuenta_bancaria:
    def __init__(self,titular,saldo_inicial):
        self._titular = titular
        self._saldo_inicial=saldo_inicial
    def consultar_saldo(self):
        print(f"saldo actual de {self._titular}: s/ {self._saldo_inicial: .2f}")
    def agregar_saldo(self,monto):
        if monto>0:
            self._saldo_inicial+=monto
            print(f"deposito de s/. {monto: .2f} realizado con exito")
        else:
            print("el monto ha realizar debe ser positivo")
    def retirar(self,monto):
        if 0 < monto <=self._saldo_inicial:
            self._saldo_inicial-=monto
            print(f"retiro de s/, {monto: .2f} realizado con exito.")
        else:
            print("saldo insuficiente o monto invalido")
cuenta= cuenta_bancaria("raul",500.00)
cuenta.consultar_saldo()

cuenta.agregar_saldo(150)
cuenta.consultar_saldo()
cuenta.retirar(800)
cuenta.consultar_saldo()