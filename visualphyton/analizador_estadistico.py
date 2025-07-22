import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
import numpy as np
import threading
import sys
from io import StringIO
import json
import os
from datetime import datetime
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw
import plotly.graph_objects as go
import plotly.express as px
import webbrowser

# --- Asumimos que este es el contenido de 'analizador_estadistico_mejorado.py' ---
# Para que el código sea autoejecutable, lo incluyo aquí.
# En un proyecto real, estaría en un archivo separado.

class AnalizadorEstadisticoAvanzado:
    """
    Una clase mejorada para realizar análisis estadísticos completos de un DataFrame.
    """
    def __init__(self, dataframe=None):

        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("La entrada debe ser un DataFrame de pandas.")
        self.df = dataframe.copy()
        self.numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()

    def resumen_descriptivo(self):
        """Genera estadísticas descriptivas para columnas numéricas."""
        if not self.numeric_cols:
            return "No hay columnas numéricas para analizar."
        
        # Uso de StringIO para capturar la salida de .info()
        buffer = StringIO()
        self.df.info(buf=buffer)
        info_str = buffer.getvalue()

        desc = self.df[self.numeric_cols].describe().T
        desc['median'] = self.df[self.numeric_cols].median()
        desc['mode'] = self.df[self.numeric_cols].mode().iloc[0]
        desc['variance'] = self.df[self.numeric_cols].var()
        desc['skew'] = self.df[self.numeric_cols].skew()
        desc['kurtosis'] = self.df[self.numeric_cols].kurtosis()
        
        return f"Información General del DataFrame:\n{info_str}\n\nEstadísticas Descriptivas:\n{desc.to_string()}"

    def distribucion_frecuencias(self):
        """Genera tablas de distribución de frecuencias para columnas categóricas."""
        if not self.categorical_cols:
            return "No hay columnas categóricas para analizar."
        
        reporte = ""
        for col in self.categorical_cols:
            freq_table = self.df[col].value_counts().to_frame(name='Frecuencia')
            freq_table['Porcentaje (%)'] = (self.df[col].value_counts(normalize=True) * 100).round(2)
            reporte += f"--- Distribución de Frecuencias para '{col}' ---\n"
            reporte += freq_table.to_string() + "\n\n"
        return reporte

    def analisis_correlacion(self, metodo='pearson'):
        """Calcula la matriz de correlación de las variables numéricas."""
        if len(self.numeric_cols) < 2:
            return None, "Se necesitan al menos dos columnas numéricas para el análisis de correlación."
        
        matriz_corr = self.df[self.numeric_cols].corr(method=metodo)
        return matriz_corr, f"Matriz de Correlación (Método: {metodo})"

    def detectar_outliers_iqr(self, columna):
        """Detecta outliers en una columna numérica usando el Rango Intercuartílico (IQR)."""
        if columna not in self.numeric_cols:
            return f"La columna '{columna}' no es numérica."
        
        Q1 = self.df[columna].quantile(0.25)
        Q3 = self.df[columna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[columna] < limite_inferior) | (self.df[columna] > limite_superior)]
        
        if outliers.empty:
            return f"No se detectaron outliers en '{columna}' usando el método IQR."
        
        return f"Outliers detectados en '{columna}':\n{outliers[[columna]].to_string()}"

# --- Clases de Widgets Personalizados ---

class ModernScrollableFrame:
    """Frame scrollable moderno con efectos visuales"""
    def __init__(self, parent, bg_color="#1a1a2e"):
        container = tk.Frame(parent, bg=bg_color)
        self.canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        container.pack(fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class AnimatedButton(tk.Canvas):
    """Botón personalizado con efectos de animación"""
    def __init__(self, parent, text="", command=None, bg_color="#0f3460", 
                 hover_color="#16537e", text_color="white", width=120, height=35):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.command = command
        
        self.configure(bg=parent['bg'])
        
        self.rect = self.create_rectangle(0, 0, width, height, fill=bg_color, outline="")
        self.text_id = self.create_text(width/2, height/2, text=text, 
                                        fill=text_color, font=("Segoe UI", 10, "bold"))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)

    def on_click(self, event):
        if self.command:
            self.command()

