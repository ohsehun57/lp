import PyPDF2

class Archivos:
#encapsulamineto _nombredelarchivo
    def __init__(self, nombredel_archivo):
        self._nombredel_archivo = nombredel_archivo
        self._archivo = None
        print(f"Archivo '{self._nombredel_archivo}' listo")

    # Getter 
    def obtener_nombre_archivo(self):
        return self._nombredel_archivo

    # Setter 
    def establecer_nombre_archivo(self, nuevo_nombre):
        self._nombredel_archivo = nuevo_nombre
#metodos
    def abrir(self):
        try:
            self._archivo = open(self._nombredel_archivo, 'rb')
            print("Archivo abierto correctamente")
        except FileNotFoundError:
            print("Error: no se encontró el archivo PDF")

    def cerrar(self):
        if self._archivo:
            self._archivo.close()
            print("Archivo cerrado")
#destructor
    def __del__(self):
        self.cerrar()
        print("Objeto destruido y recursos liberados")
#herencia
class LeerPDF(Archivos):
#constructor
    def __init__(self, nombredel_archivo):
        super().__init__(nombredel_archivo)
        self._lector = None
        self._texto_extraido = ""
        self.abrir_pdf()

    def abrir_pdf(self):
        self.abrir()
        if self._archivo:
            self._lector = PyPDF2.PdfReader(self._archivo)
            print("PDF cargado con éxito")

    def extraer_texto(self):
        if not self._lector:
            print("No se ha cargado el PDF")
            return ""

        for pagina in self._lector.pages:
            texto = pagina.extract_text()
            if texto:
                self._texto_extraido += texto + "\n"

        print("Texto extraído correctamente")
        return self._texto_extraido

    def resumen_simple(self, cantidad_palabras=50):
        if not self._texto_extraido:
            self.extraer_texto()

        palabras = self._texto_extraido.split()
        resumen = " ".join(palabras[:cantidad_palabras])
        return resumen + "..." if len(palabras) > cantidad_palabras else resumen

# Función para mostrar resultados
def mostrar_resultados():
    ruta_pdf = "ejemplo.pdf"  # Cambia esta ruta por el nombre real de tu archivo PDF

    try:
        lector = LeerPDF(ruta_pdf)
        texto = lector.extraer_texto()
        print("\nTexto completo (primeros 25 caracteres):")
        print(texto[:25])
        print("\nResumen:")
        print(lector.resumen_simple())

        # Mostrar el nombre del archivo usando el getter
        print(f"\nNombre del archivo leído: {lector.obtener_nombre_archivo()}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llamada directa
mostrar_resultados()
