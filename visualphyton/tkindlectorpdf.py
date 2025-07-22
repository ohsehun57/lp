import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class Archivos:
    def __init__(self, nombredel_archivo):
        self._nombredel_archivo = nombredel_archivo
        self._archivo = None
        print(f"Archivo '{self._nombredel_archivo}' listo")

    def obtener_nombre_archivo(self):
        return self._nombredel_archivo

    def establecer_nombre_archivo(self, nuevo_nombre):
        self._nombredel_archivo = nuevo_nombre

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

    def __del__(self):
        self.cerrar()
        print("Objeto destruido y recursos liberados")

class LeerPDF(Archivos):
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

# --- Interfaz Gráfica con Tkinter ---
def seleccionar_pdf():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if archivo:
        procesar_pdf(archivo)

def procesar_pdf(ruta_pdf):
    try:
        lector = LeerPDF(ruta_pdf)
        texto = lector.extraer_texto()
        resumen = lector.resumen_simple()

        # Mostrar en la interfaz
        texto_salida.delete(1.0, tk.END)
        texto_salida.insert(tk.END, texto)

        resumen_salida.delete(1.0, tk.END)
        resumen_salida.insert(tk.END, resumen)

        nombre_label.config(text=f"Archivo: {lector.obtener_nombre_archivo()}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al leer el PDF:\n{e}")

# --- Crear ventana principal ---
ventana = tk.Tk()
ventana.title("Lector de PDF con Resumen")
ventana.geometry("800x600")

tk.Button(ventana, text="Seleccionar PDF", command=seleccionar_pdf, font=("Arial", 12)).pack(pady=10)

nombre_label = tk.Label(ventana, text="Archivo: ninguno", font=("Arial", 10))
nombre_label.pack()

tk.Label(ventana, text="Texto extraído:", font=("Arial", 12, "bold")).pack()
texto_salida = scrolledtext.ScrolledText(ventana, height=15, wrap=tk.WORD)
texto_salida.pack(fill=tk.BOTH, expand=True, padx=10)

tk.Label(ventana, text="Resumen:", font=("Arial", 12, "bold")).pack()
resumen_salida = scrolledtext.ScrolledText(ventana, height=5, wrap=tk.WORD, bg="#f5f5f5")
resumen_salida.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))

ventana.mainloop()
