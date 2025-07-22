import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import fitz  # PyMuPDF
import os

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lector Profesional de PDF")
        self.root.geometry("900x700")

        self.pdf_file = None
        self.total_pages = 0
        self.current_page = 0
        self.doc = None

        self.setup_ui()

    def setup_ui(self):
        # Frame de botones
        top_frame = ttk.Frame(self.root)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        ttk.Button(top_frame, text="Abrir PDF", command=self.load_pdf).grid(row=0, column=0, padx=5)
        ttk.Button(top_frame, text="Anterior", command=self.prev_page).grid(row=0, column=1, padx=5)
        ttk.Button(top_frame, text="Siguiente", command=self.next_page).grid(row=0, column=2, padx=5)

        ttk.Label(top_frame, text="Página:").grid(row=0, column=3, padx=5)
        self.page_label = ttk.Label(top_frame, text="0 / 0")
        self.page_label.grid(row=0, column=4, padx=5)

        # Buscador
        search_frame = ttk.Frame(self.root)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.case_sensitive = tk.BooleanVar()
        ttk.Checkbutton(search_frame, text="Mayúsculas/Minúsculas", variable=self.case_sensitive).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.search_text).grid(row=0, column=3, padx=5)

        # Botón para resumen
        ttk.Button(search_frame, text="Resumir Página", command=self.summarize_page).grid(row=0, column=4, padx=5)

        # Área de texto
        self.text_area = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Configuración del layout
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if not file_path:
            return
        try:
            self.doc = fitz.open(file_path)
            self.total_pages = len(self.doc)
            self.current_page = 0
            self.show_page()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF:\n{e}")

    def show_page(self):
        if not self.doc or self.current_page < 0 or self.current_page >= self.total_pages:
            return
        page = self.doc.load_page(self.current_page)
        text = page.get_text()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.page_label.config(text=f"{self.current_page + 1} / {self.total_pages}")

    def next_page(self):
        if self.doc and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def search_text(self):
        query = self.search_entry.get()
        if not query:
            return
        content = self.text_area.get(1.0, tk.END)
        self.text_area.tag_remove("found", "1.0", tk.END)
        count = 0
        start = "1.0"
        while True:
            start = self.text_area.search(query, start, nocase=not self.case_sensitive.get(), stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(query)}c"
            self.text_area.tag_add("found", start, end)
            self.text_area.tag_config("found", background="yellow", foreground="black")
            start = end
            count += 1
        if count == 0:
            messagebox.showinfo("Buscar", "Texto no encontrado.")

    def summarize_page(self):
        if not self.doc:
            return
        threading.Thread(target=self._summarize_thread, daemon=True).start()

    def _summarize_thread(self):
        self.text_area.insert(tk.END, "\n\n[Resumiendo página...]\n")
        # Simulación de resumen, aquí podrías conectar un modelo real
        import time
        time.sleep(2)
        resumen = "Este es un resumen simulado de la página actual."
        self.text_area.insert(tk.END, resumen)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()
