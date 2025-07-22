import PyPDF2
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from PIL import Image, ImageTk
import threading
import time

class Archivos:
    def __init__(self, nombredel_archivo=None):
        self._nombredel_archivo = nombredel_archivo
        self._archivo = None
        self.status_callback = None
        
    @property
    def nombredel_archivo(self):
        return self._nombredel_archivo
        
    @nombredel_archivo.setter
    def nombredel_archivo(self, nuevo_nombre):
        self._nombredel_archivo = nuevo_nombre
        
    def set_status_callback(self, callback):
        self.status_callback = callback
        
    def update_status(self, message):
        if self.status_callback:
            self.status_callback(message)
        
    def abrir(self):
        try:
            if self._nombredel_archivo:
                self._archivo = open(self._nombredel_archivo, 'rb')
                self.update_status(f"Archivo abierto correctamente: {os.path.basename(self._nombredel_archivo)}")
                return True
        except FileNotFoundError:
            self.update_status("Error: No se encontró el archivo PDF")
        except Exception as e:
            self.update_status(f"Error al abrir el archivo: {str(e)}")
        return False
            
    def cerrar(self):
        if self._archivo:
            self._archivo.close()
            self.update_status("Archivo cerrado")
            
    def __del__(self):
        self.cerrar()


class LeerPDF(Archivos):
    def __init__(self, nombredel_archivo=None):
        super().__init__(nombredel_archivo)
        self._lector = None
        self._texto_extraido = ""
        self._paginas_totales = 0
        self._texto_por_pagina = {}
        
    def abrir_pdf(self):
        if self.abrir():
            try:
                self._lector = PyPDF2.PdfReader(self._archivo)
                self._paginas_totales = len(self._lector.pages)
                self.update_status(f"PDF cargado con éxito: {self._paginas_totales} páginas")
                return True
            except Exception as e:
                self.update_status(f"Error al cargar el PDF: {str(e)}")
        return False
            
    def extraer_texto(self, callback=None):
        if not self._lector:
            self.update_status("No se ha cargado el PDF")
            return ""
            
        self._texto_extraido = ""
        self._texto_por_pagina = {}
        
        for i, pagina in enumerate(self._lector.pages):
            try:
                texto_pagina = pagina.extract_text() + "\n"
                self._texto_por_pagina[i+1] = texto_pagina
                self._texto_extraido += texto_pagina
                if callback:
                    progreso = (i + 1) / self._paginas_totales * 100
                    callback(progreso, i+1)
                    
            except Exception as e:
                self.update_status(f"Error al extraer texto de la página {i+1}: {str(e)}")
                
        self.update_status("Texto extraído correctamente")
        return self._texto_extraido
    
    def obtener_texto_pagina(self, num_pagina):
        if 1 <= num_pagina <= self._paginas_totales:
            if num_pagina in self._texto_por_pagina:
                return self._texto_por_pagina[num_pagina]
            else:
                try:
                    texto = self._lector.pages[num_pagina-1].extract_text()
                    self._texto_por_pagina[num_pagina] = texto
                    return texto
                except Exception as e:
                    self.update_status(f"Error al extraer texto de la página {num_pagina}: {str(e)}")
                    return ""
        else:
            return f"Número de página inválido. El documento tiene {self._paginas_totales} páginas."
    
    def get_total_paginas(self):
        return self._paginas_totales
        
    def resumen_simple(self, cantidad_palabras=50):
        if not self._texto_extraido:
            self.extraer_texto()
            
        palabras = self._texto_extraido.split()
        resumen = " ".join(palabras[:cantidad_palabras])
        return resumen + "..." if len(palabras) > cantidad_palabras else resumen
    
    def buscar_texto(self, texto_buscar, distinguir_mayusculas=False):
        if not self._texto_extraido:
            self.extraer_texto()
            
        resultados = []
        
        for num_pagina, contenido in self._texto_por_pagina.items():
            if not distinguir_mayusculas:
                texto_buscar = texto_buscar.lower()
                contenido_comparar = contenido.lower()
            else:
                contenido_comparar = contenido
                
            if texto_buscar in contenido_comparar:
                resultados.append((num_pagina, contenido))
                
        return resultados


