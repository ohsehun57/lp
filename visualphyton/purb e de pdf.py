import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
import os

# Asegúrate de tener los recursos de NLTK
nltk.download('punkt')

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = None
        self.text = ""
        self.load_pdf()

    def load_pdf(self):
        """Carga el archivo PDF y extrae el texto."""
        if not os.path.exists(self.pdf_path):
            print(f"El archivo {self.pdf_path} no existe.")
            return

        try:
            # Abre el archivo PDF
            self.doc = fitz.open(self.pdf_path)
            # Extrae el texto de cada página
            self.text = ""
            for page_num in range(self.doc.page_count):
                page = self.doc.load_page(page_num)
                self.text += page.get_text()

        except Exception as e:
            print(f"Error al abrir el archivo PDF: {e}")

    def search_text(self, query):
        """Busca un término en el texto extraído."""
        if not self.text:
            print("No se ha cargado texto. Asegúrate de cargar un archivo PDF.")
            return

        # Realiza la búsqueda de texto (ignorando mayúsculas/minúsculas)
        occurrences = []
        start = 0
        while True:
            start = self.text.lower().find(query.lower(), start)
            if start == -1:
                break
            end = start + len(query)
            occurrences.append((start, end))
            start = end

        if occurrences:
            print(f"Se encontró '{query}' {len(occurrences)} veces.")
            for start, end in occurrences:
                print(f"Encontrado: {self.text[start-30:end+30]}...")
        else:
            print(f"No se encontró '{query}' en el texto.")

    def summarize_text(self):
        """Genera un resumen simple de las primeras frases del texto."""
        if not self.text:
            print("No se ha cargado texto. Asegúrate de cargar un archivo PDF.")
            return

        # Tokeniza el texto en oraciones
        sentences = sent_tokenize(self.text)

        # Genera un resumen simple (solo las primeras 5 oraciones)
        summary = " ".join(sentences[:5])  # Resumen con las primeras 5 oraciones
        print("\nResumen del PDF:")
        print(summary)

    def display_text(self):
        """Muestra el texto completo del archivo PDF."""
        if not self.text:
            print("No se ha cargado texto. Asegúrate de cargar un archivo PDF.")
            return

        print("\nTexto Completo Extraído del PDF:")
        print(self.text[:1000])  # Muestra solo los primeros 1000 caracteres para evitar salida larga

if __name__ == "__main__":
    # Solicitar al usuario el archivo PDF
    pdf_file = input("Introduce la ruta del archivo PDF: ")

    # Crear una instancia de PDFExtractor
    extractor = PDFExtractor(pdf_file)

    # Opción para buscar texto
    search_query = input("Introduce el texto a buscar (o presiona Enter para omitir): ")
    if search_query:
        extractor.search_text(search_query)

    # Opción para ver un resumen del texto
    summarize = input("¿Te gustaría ver un resumen del texto? (s/n): ").strip().lower()
    if summarize == 's':
        extractor.summarize_text()

    # Opción para mostrar el texto completo
    display = input("¿Te gustaría ver el texto completo extraído? (s/n): ").strip().lower()
    if display == 's':
        extractor.display_text()
