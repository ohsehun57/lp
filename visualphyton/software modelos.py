import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import threading
from PIL import Image, ImageTk

# --- Módulo de Análisis Estadístico Integrado ---
# He creado esta clase para que el script sea autocontenido.
# Utiliza statsmodels para un análisis robusto.

class AnalizadorEstadistico:
    """
    Clase para realizar un análisis de regresión lineal múltiple,
    verificación de supuestos y generación de resultados y gráficos.
    """
    def __init__(self):
        self.data = None
        self.dependiente = None
        self.independientes = None
        self.modelo = None
        self.resultados = None

    def cargar_datos(self, archivo, dependiente, independientes):
        """Carga datos desde un archivo .csv o .xlsx."""
        if not (archivo and dependiente and independientes):
            raise ValueError("Archivo, variable dependiente e independientes son requeridos.")
            
        try:
            if archivo.endswith('.csv'):
                self.data = pd.read_csv(archivo)
            else:
                self.data = pd.read_excel(archivo)
        except Exception as e:
            raise IOError(f"Error al leer el archivo: {e}")

        self.dependiente = dependiente
        self.independientes = independientes
        
        # Validar que las columnas existen en el DataFrame
        columnas_requeridas = [dependiente] + independientes
        for col in columnas_requeridas:
            if col not in self.data.columns:
                raise ValueError(f"La columna '{col}' no se encuentra en el archivo.")

    def realizar_analisis_completo(self):
        """
        Ejecuta todo el flujo de análisis y devuelve un diccionario con resultados.
        """
        if self.data is None:
            raise ValueError("No se han cargado datos.")

        # Preparar datos y modelo
        y = self.data[self.dependiente]
        X = self.data[self.independientes]
        X = sm.add_constant(X) # Añadir constante (intercepto)
        self.modelo = sm.OLS(y, X)
        self.resultados = self.modelo.fit()

        # Generar todos los resultados
        resultados_dict = {
            "resumen_spss": self._generar_resumen_spss(),
            "supuestos_texto": self._generar_texto_supuestos(),
            "supuestos_graficos": self._generar_graficos_supuestos(),
            "grafico_dispersion": self._generar_grafico_dispersion(),
            "ecuacion": self._generar_ecuacion()
        }
        return resultados_dict

    def _generar_resumen_spss(self):
        """Genera un resumen de regresión similar al de SPSS."""
        # Esto es una simplificación del resumen de statsmodels
        return str(self.resultados.summary())

    def _generar_texto_supuestos(self):
        """Genera un reporte de texto con la verificación de supuestos."""
        X_for_vif = sm.add_constant(self.data[self.independientes])
        
        # 1. Multicolinealidad (VIF)
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X_for_vif.columns
        vif_data["VIF"] = [variance_inflation_factor(X_for_vif.values, i) for i in range(X_for_vif.shape[1])]
        
        # 2. Normalidad de los residuos (Shapiro-Wilk)
        shapiro_test = stats.shapiro(self.resultados.resid)
        
        # 3. Homocedasticidad (Breusch-Pagan)
        bp_test = sm.stats.het_breuschpagan(self.resultados.resid, self.resultados.model.exog)
        
        # 4. Autocorrelación de residuos (Durbin-Watson)
        dw_test = sm.stats.durbin_watson(self.resultados.resid)
        
        # Construir el reporte
        reporte = "🔍 VERIFICACIÓN DE SUPUESTOS\n" + "="*40 + "\n\n"
        reporte += "1. No Multicolinealidad (VIF - Factor de Inflación de Varianza):\n"
        reporte += "   (Valores > 5 o 10 pueden indicar un problema)\n"
        reporte += vif_data.to_string(index=False) + "\n\n"
        reporte += "-"*40 + "\n"
        reporte += "2. Normalidad de los Residuos (Test de Shapiro-Wilk):\n"
        reporte += f"   Estadístico W: {shapiro_test.statistic:.4f}, p-valor: {shapiro_test.pvalue:.4f}\n"
        reporte += "   (Si p > 0.05, los residuos se distribuyen normalmente)\n\n"
        reporte += "-"*40 + "\n"
        reporte += "3. Homocedasticidad (Test de Breusch-Pagan):\n"
        reporte += f"   Estadístico LM: {bp_test[0]:.4f}, p-valor: {bp_test[1]:.4f}\n"
        reporte += "   (Si p > 0.05, se cumple la homocedasticidad - varianza constante)\n\n"
        reporte += "-"*40 + "\n"
        reporte += "4. No Autocorrelación de Residuos (Test de Durbin-Watson):\n"
        reporte += f"   Estadístico DW: {dw_test:.4f}\n"
        reporte += "   (Valores cercanos a 2 sugieren no autocorrelación)\n"
        
        return reporte

    def _generar_graficos_supuestos(self):
        """Genera los gráficos de diagnóstico de supuestos."""
        fig = plt.figure(figsize=(10, 8))
        gs = fig.add_gridspec(2, 1)

        # Gráfico de Residuos vs Ajustados (Homocedasticidad)
        ax1 = fig.add_subplot(gs[0, 0])
        sns.residplot(x=self.resultados.fittedvalues, y=self.resultados.resid, lowess=True, 
                      scatter_kws={'alpha': 0.5}, 
                      line_kws={'color': 'red', 'lw': 1.5}, ax=ax1)
        ax1.set_title('Residuos vs. Valores Ajustados', fontsize=12)
        ax1.set_xlabel('Valores Ajustados')
        ax1.set_ylabel('Residuos')
        
        # Gráfico Q-Q (Normalidad de los residuos)
        ax2 = fig.add_subplot(gs[1, 0])
        sm.qqplot(self.resultados.resid, line='s', ax=ax2, markerfacecolor='skyblue', markeredgecolor='steelblue')
        ax2.set_title('Gráfico Q-Q de los Residuos', fontsize=12)
        
        fig.tight_layout(pad=3.0)
        return fig

    def _generar_grafico_dispersion(self):
        """Genera un gráfico de dispersión de la variable dependiente vs una independiente."""
        # Se grafica solo la primera variable independiente por simplicidad
        fig = plt.figure(figsize=(6, 5))
        sns.regplot(x=self.data[self.independientes[0]], y=self.data[self.dependiente], ci=None,
                    scatter_kws={'alpha': 0.6}, line_kws={'color': 'red'})
        plt.title(f'Dispersión: {self.dependiente} vs. {self.independientes[0]}')
        plt.xlabel(self.independientes[0])
        plt.ylabel(self.dependiente)
        plt.tight_layout()
        return fig

    def _generar_ecuacion(self):
        """Genera la ecuación de la recta de regresión."""
        ecuacion = f"🧾 ECUACIÓN DE PRONÓSTICO\n" + "="*40 + "\n\n"
        ecuacion += f"{self.dependiente} = {self.resultados.params['const']:.4f}"
        for var in self.independientes:
            coef = self.resultados.params[var]
            signo = "+" if coef >= 0 else "-"
            ecuacion += f" {signo} {abs(coef):.4f} * ({var})"
        return ecuacion