class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lector PDF Profesional")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Variables de control
        self.lector_pdf = LeerPDF()
        self.lector_pdf.set_status_callback(self.actualizar_estado)
        self.archivo_actual = None
        self.pagina_actual = tk.IntVar(value=1)
        self.palabras_resumen = tk.IntVar(value=50)
        self.distinguir_mayusculas = tk.BooleanVar(value=False)
        
        # Crear layout principal
        self.crear_interfaz()
        
    def configurar_estilos(self):
        # Colores
        self.COLOR_PRIMARY = "#1f77b4"
        self.COLOR_SECONDARY = "#ff7f0e"
        self.COLOR_BG = "#f8f9fa"
        self.COLOR_TEXT = "#212529"
        self.COLOR_ACCENT = "#28a745"
        self.COLOR_WARNING = "#dc3545"
        
        # Estilos ttk
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar estilos de botones
        estilo.configure('TButton', 
                         font=('Segoe UI', 10), 
                         background=self.COLOR_PRIMARY, 
                         foreground='white')
        
        estilo.configure('Accent.TButton', 
                         font=('Segoe UI', 10), 
                         background=self.COLOR_ACCENT, 
                         foreground='white')
        
        estilo.configure('TLabel', 
                         font=('Segoe UI', 10), 
                         background=self.COLOR_BG, 
                         foreground=self.COLOR_TEXT)
        
        estilo.configure('Header.TLabel', 
                         font=('Segoe UI', 12, 'bold'), 
                         background=self.COLOR_BG, 
                         foreground=self.COLOR_PRIMARY)
        
        estilo.configure('Status.TLabel', 
                         font=('Segoe UI', 9), 
                         background='#e9ecef', 
                         foreground=self.COLOR_TEXT)
        
        estilo.configure('TFrame', background=self.COLOR_BG)
        estilo.configure('TNotebook', background=self.COLOR_BG)
        estilo.configure('TNotebook.Tab', 
                         font=('Segoe UI', 10), 
                         padding=[10, 4], 
                         background=self.COLOR_BG)
        
        estilo.map('TNotebook.Tab', 
                   background=[('selected', self.COLOR_PRIMARY)],
                   foreground=[('selected', 'white')])
        
        # Configurar progressbar
        estilo.configure("TProgressbar", 
                         troughcolor='#e9ecef', 
                         background=self.COLOR_PRIMARY,
                         thickness=10)

    def crear_interfaz(self):
        # Configurar grid principal
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)  # Barra de herramientas
        self.root.rowconfigure(1, weight=1)  # Contenido principal
        self.root.rowconfigure(2, weight=0)  # Barra de estado
        
        # Barra de herramientas superior
        self.crear_barra_herramientas()
        
        # Panel contenido principal
        self.panel_principal = ttk.Frame(self.root)
        self.panel_principal.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.panel_principal.columnconfigure(0, weight=1)
        self.panel_principal.rowconfigure(0, weight=1)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.panel_principal)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Tab 1: Visor de texto
        self.tab_visor = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_visor, text="Visor PDF")
        self.crear_tab_visor()
        
        # Tab 2: Resumen
        self.tab_resumen = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resumen, text="Resumen")
        self.crear_tab_resumen()
        
        # Tab 3: Búsqueda
        self.tab_busqueda = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_busqueda, text="Búsqueda")
        self.crear_tab_busqueda()
        
        # Barra de estado
        self.crear_barra_estado()
        
    def crear_barra_herramientas(self):
        toolbar = ttk.Frame(self.root)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Botón abrir archivo
        self.btn_abrir = ttk.Button(toolbar, text="Abrir PDF", command=self.abrir_pdf)
        self.btn_abrir.pack(side=tk.LEFT, padx=5)
        
        # Botón extraer texto
        self.btn_extraer = ttk.Button(toolbar, text="Extraer Texto", 
                                      command=self.iniciar_extraccion,
                                      state="disabled")
        self.btn_extraer.pack(side=tk.LEFT, padx=5)
        
    def crear_tab_visor(self):
        self.tab_visor.columnconfigure(0, weight=1)
        self.tab_visor.rowconfigure(0, weight=0)  # Controles
        self.tab_visor.rowconfigure(1, weight=1)  # Texto
        
        # Panel de control de páginas
        panel_control = ttk.Frame(self.tab_visor)
        panel_control.grid(row=0, column=0, sticky="ew", pady=10)
        
        ttk.Label(panel_control, text="Página:").pack(side=tk.LEFT, padx=5)
        
        self.btn_anterior = ttk.Button(panel_control, text="◀", width=3,
                                      command=self.pagina_anterior,
                                      state="disabled")
        self.btn_anterior.pack(side=tk.LEFT, padx=2)
        
        self.entry_pagina = ttk.Entry(panel_control, textvariable=self.pagina_actual, width=5)
        self.entry_pagina.pack(side=tk.LEFT, padx=2)
        self.entry_pagina.bind('<Return>', lambda e: self.cambiar_pagina())
        
        self.lbl_total_paginas = ttk.Label(panel_control, text="de 0")
        self.lbl_total_paginas.pack(side=tk.LEFT, padx=2)
        
        self.btn_siguiente = ttk.Button(panel_control, text="▶", width=3,
                                       command=self.pagina_siguiente,
                                       state="disabled")
        self.btn_siguiente.pack(side=tk.LEFT, padx=2)
        
        # Área de texto
        frame_texto = ttk.Frame(self.tab_visor)
        frame_texto.grid(row=1, column=0, sticky="nsew", pady=5)
        frame_texto.columnconfigure(0, weight=1)
        frame_texto.rowconfigure(0, weight=1)
        
        self.texto_pdf = scrolledtext.ScrolledText(frame_texto, wrap=tk.WORD, 
                                                  font=('Segoe UI', 11),
                                                  bg='white', fg=self.COLOR_TEXT)
        self.texto_pdf.grid(row=0, column=0, sticky="nsew")
        
    def crear_tab_resumen(self):
        self.tab_resumen.columnconfigure(0, weight=1)
        self.tab_resumen.rowconfigure(0, weight=0)  # Controles
        self.tab_resumen.rowconfigure(1, weight=1)  # Contenido
        
        # Controles
        panel_resumen = ttk.Frame(self.tab_resumen)
        panel_resumen.grid(row=0, column=0, sticky="ew", pady=10)
        
        ttk.Label(panel_resumen, text="Palabras:").pack(side=tk.LEFT, padx=5)
        
        spin_palabras = ttk.Spinbox(panel_resumen, from_=10, to=200, increment=10,
                                   textvariable=self.palabras_resumen, width=5)
        spin_palabras.pack(side=tk.LEFT, padx=5)
        
        btn_generar = ttk.Button(panel_resumen, text="Generar Resumen",
                                command=self.generar_resumen,
                                style='Accent.TButton')
        btn_generar.pack(side=tk.LEFT, padx=5)
        
        # Área de resumen
        frame_resumen = ttk.Frame(self.tab_resumen)
        frame_resumen.grid(row=1, column=0, sticky="nsew", pady=5)
        frame_resumen.columnconfigure(0, weight=1)
        frame_resumen.rowconfigure(0, weight=1)
        
        self.texto_resumen = scrolledtext.ScrolledText(frame_resumen, wrap=tk.WORD,
                                                      font=('Segoe UI', 11),
                                                      bg='white', fg=self.COLOR_TEXT)
        self.texto_resumen.grid(row=0, column=0, sticky="nsew")
        
    def crear_tab_busqueda(self):
        self.tab_busqueda.columnconfigure(0, weight=1)
        self.tab_busqueda.rowconfigure(0, weight=0)  # Controles
        self.tab_busqueda.rowconfigure(1, weight=1)  # Resultados
        
        # Controles de búsqueda
        panel_busqueda = ttk.Frame(self.tab_busqueda)
        panel_busqueda.grid(row=0, column=0, sticky="ew", pady=10)
        
        ttk.Label(panel_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
        
        self.entry_busqueda = ttk.Entry(panel_busqueda, width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        
        check_mayusculas = ttk.Checkbutton(panel_busqueda, text="Diferenciar mayúsculas/minúsculas",
                                         variable=self.distinguir_mayusculas)
        check_mayusculas.pack(side=tk.LEFT, padx=5)
        
        btn_buscar = ttk.Button(panel_busqueda, text="Buscar",
                               command=self.buscar_en_pdf,
                               style='Accent.TButton')
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Resultados
        frame_resultados = ttk.Frame(self.tab_busqueda)
        frame_resultados.grid(row=1, column=0, sticky="nsew")
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
        
        # Treeview para resultados
        self.tree_resultados = ttk.Treeview(frame_resultados, 
                                           columns=("pagina", "vista_previa"),
                                           show="headings")
        self.tree_resultados.heading("pagina", text="Página")
        self.tree_resultados.heading("vista_previa", text="Vista previa")
        self.tree_resultados.column("pagina", width=80, anchor="center")
        self.tree_resultados.column("vista_previa", width=400)
        self.tree_resultados.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", 
                                 command=self.tree_resultados.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_resultados.configure(yscrollcommand=scrollbar.set)
        
        # Evento al hacer doble clic en un resultado
        self.tree_resultados.bind("<Double-1>", self.ir_a_resultado)
        
    def crear_barra_estado(self):
        # Frame para la barra de estado
        barra_estado = ttk.Frame(self.root, style='Status.TLabel')
        barra_estado.grid(row=2, column=0, sticky="ew")
        barra_estado.columnconfigure(0, weight=1)
        barra_estado.columnconfigure(1, weight=0)
        
        # Etiqueta para mostrar mensajes de estado
        self.lbl_estado = ttk.Label(barra_estado, style='Status.TLabel')
        self.lbl_estado.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(barra_estado, orient="horizontal", 
                                             length=150, mode="determinate",
                                             style="TProgressbar")
        self.barra_progreso.grid(row=0, column=1, padx=10, pady=5)
        
    def abrir_pdf(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            self.archivo_actual = ruta_archivo
            self.lector_pdf = LeerPDF(ruta_archivo)
            self.lector_pdf.set_status_callback(self.actualizar_estado)
            
            if self.lector_pdf.abrir_pdf():
                # Actualizar estado de los controles
                self.btn_extraer.config(state="normal")
                self.actualizar_info_paginas()
                self.mostrar_pagina(1)
                
                # Limpiar otras pestañas
                self.texto_resumen.delete(1.0, tk.END)
                for item in self.tree_resultados.get_children():
                    self.tree_resultados.delete(item)
                    
    def iniciar_extraccion(self):
        # Deshabilitar controles durante la extracción
        self.btn_extraer.config(state="disabled")
        self.btn_abrir.config(state="disabled")
        
        # Iniciar extracción en un hilo separado
        threading.Thread(target=self.extraer_texto_hilo, daemon=True).start()
        
    def extraer_texto_hilo(self):
        def actualizar_progreso(progreso, pagina_actual):
            self.barra_progreso["value"] = progreso
            self.actualizar_estado(f"Extrayendo texto: página {pagina_actual} de {self.lector_pdf.get_total_paginas()}")
            self.root.update_idletasks()
            
        self.lector_pdf.extraer_texto(callback=actualizar_progreso)
        
        # Actualizar la interfaz desde el hilo principal
        self.root.after(0, self.finalizar_extraccion)
        
    def finalizar_extraccion(self):
        # Restablecer controles
        self.btn_extraer.config(state="normal")
        self.btn_abrir.config(state="normal")
        self.barra_progreso["value"] = 0
        
        # Activar navegación
        self.btn_anterior.config(state="normal")
        self.btn_siguiente.config(state="normal")
        
        # Mostrar primera página
        self.mostrar_pagina(1)
        
    def actualizar_info_paginas(self):
        total_paginas = self.lector_pdf.get_total_paginas()
        self.lbl_total_paginas.config(text=f"de {total_paginas}")
        
        if total_paginas > 0:
            self.pagina_actual.set(1)
        
    def mostrar_pagina(self, num_pagina):
        if not self.lector_pdf:
            return
            
        if num_pagina < 1:
            num_pagina = 1
        elif num_pagina > self.lector_pdf.get_total_paginas():
            num_pagina = self.lector_pdf.get_total_paginas()
            
        self.pagina_actual.set(num_pagina)
        texto = self.lector_pdf.obtener_texto_pagina(num_pagina)
        
        self.texto_pdf.delete(1.0, tk.END)
        self.texto_pdf.insert(1.0, texto)
        
    def cambiar_pagina(self):
        try:
            pagina = self.pagina_actual.get()
            self.mostrar_pagina(pagina)
        except:
            pass
            
    def pagina_anterior(self):
        pagina = self.pagina_actual.get() - 1
        self.mostrar_pagina(pagina)
        
    def pagina_siguiente(self):
        pagina = self.pagina_actual.get() + 1
        self.mostrar_pagina(pagina)
        
    def generar_resumen(self):
        if not self.lector_pdf:
            self.actualizar_estado("No hay un PDF cargado")
            return
            
        palabras = self.palabras_resumen.get()
        resumen = self.lector_pdf.resumen_simple(palabras)
        
        self.texto_resumen.delete(1.0, tk.END)
        self.texto_resumen.insert(1.0, resumen)
        
    def buscar_en_pdf(self):
        if not self.lector_pdf:
            self.actualizar_estado("No hay un PDF cargado")
            return
            
        texto_buscar = self.entry_busqueda.get().strip()
        if not texto_buscar:
            self.actualizar_estado("Ingrese un texto para buscar")
            return
            
        # Limpiar resultados anteriores
        for item in self.tree_resultados.get_children():
            self.tree_resultados.delete(item)
            
        # Realizar búsqueda
        resultados = self.lector_pdf.buscar_texto(
            texto_buscar, 
            self.distinguir_mayusculas.get()
        )
        
        if not resultados:
            self.actualizar_estado(f"No se encontraron coincidencias para '{texto_buscar}'")
            return
            
        # Mostrar resultados
        for pagina, contenido in resultados:
            # Obtener fragmento de texto con contexto
            indice = contenido.lower().find(texto_buscar.lower())
            inicio = max(0, indice - 30)
            fin = min(len(contenido), indice + len(texto_buscar) + 30)
            
            # Crear fragmento con el texto encontrado
            if inicio > 0:
                fragmento = "..." + contenido[inicio:fin] + "..."
            else:
                fragmento = contenido[inicio:fin] + "..."
                
            self.tree_resultados.insert("", "end", values=(pagina, fragmento))
            
        self.actualizar_estado(f"Se encontraron {len(resultados)} coincidencias para '{texto_buscar}'")
        
    def ir_a_resultado(self, event):
        seleccion = self.tree_resultados.selection()
        if seleccion:
            item = self.tree_resultados.item(seleccion[0])
            pagina = int(item['values'][0])
            
            # Cambiar a la pestaña del visor y mostrar la página
            self.notebook.select(0)  # Seleccionar primera pestaña
            self.mostrar_pagina(pagina)
        
    def actualizar_estado(self, mensaje):
        self.lbl_estado.config(text=mensaje)
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()