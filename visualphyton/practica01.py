from abc import ABC, abstractmethod

# ---------------------- Clase base ----------------------

class Vehiculo(ABC):
    def __init__(self, modelo, fabricante):
        self.modelo = modelo
        self.fabricante = fabricante

    @abstractmethod
    def descripcion(self):
        pass

# ---------------------- Subclases ----------------------

class Auto(Vehiculo):
    def __init__(self, modelo, fabricante, pasajeros):
        super().__init__(modelo, fabricante)
        self.pasajeros = pasajeros

    def descripcion(self):
        texto = "\n----- AUTO -----\n"
        texto += "Fabricante: " + self.fabricante + "\n"
        texto += "Modelo: " + self.modelo + "\n"
        texto += "Cantidad de Pasajeros: " + str(self.pasajeros) + "\n"
        texto += "----------------\n"
        return texto

class Camion(Vehiculo):
    def __init__(self, modelo, fabricante, peso_maximo, tipo_carga):
        super().__init__(modelo, fabricante)
        self.peso_maximo = peso_maximo
        self.tipo_carga = tipo_carga

    def descripcion(self):
        texto = "\n----- CAMIÓN -----\n"
        texto += "Fabricante: " + self.fabricante + "\n"
        texto += "Modelo: " + self.modelo + "\n"
        texto += "Peso Máximo: " + str(self.peso_maximo) + " kg\n"
        texto += "Tipo de Carga: " + self.tipo_carga + "\n"
        texto += "------------------\n"
        return texto

class Moto(Vehiculo):
    def __init__(self, modelo, fabricante, consumo):
        super().__init__(modelo, fabricante)
        self.consumo = consumo

    def descripcion(self):
        texto = "\n----- MOTOCICLETA -----\n"
        texto += "Fabricante: " + self.fabricante + "\n"
        texto += "Modelo: " + self.modelo + "\n"
        texto += "Consumo: " + str(self.consumo) + " km/l\n"
        texto += "------------------------\n"
        return texto

# ---------------------- Interfaz de reporte ----------------------

class GeneradorReporte(ABC):
    @abstractmethod
    def generar(self, vehiculo: Vehiculo):
        pass

# ---------------------- Implementaciones de reporte ----------------------

class ReporteConsola(GeneradorReporte):
    def generar(self, vehiculo: Vehiculo):
        print("\n=== REPORTE EN CONSOLA ===")
        print(vehiculo.descripcion())
        print("===========================\n")

class ReporteTexto(GeneradorReporte):
    def generar(self, vehiculo: Vehiculo):
        print("\n=== REPORTE EN ARCHIVO DE TEXTO (SIMULADO) ===")
        print(vehiculo.descripcion())
        print("==== FIN DEL ARCHIVO SIMULADO ====\n")

class ReportePDF(GeneradorReporte):
    def generar(self, vehiculo: Vehiculo):
        print("\n=== REPORTE EN PDF (SIMULADO) ===")
        print(vehiculo.descripcion())
        print("==== FIN DEL PDF SIMULADO ====\n")

# ---------------------- Clase que usa la inyección ----------------------

class GeneradorDeInformes:
    def __init__(self, generador: GeneradorReporte):
        self.generador = generador

    def procesar_reporte(self, vehiculo: Vehiculo):
        self.generador.generar(vehiculo)

# ---------------------- USO DEL SISTEMA ----------------------

if __name__ == "__main__":
    auto1 = Auto("Corolla", "Toyota", 5)
    camion1 = Camion("Actros", "Mercedes-Benz", 18000, "Carga pesada")
    moto1 = Moto("FZ", "Yamaha", 35)

    consola = GeneradorDeInformes(ReporteConsola())
    texto = GeneradorDeInformes(ReporteTexto())
    pdf = GeneradorDeInformes(ReportePDF())

    consola.procesar_reporte(auto1)
    texto.procesar_reporte(camion1)
    pdf.procesar_reporte(moto1)

    # Agregar nuevo tipo de reporte sin modificar nada anterior
    class ReporteCorreo(GeneradorReporte):
        def generar(self, vehiculo: Vehiculo):
            print("\n=== REPORTE EN CORREO (SIMULADO) ===")
            print(vehiculo.descripcion())
            print("==== MENSAJE ENVIADO ====\n")

    correo = GeneradorDeInformes(ReporteCorreo())
    correo.procesar_reporte(auto1)