class ModernProgressBar(tk.Canvas):
    """Barra de progreso moderna con efectos de degradado"""
    def __init__(self, parent, width=300, height=10, bg_color="#2d2d44", 
                 start_color="#00d4aa", end_color="#00836a", text_color="white"):
        super().__init__(parent, width=width, height=height + 15, bg=parent['bg'], highlightthickness=0)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.start_color = start_color
        self.end_color = end_color
        self.text_color = text_color
        
        self.progress = 0
        
        # Fondo de la barra
        self.create_rectangle(0, 5, width, height + 5, fill=bg_color, outline="")
        
        # Etiqueta de texto
        self.text_label = self.create_text(width / 2, height + 15, text="0%", fill=text_color, font=("Segoe UI", 8))

    def set_progress(self, value):
        """Actualiza el progreso (0 a 100)"""
        self.progress = max(0, min(100, value))
        self.delete("progress") # Borra el degradado anterior
        
        # Dibuja el nuevo degradado
        progress_width = (self.width * self.progress) / 100
        if progress_width > 0:
            self.draw_gradient(0, 5, progress_width, self.height + 5)
        
        # Actualiza el texto
        self.itemconfig(self.text_label, text=f"{int(self.progress)}%")
        self.update_idletasks()

    def draw_gradient(self, x0, y0, x1, y1):
        """Dibuja un degradado horizontal"""
        r1, g1, b1 = self.winfo_rgb(self.start_color)
        r2, g2, b2 = self.winfo_rgb(self.end_color)
        
        for i in range(int(x1 - x0)):
            nr = int(r1 + (r2 - r1) * i / (x1 - x0))
            ng = int(g1 + (g2 - g1) * i / (x1 - x0))
            nb = int(b1 + (b2 - b1) * i / (x1 - x0))
            color = f"#{nr:04x}{ng:04x}{nb:04x}"
            self.create_line(x0 + i, y0, x0 + i, y1, fill=color, tags="progress")

# --- Clase Principal de la Aplicación ---

class AnalizadorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Estadístico Avanzado")
        self.geometry("1200x750")
        self.configure(bg="#1a1a2e")
        self.data = None
        self.analizador = None

        # --- Estilos y Fuentes ---
        self.font_title = tkFont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_label = tkFont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_text = tkFont.Font(family="Segoe UI", size=10)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#2d2d44", background="#2d2d44", foreground="white", arrowcolor="white")
        style.configure("TScrollbar", background="#1a1a2e", troughcolor="#2d2d44", bordercolor="#1a1a2e", arrowcolor="white")

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome_frame = tk.Frame(self, bg="#1a1a2e")
        
        # Simula un logo (puedes reemplazarlo con una imagen)
        logo_canvas = tk.Canvas(self.welcome_frame, width=150, height=150, bg="#1a1a2e", highlightthickness=0)
        logo_canvas.create_oval(10, 10, 140, 140, outline="#e94560", width=4)
        logo_canvas.create_text(75, 75, text="STAT\nPRO", fill="white", font=("Segoe UI", 24, "bold"), justify="center")
        logo_canvas.pack(pady=50)

        tk.Label(self.welcome_frame, text="Analizador Estadístico Pro", font=self.font_title, fg="white", bg="#1a1a2e").pack(pady=(0, 20))
        tk.Label(self.welcome_frame, text="Cargando componentes...", font=self.font_label, fg="#a0a0a0", bg="#1a1a2e").pack(pady=10)
        
        self.welcome_frame.pack(fill="both", expand=True)
        self.after(2500, self.setup_main_ui) # Muestra la pantalla por 2.5 segundos

    def setup_main_ui(self):
        self.welcome_frame.destroy()
        
        # --- Frame Superior (Controles) ---
        top_frame = tk.Frame(self, bg="#0f3460", height=80, relief='solid', borderwidth=1)
        top_frame.pack(side="top", fill="x", padx=10, pady=10)
        top_frame.pack_propagate(False)

        AnimatedButton(top_frame, text="Cargar CSV", command=self.cargar_datos, width=150, height=40).pack(side="left", padx=20, pady=20)
        self.file_label = tk.Label(top_frame, text="Ningún archivo cargado", fg="white", bg="#0f3460", font=self.font_text)
        self.file_label.pack(side="left")

        # --- Frame Principal (Contenido) ---
        main_content_frame = tk.Frame(self, bg="#1a1a2e")
        main_content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- Columna Izquierda (Selección y Análisis) ---
        left_panel = tk.Frame(main_content_frame, bg="#1a1a2e", width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        # Sección de Variables
        vars_frame = tk.LabelFrame(left_panel, text="Selección de Variables", fg="white", bg="#1a1a2e", font=self.font_label, relief='groove')
        vars_frame.pack(fill="x", pady=10)
        
        tk.Label(vars_frame, text="Variable Numérica:", fg="white", bg="#1a1a2e", font=self.font_text).pack(anchor="w", padx=10, pady=(10, 0))
        self.numeric_var_combo = ttk.Combobox(vars_frame, state='readonly', width=35)
        self.numeric_var_combo.pack(padx=10, pady=5)
        
        tk.Label(vars_frame, text="Variable Categórica:", fg="white", bg="#1a1a2e", font=self.font_text).pack(anchor="w", padx=10, pady=(10, 0))
        self.categorical_var_combo = ttk.Combobox(vars_frame, state='readonly', width=35)
        self.categorical_var_combo.pack(padx=10, pady=(0, 15))


        # Sección de Análisis
        analysis_frame = tk.LabelFrame(left_panel, text="Tipos de Análisis y Gráficos", fg="white", bg="#1a1a2e", font=self.font_label, relief='groove')
        analysis_frame.pack(fill="x", pady=10)

        AnimatedButton(analysis_frame, text="Resumen Descriptivo", command=lambda: self.ejecutar_analisis('resumen'), width=280, height=35).pack(pady=8, padx=10)
        AnimatedButton(analysis_frame, text="Distribución de Frecuencias", command=lambda: self.ejecutar_analisis('frecuencias'), width=280, height=35).pack(pady=8, padx=10)
        AnimatedButton(analysis_frame, text="Mapa de Calor de Correlación", command=lambda: self.ejecutar_analisis('correlacion'), width=280, height=35).pack(pady=8, padx=10)
        AnimatedButton(analysis_frame, text="Histograma y Boxplot (Num)", command=lambda: self.ejecutar_analisis('histograma_boxplot'), width=280, height=35).pack(pady=8, padx=10)
        AnimatedButton(analysis_frame, text="Gráfico de Barras (Cat)", command=lambda: self.ejecutar_analisis('barras'), width=280, height=35).pack(pady=8, padx=10)
        AnimatedButton(analysis_frame, text="Detectar Outliers (IQR)", command=lambda: self.ejecutar_analisis('outliers'), width=280, height=35).pack(pady=8, padx=10)

        # Barra de Progreso
        self.progress_bar = ModernProgressBar(left_panel, width=330)
        self.progress_bar.pack(pady=20)

        # --- Columna Derecha (Resultados) ---
        right_panel = tk.Frame(main_content_frame, bg="#2d2d44", relief='solid', borderwidth=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.notebook = ttk.Notebook(right_panel)
        style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d44", foreground="white", padding=[10, 5], font=self.font_text)
        style.map("TNotebook.Tab", background=[("selected", "#e94560")])

        self.results_tab = tk.Frame(self.notebook, bg="#1a1a2e")
        self.plot_tab = tk.Frame(self.notebook, bg="#1a1a2e")

        self.notebook.add(self.results_tab, text='Resultados de Texto')
        self.notebook.add(self.plot_tab, text='Visualización de Gráficos')
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Contenido de la pestaña de resultados
        self.results_text = scrolledtext.ScrolledText(self.results_tab, wrap=tk.WORD, bg="#101020", fg="white", font=self.font_text, relief='flat')
        self.results_text.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Contenido de la pestaña de gráficos
        self.plot_canvas_frame = tk.Frame(self.plot_tab, bg="#1a1a2e")
        self.plot_canvas_frame.pack(expand=True, fill='both')
        self.plot_canvas = None # Se creará dinámicamente

        # Botones de exportación
        export_frame = tk.Frame(left_panel, bg="#1a1a2e")
        export_frame.pack(pady=10)
        AnimatedButton(export_frame, text="Exportar Resultado", command=self.exportar_resultados, width=150, height=35).pack(side="left", padx=5)
        AnimatedButton(export_frame, text="Exportar Gráfico", command=self.exportar_grafico, width=150, height=35).pack(side="left", padx=5)

    def cargar_datos(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
        )
        if not file_path:
            return

        try:
            self.data = pd.read_csv(file_path)
            self.analizador = AnalizadorEstadisticoAvanzado(self.data)
            self.file_label.config(text=os.path.basename(file_path))
            
            # Poblar comboboxes
            self.numeric_var_combo['values'] = self.analizador.numeric_cols
            self.categorical_var_combo['values'] = self.analizador.categorical_cols
            if self.analizador.numeric_cols:
                self.numeric_var_combo.set(self.analizador.numeric_cols[0])
            if self.analizador.categorical_cols:
                self.categorical_var_combo.set(self.analizador.categorical_cols[0])
            
            messagebox.showinfo("Éxito", f"Datos cargados correctamente.\nFilas: {self.data.shape[0]}, Columnas: {self.data.shape[1]}")
            self.mostrar_dataframe_head()
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"No se pudo cargar el archivo.\nError: {e}")
            self.data = None
            self.analizador = None

    def mostrar_dataframe_head(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Primeras 5 filas del DataFrame:\n\n")
        self.results_text.insert(tk.END, self.data.head().to_string())
        self.notebook.select(self.results_tab)

    def ejecutar_analisis(self, tipo_analisis):
        if self.data is None:
            messagebox.showwarning("Sin Datos", "Por favor, carga un archivo CSV primero.")
            return

        # Deshabilitar botones para evitar múltiples clics
        # (Implementación más robusta sería necesaria para una app compleja)
        
        self.progress_bar.set_progress(0)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Ejecutando '{tipo_analisis}'... por favor espera.\n")
        self.update_idletasks()

        # Usar un hilo para no bloquear la GUI
        thread = threading.Thread(target=self.ejecutar_analisis_thread, args=(tipo_analisis,))
        thread.start()

    def ejecutar_analisis_thread(self, tipo_analisis):
        try:
            resultado = None
            self.current_plot = None # Para guardar la figura actual
            self.current_plot_interactive = None # Para guardar el plot de Plotly

            # Simular progreso
            for i in range(1, 101):
                self.progress_bar.set_progress(i)
            
            if tipo_analisis == 'resumen':
                resultado = self.analizador.resumen_descriptivo()
                self.notebook.select(self.results_tab)
            elif tipo_analisis == 'frecuencias':
                resultado = self.analizador.distribucion_frecuencias()
                self.notebook.select(self.results_tab)
            elif tipo_analisis == 'correlacion':
                matriz_corr, titulo = self.analizador.analisis_correlacion()
                if matriz_corr is not None:
                    resultado = f"{titulo}\n\n{matriz_corr.to_string()}"
                    # Usar Plotly para el mapa de calor interactivo
                    fig = px.imshow(matriz_corr, text_auto=True, aspect="auto",
                                    color_continuous_scale='viridis',
                                    title="Mapa de Calor de Correlación Interactivo")
                    self.current_plot_interactive = fig
                    self.mostrar_grafico_interactivo(fig)
                else:
                    resultado = titulo
                self.notebook.select(self.plot_tab)
            elif tipo_analisis == 'histograma_boxplot':
                var = self.numeric_var_combo.get()
                if not var:
                    raise ValueError("Selecciona una variable numérica.")
                resultado = f"Mostrando Histograma y Boxplot para '{var}'."
                # Usar Plotly para un gráfico combinado
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=self.data[var], name='Histograma'))
                fig.add_trace(go.Box(x=self.data[var], name='Boxplot', yaxis='y2'))
                fig.update_layout(
                    title_text=f"Distribución de {var}",
                    xaxis_title=var,
                    yaxis_title="Frecuencia",
                    yaxis2=dict(title="Boxplot", overlaying='y', side='right', showticklabels=False),
                    template="plotly_dark"
                )
                self.current_plot_interactive = fig
                self.mostrar_grafico_interactivo(fig)
                self.notebook.select(self.plot_tab)
            elif tipo_analisis == 'barras':
                var = self.categorical_var_combo.get()
                if not var:
                    raise ValueError("Selecciona una variable categórica.")
                resultado = f"Mostrando Gráfico de Barras para '{var}'."
                # Usar Plotly para el gráfico de barras interactivo
                counts = self.data[var].value_counts()
                fig = px.bar(x=counts.index, y=counts.values, title=f"Distribución de {var}",
                             labels={'x': var, 'y': 'Conteo'}, text_auto=True,
                             template="plotly_dark")
                fig.update_traces(marker_color='#e94560')
                self.current_plot_interactive = fig
                self.mostrar_grafico_interactivo(fig)
                self.notebook.select(self.plot_tab)
            elif tipo_analisis == 'outliers':
                var = self.numeric_var_combo.get()
                if not var:
                    raise ValueError("Selecciona una variable numérica.")
                resultado = self.analizador.detectar_outliers_iqr(var)
                self.notebook.select(self.results_tab)
            else:
                resultado = "Análisis no reconocido."

            # Actualizar la GUI desde el hilo principal
            self.after(0, self.actualizar_ui_resultados, resultado)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error en Análisis", str(e)))
        finally:
            # Resetear la barra de progreso
            self.after(100, lambda: self.progress_bar.set_progress(0))

    def actualizar_ui_resultados(self, resultado):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, resultado)

    def mostrar_grafico_interactivo(self, fig):
        """Muestra un gráfico de Plotly guardándolo como HTML y abriéndolo en el navegador."""
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
        
        # Guardar gráfico y abrir en navegador para interactividad completa
        path = os.path.join(os.getcwd(), "interactive_plot.html")
        fig.write_html(path)
        
        # Mostrar una notificación en la GUI
        for widget in self.plot_canvas_frame.winfo_children():
            widget.destroy()
            
        label = tk.Label(self.plot_canvas_frame,
                         text="El gráfico interactivo se ha abierto en tu navegador web.\n\n"
                              "Cierra esta ventana y selecciona otro análisis para continuar.",
                         font=self.font_label, fg="white", bg="#1a1a2e", wraplength=400)
        label.pack(expand=True)
        
        # Guardar la figura de Matplotlib para la exportación de imagen estática
        self.current_plot = self.plotly_to_matplotlib(fig)
        
        webbrowser.open('file://' + path)

    def plotly_to_matplotlib(self, fig_plotly):
        """Convierte una figura de Plotly a una figura de Matplotlib para guardarla como imagen."""
        # Esta es una conversión simple, puede no funcionar para todos los tipos de gráficos complejos
        fig_matplotlib = plt.figure(facecolor="#1a1a2e")
        ax = fig_matplotlib.add_subplot(111)
        ax.set_facecolor("#2d2d44")
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')

        for trace in fig_plotly.data:
            if isinstance(trace, go.Histogram):
                counts, bins = np.histogram(trace.x, bins='auto')
                ax.hist(trace.x, bins=bins, color='#00d4aa', alpha=0.7)
            elif isinstance(trace, go.Bar):
                ax.bar(trace.x, trace.y, color=trace.marker.color or '#e94560')
            elif isinstance(trace, go.Box):
                ax.boxplot(trace.x, vert=False, patch_artist=True,
                           boxprops=dict(facecolor='#16537e', color='white'),
                           whiskerprops=dict(color='white'),
                           capprops=dict(color='white'),
                           medianprops=dict(color='yellow'))
        
        ax.set_title(fig_plotly.layout.title.text if fig_plotly.layout.title else "")
        ax.set_xlabel(fig_plotly.layout.xaxis.title.text if fig_plotly.layout.xaxis.title else "")
        ax.set_ylabel(fig_plotly.layout.yaxis.title.text if fig_plotly.layout.yaxis.title else "")
        plt.tight_layout()
        return fig_matplotlib

    def exportar_resultados(self):
        contenido = self.results_text.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showwarning("Vacío", "No hay resultados para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Guardar Resultado Como"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    # Intenta convertir el texto a un diccionario para un JSON bonito
                    try:
                        # Esto es una heurística; puede fallar si el formato no es simple
                        data_dict = {"resultado": contenido}
                        json.dump(data_dict, f, indent=4)
                    except:
                        f.write(json.dumps({"raw_text": contenido}))
                else:
                    f.write(contenido)
            messagebox.showinfo("Éxito", f"Resultado guardado en {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo.\nError: {e}")

    def exportar_grafico(self):
        if self.current_plot_interactive is None:
            messagebox.showwarning("Sin Gráfico", "No hay un gráfico generado para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Archivo de Imagen PNG", "*.png"), ("Archivo Interactivo HTML", "*.html")],
            title="Guardar Gráfico Como"
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.html'):
                self.current_plot_interactive.write_html(file_path)
            elif file_path.endswith('.png'):
                # Usa la figura de Matplotlib guardada para exportar como PNG
                if self.current_plot:
                    self.current_plot.savefig(file_path, dpi=300, facecolor=self.current_plot.get_facecolor())
                else: # Fallback si la conversión no fue posible
                    self.current_plot_interactive.write_image(file_path)

            messagebox.showinfo("Éxito", f"Gráfico guardado en {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el gráfico.\nError: {e}")


if __name__ == "__main__":
    app = AnalizadorGUI()
    app.mainloop()