# --- Clase de la Interfaz Gráfica ---

class InterfazEstadistica:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Estadístico de Regresión Múltiple")
        self.analizador = AnalizadorEstadistico()
        self.canvas_supuestos = None
        self.canvas_dispersion = None

        # --- Estilos ---
        self.root.configure(bg='#202833')
        style = ttk.Style(self.root)
        style.theme_use('clam')
        # Configuración del Notebook (pestañas)
        style.configure("TNotebook", background='#202833', borderwidth=0)
        style.configure("TNotebook.Tab", background="#2c3e50", foreground="white", padding=[10, 5], font=('Segoe UI', 10))
        style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        # Configuración de otros widgets
        style.configure("TFrame", background='#202833')
        style.configure("TLabel", background='#202833', foreground='white', font=('Segoe UI', 10))
        style.configure("TButton", background='#3498db', foreground='white', font=('Segoe UI', 10, 'bold'))
        style.map("TButton", background=[('active', '#2980b9')])
        style.configure("TEntry", fieldbackground="#2c3e50", foreground="white", insertbackground="white")
        
        self.crear_interfaz()

    def crear_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- Pestañas ---
        tabs = {
            "instrucciones": "📝 Instrucciones", "teoria": "📚 Teoría",
            "formulario": "📂 Análisis", "resultado": "📊 Resultados",
            "supuestos": "🔍 Supuestos", "dispersion": "📈 Dispersión",
            "ecuacion": "🧮 Ecuación"
        }
        self.tab_frames = {}
        for key, text in tabs.items():
            frame = ttk.Frame(self.notebook, padding=10)
            self.tab_frames[key] = frame
            self.notebook.add(frame, text=text)

        # Contenido de cada pestaña
        self._crear_tab_instrucciones()
        self._crear_tab_teoria()
        self._crear_tab_formulario()
        self._crear_tab_resultados()
        
        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#34495e', fg='white')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _crear_tab_instrucciones(self):
        texto = ("Bienvenido al Analizador de Regresión Múltiple.\n\n"
                 "Este software replica salidas de análisis estadístico para modelos de regresión.\n\n"
                 "▶ Paso 1: En la pestaña 'Análisis', selecciona un archivo .csv o .xlsx.\n"
                 "▶ Paso 2: Elige la variable dependiente y las independientes de los menús.\n"
                 "▶ Paso 3: Haz clic en 'Ejecutar Análisis' y explora los resultados en las pestañas.\n\n"
                 "Asegúrate de que tu archivo de datos no tenga celdas vacías en las variables de interés.")
        label = ttk.Label(self.tab_frames["instrucciones"], text=texto, justify='left', font=('Segoe UI', 11))
        label.pack(padx=10, pady=10, anchor='w')

    def _crear_tab_teoria(self):
        texto = ("Regresión Lineal Múltiple\n\n"
                 "Modela la relación entre una variable dependiente y varias independientes.\n\n"
                 "Supuestos Clave:\n"
                 "1. Linealidad: La relación entre X e Y es lineal.\n"
                 "2. Normalidad de los errores: Los residuos siguen una distribución normal.\n"
                 "3. Homocedasticidad: La varianza de los residuos es constante.\n"
                 "4. No Autocorrelación: Los residuos son independientes entre sí.\n"
                 "5. No Multicolinealidad: Las variables independientes no están altamente correlacionadas entre sí.\n\n"
                 "El incumplimiento de estos supuestos puede invalidar el modelo.")
        label = ttk.Label(self.tab_frames["teoria"], text=texto, justify='left', font=('Segoe UI', 11))
        label.pack(padx=10, pady=10, anchor='w')
    
    def _crear_tab_formulario(self):
        frame = self.tab_frames["formulario"]
        
        ttk.Label(frame, text="Archivo de datos:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_archivo = ttk.Entry(frame, width=60)
        self.entry_archivo.grid(row=0, column=1, padx=5)
        self.btn_buscar = ttk.Button(frame, text="Buscar Archivo", command=self.seleccionar_archivo)
        self.btn_buscar.grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="Variable Dependiente (Y):").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.combo_dependiente = ttk.Combobox(frame, width=30, state='readonly')
        self.combo_dependiente.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(frame, text="Variables Independientes (X):").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.listbox_independientes = tk.Listbox(frame, selectmode='multiple', height=5, width=32, exportselection=False, bg="#2c3e50", fg="white")
        self.listbox_independientes.grid(row=2, column=1, padx=5, sticky='w')

        self.btn_ejecutar = ttk.Button(frame, text="Ejecutar Análisis", command=self.iniciar_analisis)
        self.btn_ejecutar.grid(row=3, column=1, pady=20)
    
    def _crear_tab_resultados(self):
        # Crear contenedores para cada pestaña de resultados
        self.text_resultado = tk.Text(self.tab_frames["resultado"], bg='#0f1117', fg='white', font=('Consolas', 10), wrap='word')
        self.text_resultado.pack(fill='both', expand=True)

        self.text_supuestos = tk.Text(self.tab_frames["supuestos"], bg='#0f1117', fg='white', font=('Consolas', 10), height=15, wrap='word')
        self.text_supuestos.pack(fill='x', side='bottom')
        self.frame_grafico_supuestos = ttk.Frame(self.tab_frames["supuestos"])
        self.frame_grafico_supuestos.pack(fill='both', expand=True)
        
        self.frame_grafico_dispersion = ttk.Frame(self.tab_frames["dispersion"])
        self.frame_grafico_dispersion.pack(fill='both', expand=True)
        
        self.text_ecuacion = tk.Text(self.tab_frames["ecuacion"], bg='#0f1117', fg='white', font=('Consolas', 14, 'bold'), wrap='word')
        self.text_ecuacion.pack(fill='both', expand=True)
        
    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Datos", "*.xlsx *.xls *.csv")])
        if not archivo:
            return
        
        self.entry_archivo.delete(0, tk.END)
        self.entry_archivo.insert(0, archivo)
        
        # Cargar columnas en los widgets de selección
        try:
            if archivo.endswith('.csv'):
                df = pd.read_csv(archivo, nrows=1)
            else:
                df = pd.read_excel(archivo, nrows=1)
            
            columnas = df.columns.tolist()
            self.combo_dependiente['values'] = columnas
            self.listbox_independientes.delete(0, tk.END)
            for col in columnas:
                self.listbox_independientes.insert(tk.END, col)
            self.status_bar.config(text=f"Archivo cargado: {archivo.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Error al leer archivo", f"No se pudieron leer las columnas.\nError: {e}")
            
    def iniciar_analisis(self):
        archivo = self.entry_archivo.get()
        dependiente = self.combo_dependiente.get()
        indices_seleccionados = self.listbox_independientes.curselection()
        independientes = [self.listbox_independientes.get(i) for i in indices_seleccionados]

        if not (archivo and dependiente and independientes):
            messagebox.showwarning("Campos incompletos", "Por favor, selecciona un archivo, una variable dependiente y al menos una independiente.")
            return
        
        if dependiente in independientes:
            messagebox.showwarning("Selección inválida", "La variable dependiente no puede ser también una variable independiente.")
            return

        # Deshabilitar botón y mostrar estado
        self.btn_ejecutar.config(state='disabled', text="Analizando...")
        self.status_bar.config(text="Ejecutando análisis... por favor espera.")
        self.limpiar_resultados_anteriores()

        # Iniciar el análisis en un hilo separado para no bloquear la GUI
        thread = threading.Thread(target=self.proceso_de_analisis, args=(archivo, dependiente, independientes))
        thread.start()

    def proceso_de_analisis(self, archivo, dependiente, independientes):
        """Función que se ejecuta en un hilo separado."""
        try:
            self.analizador.cargar_datos(archivo, dependiente, independientes)
            resultados = self.analizador.realizar_analisis_completo()
            # Enviar los resultados al hilo principal para actualizar la GUI
            self.root.after(0, self.actualizar_gui_con_resultados, resultados)
        except Exception as e:
            self.root.after(0, self.mostrar_error, str(e))

    def actualizar_gui_con_resultados(self, resultados):
        """Actualiza la GUI con los resultados. Se ejecuta en el hilo principal."""
        # Poblar pestañas de texto
        self.text_resultado.insert(tk.END, resultados["resumen_spss"])
        self.text_supuestos.insert(tk.END, resultados["supuestos_texto"])
        self.text_ecuacion.insert(tk.END, resultados["ecuacion"])

        # Mostrar gráficos
        self._mostrar_grafico(self.frame_grafico_supuestos, resultados["supuestos_graficos"], "canvas_supuestos")
        self._mostrar_grafico(self.frame_grafico_dispersion, resultados["grafico_dispersion"], "canvas_dispersion")
        
        self.status_bar.config(text="Análisis completado exitosamente.")
        self.btn_ejecutar.config(state='normal', text="Ejecutar Análisis")
        self.notebook.select(self.tab_frames["resultado"]) # Ir a la pestaña de resultados

    def _mostrar_grafico(self, frame_destino, fig, canvas_attr_name):
        """Función auxiliar para dibujar un gráfico de matplotlib en un frame de tkinter."""
        # Limpiar canvas anterior si existe
        canvas_anterior = getattr(self, canvas_attr_name)
        if canvas_anterior:
            canvas_anterior.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_destino)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        setattr(self, canvas_attr_name, canvas)

    def limpiar_resultados_anteriores(self):
        self.text_resultado.delete(1.0, tk.END)
        self.text_supuestos.delete(1.0, tk.END)
        self.text_ecuacion.delete(1.0, tk.END)
        if self.canvas_supuestos:
            self.canvas_supuestos.get_tk_widget().destroy()
            self.canvas_supuestos = None
        if self.canvas_dispersion:
            self.canvas_dispersion.get_tk_widget().destroy()
            self.canvas_dispersion = None

    def mostrar_error(self, error_msg):
        """Muestra un error y restaura el estado de la GUI."""
        messagebox.showerror("Error en el Análisis", error_msg)
        self.btn_ejecutar.config(state='normal', text="Ejecutar Análisis")
        self.status_bar.config(text="Error. Listo para un nuevo análisis.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    app = InterfazEstadistica(root)
    root.mainloop()