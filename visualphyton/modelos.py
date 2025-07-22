import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import matplotlib.pyplot as plt # Still needed for qqplot workaround
import seaborn as sns # Not directly used in plotting, but often part of data science env
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import threading
import os
import webbrowser
from PIL import Image, ImageTk, ImageDraw # Import ImageDraw
import tkinter.font as tkFont

# For PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

# =============================================================================
# ANALYTICAL LOGIC (BACKEND)
# =============================================================================

class AnalizadorExploratorio:
    """Performs basic descriptive and exploratory analysis."""
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Se requiere un DataFrame de pandas.")
        self.df = df.copy() # Work with a copy to avoid modifying original
        self.numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        # Ensure 'object' and 'category' dtypes are explicitly included for categorical
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()

    def get_resumen_descriptivo(self):
        if not self.numeric_cols:
            return "No hay columnas numéricas para un resumen descriptivo.", pd.DataFrame()
        desc = self.df[self.numeric_cols].describe().T
        return f"📊 Estadísticas Descriptivas (Numéricas):\n\n{desc.to_string()}", desc

    def get_distribucion_frecuencias(self, var):
        if var not in self.df.columns:
            return "Variable no encontrada.", pd.DataFrame()
        
        # Check if truly categorical or if it's numeric with few unique values (might be treated as categorical)
        if self.df[var].dtype in ['object', 'category'] or self.df[var].nunique() < 20: # Heuristic for pseudo-categorical
            freq_table = self.df[var].value_counts().to_frame(name='Frecuencia')
            freq_table['Porcentaje (%)'] = (self.df[var].value_counts(normalize=True) * 100).round(2)
            return f"📊 Distribución de Frecuencias para '{var}':\n\n{freq_table.to_string()}", freq_table
        else: # Numeric variable, might want to show quantiles or bins
            # Use fixed number of bins or Freedman-Diaconis rule
            bins = pd.cut(self.df[var], bins='auto', include_lowest=True, right=True) # 'auto' for better binning
            freq_table = bins.value_counts().sort_index().to_frame(name='Frecuencia')
            freq_table['Porcentaje (%)'] = (bins.value_counts(normalize=True) * 100).round(2)
            freq_table.index = freq_table.index.astype(str) # Convert IntervalIndex to string for display
            return f"📊 Distribución Binned para '{var}' (bins automáticos):\n\n{freq_table.to_string()}", freq_table


    def plot_correlacion(self):
        if not self.numeric_cols:
            return None, "No hay columnas numéricas para calcular la correlación."
        corr_matrix = self.df[self.numeric_cols].corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                        color_continuous_scale='RdYlBu',
                        title="Mapa de Calor de Correlación Interactivo")
        fig.update_layout(template="plotly_dark", title_x=0.5, font=dict(color="white", size=12)) # Consistent font
        return fig, f"Matriz de Correlación:\n\n{corr_matrix.to_string()}"

    def plot_distribucion(self, var):
        if var not in self.df.columns:
            return None, "Variable no encontrada."
        
        # Use more descriptive titles
        if self.df[var].dtype in np.number:
            fig = px.histogram(self.df, x=var, marginal="box",
                               title=f"Distribución y Boxplot de '{var}'",
                               color_discrete_sequence=['#45a29e'])
        else: # Categorical or object type
            counts = self.df[var].value_counts().reset_index()
            counts.columns = ['Category', 'Count'] # Renaming for clarity
            fig = px.bar(counts, x='Category', y='Count',
                         title=f"Distribución de Frecuencias de '{var}'",
                         color_discrete_sequence=['#45a29e'])
        
        fig.update_layout(template="plotly_dark", title_x=0.5, font=dict(color="white", size=12))
        return fig, f"Gráfico de Distribución para '{var}' generado."


class AnalizadorRegresion:
    """Performs a complete multiple linear regression analysis."""
    def __init__(self, df):
        self.df = df.copy() # Work with a copy
        self.modelo = None
        self.resultados = None

    def ejecutar_regresion(self, y_var, x_vars):
        if not all(col in self.df.columns for col in [y_var] + x_vars):
            raise ValueError("Una o más variables seleccionadas no existen en el DataFrame.")
        if self.df[[y_var] + x_vars].isnull().any().any():
            messagebox.showwarning("Datos Faltantes", "Se detectaron valores faltantes en las variables seleccionadas. Las filas con valores nulos serán omitidas para el análisis de regresión.")
            df_cleaned = self.df[[y_var] + x_vars].dropna()
            if df_cleaned.empty:
                raise ValueError("No quedan datos válidos después de eliminar filas con valores faltantes.")
        else:
            df_cleaned = self.df[[y_var] + x_vars]

        y = df_cleaned[y_var]
        X = df_cleaned[x_vars]
        
        # Check for non-numeric types in X before adding constant
        if not X.select_dtypes(include=np.number).columns.tolist() == X.columns.tolist():
             raise ValueError("Las variables independientes deben ser numéricas.")

        X = sm.add_constant(X) # Ensure 'const' is added only once
        
        self.modelo = sm.OLS(y, X).fit()
        self.resultados = self.modelo
        
        spss_summary = str(self.resultados.summary())
        
        r_squared = self.resultados.rsquared
        adj_r_squared = self.resultados.rsquared_adj
        f_statistic = self.resultados.fvalue
        f_pvalue = self.resultados.f_pvalue

        model_summary_intro = (
            f"--- Resumen del Modelo ---\n"
            f"R-cuadrado: {r_squared:.4f}\n"
            f"R-cuadrado Ajustado: {adj_r_squared:.4f}\n"
            f"Estadístico F: {f_statistic:.2f}\n"
            f"Prob (F-estadístico): {f_pvalue:.4f}\n\n"
        )
        
        texto_supuestos = self._generar_texto_supuestos()
        ecuacion = self._generar_ecuacion(y_var, x_vars)
        
        full_text_report = (
            f"{model_summary_intro}"
            f"--- Detalles Completos del Modelo (SPSS-like) ---\n{spss_summary}\n\n"
            f"--- Verificación de Supuestos ---\n{texto_supuestos}\n\n"
            f"--- Ecuación de Regresión ---\n{ecuacion}"
        )
        
        return full_text_report, self.resultados # Return results object for coefficient table

    def plot_diagnosticos_regresion(self):
        if self.resultados is None:
            return None
        
        fitted_vals = self.resultados.fittedvalues
        residuals = self.resultados.resid
        
        fig = make_subplots(rows=2, cols=2, 
                            subplot_titles=("Residuos vs. Valores Ajustados", "Gráfico Q-Q de Residuos",
                                            "Histograma de Residuos", "Residuos vs. Orden de Observación"),
                            specs=[[{}, {}],
                                   [{}, {}]])

        # 1. Residuos vs. Valores Ajustados
        fig.add_trace(go.Scatter(x=fitted_vals, y=residuals, mode='markers', 
                                 marker=dict(color='#17a2b8', opacity=0.7), name='Residuos'), row=1, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1) # Add a zero line
        fig.update_xaxes(title_text="Valores Ajustados", row=1, col=1)
        fig.update_yaxes(title_text="Residuos", row=1, col=1)

        # 2. Gráfico Q-Q
        qq_data = sm.ProbPlot(residuals).qqplot(ax=None, line='s')
        qq_x = qq_data.get_axes()[0].get_lines()[0].get_xdata()
        qq_y = qq_data.get_axes()[0].get_lines()[0].get_ydata()
        line_x = qq_data.get_axes()[0].get_lines()[1].get_xdata()
        line_y = qq_data.get_axes()[0].get_lines()[1].get_ydata()
        plt.close(qq_data) # Close matplotlib figure to prevent memory issues
        
        fig.add_trace(go.Scatter(x=qq_x, y=qq_y, mode='markers', marker=dict(color='#ffc107'), name='Cuantiles'), row=1, col=2)
        fig.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='#dc3545'), name='Línea teórica'), row=1, col=2)
        fig.update_xaxes(title_text="Cuantiles Teóricos", row=1, col=2)
        fig.update_yaxes(title_text="Cuantiles Muestrales", row=1, col=2)

        # 3. Histograma de Residuos
        hist_trace = px.histogram(x=residuals, color_discrete_sequence=['#45a29e'], nbins=30).data[0] # Add nbins
        fig.add_trace(hist_trace, row=2, col=1)
        fig.update_xaxes(title_text="Residuos", row=2, col=1)
        fig.update_yaxes(title_text="Frecuencia", row=2, col=1)

        # 4. Residuos vs. Orden de Observación (for visual autocorrelation detection)
        fig.add_trace(go.Scatter(y=residuals, mode='lines+markers', 
                                 marker=dict(color='#66fcf1', opacity=0.7, size=4), name='Residuos por Orden'), row=2, col=2)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=2)
        fig.update_xaxes(title_text="Orden de Observación", row=2, col=2)
        fig.update_yaxes(title_text="Residuos", row=2, col=2)

        fig.update_layout(height=800, width=1000, showlegend=False, template="plotly_dark", title_x=0.5, font=dict(color="white", size=12))
        return fig

    def _generar_texto_supuestos(self):
        x_vars = self.resultados.model.exog
        exog_names = self.resultados.model.exog_names
        
        vif_data = pd.DataFrame()
        vif_data["Variable"] = [name for name in exog_names if name != 'const']
        vif_values = []
        # Calculate VIF only for independent variables
        for i, name in enumerate(exog_names):
            if name != 'const':
                # Ensure the column is numeric for VIF calculation
                if self.df[name].dtype in np.number:
                    vif_values.append(variance_inflation_factor(x_vars, i))
                else:
                    vif_values.append(np.nan) # Handle non-numeric if somehow passed
        vif_data["VIF"] = vif_values
        
        # Normality test
        try:
            shapiro = stats.shapiro(self.resultados.resid)
            shapiro_text = f"Estadístico: {shapiro.statistic:.4f}, p-valor: {shapiro.pvalue:.4f}\n(p > 0.05 sugiere normalidad. Considerar muestra grande: K-S test o visualización Q-Q)"
        except Exception as e:
            shapiro_text = f"Error al calcular Shapiro-Wilk: {e} (posiblemente pocos datos o residuos constantes)."

        # Homoscedasticity test
        try:
            bp_test = sm.stats.het_breuschpagan(self.resultados.resid, self.resultados.model.exog)
            bp_text = f"Estadístico: {bp_test[0]:.4f}, p-valor: {bp_test[1]:.4f}\n(p > 0.05 sugiere homocedasticidad)"
        except Exception as e:
            bp_text = f"Error al calcular Breusch-Pagan: {e} (posiblemente pocos datos o problemas de rango)."

        # Autocorrelation test
        dw_test = sm.stats.durbin_watson(self.resultados.resid)

        reporte = (
            f"--- No Multicolinealidad (VIF) ---\n"
            f"(Valores > 5-10 sugieren posible problema)\n{vif_data.to_string(index=False)}\n\n"
            f"--- Normalidad de Residuos (Shapiro-Wilk) ---\n"
            f"{shapiro_text}\n\n"
            f"--- Homocedasticidad (Breusch-Pagan) ---\n"
            f"{bp_text}\n\n"
            f"--- No Autocorrelación (Durbin-Watson) ---\n"
            f"Estadístico: {dw_test:.4f}\n(Valores cercanos a 2 son ideales, 0 indica positiva, 4 negativa)\n"
        )
        return reporte

    def _generar_ecuacion(self, y_var, x_vars):
        # Using correct LaTeX for coefficients and variables
        equation_parts = [f"$\\mathbf{{{y_var}}} = {self.resultados.params['const']:.4f}"]
        for var in x_vars:
            coef = self.resultados.params[var]
            sign = "+" if coef >= 0 else "-"
            # Use \\cdot for multiplication, and \\mathbf for bold variables in LaTeX
            equation_parts.append(f" {sign} {abs(coef):.4f} \\cdot \\mathbf{{{var}}}")
        return "".join(equation_parts) + "$"


class AnalizadorSeriesTiempo:
    """Performs time series forecasting using ARIMA."""
    def __init__(self, df):
        self.df = df.copy() # Work with a copy
        self.model_fit = None

    def ejecutar_arima(self, time_var, target_var, order=(5,1,0), steps=10):
        if time_var not in self.df.columns or target_var not in self.df.columns:
            raise ValueError("Las columnas de tiempo o objetivo no existen en el DataFrame.")
        if not pd.api.types.is_numeric_dtype(self.df[target_var]):
            raise ValueError(f"La columna objetivo '{target_var}' debe ser numérica.")

        # Ensure time_var is datetime indexed for time series
        try:
            # Attempt to convert to datetime and handle potential errors
            self.df[time_var] = pd.to_datetime(self.df[time_var], errors='coerce')
            df_ts = self.df.dropna(subset=[time_var, target_var]) # Drop rows where time or target is null after conversion
            if df_ts.empty:
                raise ValueError("No quedan datos válidos de serie de tiempo después de limpiar valores nulos o fechas inválidas.")
            df_ts = df_ts.set_index(time_var).sort_index()
            ts_data = df_ts[target_var]
        except Exception as e:
            raise ValueError(f"Error al preparar la serie de tiempo: {e}. Asegúrese que '{time_var}' es una columna de fecha/hora válida y que no contiene valores nulos no convertibles.")

        # Handle potential duplicate index entries (ARIMA requires unique index)
        if not ts_data.index.is_unique:
            messagebox.showwarning("Índice Duplicado", "Se detectaron valores de tiempo duplicados. Se sumarán los valores para las fechas duplicadas. Considere preprocesar sus datos si este comportamiento no es deseado.")
            ts_data = ts_data.groupby(ts_data.index).sum() # Example: sum values for duplicate timestamps

        # Infer frequency if not already set, crucial for statsmodels
        # if pd.infer_freq(ts_data.index) is None:
        #     messagebox.showwarning("Frecuencia no inferida", "La frecuencia de la serie de tiempo no pudo ser inferida automáticamente. Esto puede afectar la precisión del modelo ARIMA.")

        try:
            model = sm.tsa.ARIMA(ts_data, order=order)
            self.model_fit = model.fit()
        except Exception as e:
            raise ValueError(f"Error al ajustar el modelo ARIMA: {e}. Verifique el orden (p,d,q) y la estacionalidad de la serie.")

        forecast_results = self.model_fit.forecast(steps=steps)
        
        # Create a DataFrame for the forecast
        last_date = ts_data.index[-1]
        
        # Generate future dates based on inferred frequency
        # If infer_freq fails, fall back to a simple daily or hourly increment if the original data is consistent.
        inferred_freq = pd.infer_freq(ts_data.index)
        if inferred_freq:
            forecast_index = pd.date_range(start=last_date, periods=steps + 1, freq=inferred_freq)[1:]
        else:
            # Fallback for when frequency can't be inferred (e.g., irregular data, very short series)
            # This is a heuristic, better to ensure regular time series data.
            # Assuming daily if dates are distinct, or hourly if timestamps are distinct.
            if len(ts_data.index) > 1:
                time_diff = ts_data.index.to_series().diff().dropna().mode()[0]
                if time_diff == pd.Timedelta(days=1):
                    forecast_index = pd.date_range(start=last_date, periods=steps + 1, freq='D')[1:]
                elif time_diff == pd.Timedelta(hours=1):
                    forecast_index = pd.date_range(start=last_date, periods=steps + 1, freq='H')[1:]
                else:
                    messagebox.showwarning("Frecuencia no inferida", "La frecuencia de la serie de tiempo no pudo ser inferida automáticamente. El pronóstico se basará en un incremento simple desde la última fecha, lo cual puede no ser preciso.")
                    forecast_index = [last_date + (i * time_diff) for i in range(1, steps + 1)]
            else:
                raise ValueError("No hay suficientes puntos de datos para inferir la frecuencia y generar el pronóstico. Necesita al menos dos puntos de tiempo para inferir una frecuencia.")


        forecast_df = pd.DataFrame({'Fecha': forecast_index, 'Pronóstico': forecast_results}).set_index('Fecha')

        report = (
            f"--- Resumen del Modelo ARIMA (p={order[0]}, d={order[1]}, q={order[2]})---\n"
            f"{self.model_fit.summary().as_text()}\n\n"
            f"--- Pronóstico para los Próximos {steps} Pasos ---\n"
            f"{forecast_df.to_string()}"
        )
        return report, ts_data, forecast_df

    def plot_arima_forecast(self, ts_data, forecast_df, title="Pronóstico ARIMA"):
        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(x=ts_data.index, y=ts_data.values, mode='lines', name='Histórico', line=dict(color='#45a29e')))

        # Forecasted data
        fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['Pronóstico'], mode='lines', name='Pronóstico', line=dict(color='#ffc107', dash='dash')))

        # Add shaded area for confidence intervals if available (ARIMA results usually have them)
        try:
            if hasattr(self.model_fit, 'conf_int'):
                # Get confidence intervals from the forecast method or manually from model_fit.get_forecast
                forecast_ci = self.model_fit.get_forecast(steps=len(forecast_df)).conf_int()
                
                fig.add_trace(go.Scatter(
                    x=forecast_df.index.tolist() + forecast_df.index.tolist()[::-1], # x, then x reversed
                    y=forecast_ci.iloc[:, 0].tolist() + forecast_ci.iloc[:, 1].tolist()[::-1], # lower, then upper reversed
                    fill='toself',
                    fillcolor='rgba(255,193,7,0.2)', # Semi-transparent yellow
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Intervalo de Confianza 95%',
                    showlegend=True
                ))
        except Exception as e:
            print(f"No se pudo añadir el intervalo de confianza: {e}")
            pass # Silently fail if CI cannot be generated/added

        fig.update_layout(
            title_text=title,
            xaxis_title="Fecha",
            yaxis_title="Valor",
            template="plotly_dark",
            title_x=0.5,
            font=dict(color="white", size=12),
            hovermode="x unified"
        )
        return fig

# =============================================================================
# CUSTOM WIDGETS
# =============================================================================

class AnimatedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, width=200, height=40, bg_color="#2c3e50", hover_color="#34495e", text_color="white", icon=None):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.icon = icon

        self.rect = self.create_rectangle(0, 0, width, height, fill=bg_color, outline="")
        
        text_x = 10
        if self.icon:
            # Place the icon on the canvas
            self.create_image(25, height // 2, image=self.icon, anchor="center")
            text_x = 45 # Adjust text position if icon is present

        self.text_id = self.create_text(text_x, height // 2, text=text, fill=text_color, font=("Segoe UI", 10, "bold"), anchor="w")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, e): self.itemconfig(self.rect, fill=self.hover_color)
    def on_leave(self, e): self.itemconfig(self.rect, fill=self.bg_color)
    def on_click(self, e):
        if self.command: self.command()

# =============================================================================
# MAIN APPLICATION CLASS (FRONTEND)
# =============================================================================

class DataSuiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Suite de Análisis de Datos Integrada")
        self.geometry("1400x800")
        self.configure(bg="#1f2833")

        self.data = None
        self.current_plot = None # Store plotly figure for export
        self.current_text_result = "" # Store text for export
        self.current_data_table = None # Store data frame for PDF table export (e.g., descriptive stats, freq tables)

        # --- Custom Fonts ---
        self.heading1_font = tkFont.Font(family="Segoe UI", size=28, weight="bold")
        self.heading2_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.subheading_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        self.label_font = tkFont.Font(family="Segoe UI", size=10)
        self.button_font = tkFont.Font(family="Segoe UI", size=10, weight="bold")
        self.monospace_font = tkFont.Font(family="Consolas", size=10)
    
        # --- Create icons in memory ---
        self.icons = self._create_icons()

        self._create_widgets()
        self._show_welcome_view()
    

    def _create_icons(self):
        """Creates basic icons with Pillow for in-memory use."""
        icons = {}
        icon_size = 20

        # Define shapes using Pillow's ImageDraw
        def draw_dashed_line(draw, xy, dash_length=4, space_length=2, fill="white", width=2):
            x1, y1, x2, y2 = xy
            dx = x2 - x1
            dy = y2 - y1
            dist = (dx**2 + dy**2)**0.5
            if dist == 0:
                return
            steps = int(dist / (dash_length + space_length))
            for i in range(steps):
                start = i * (dash_length + space_length)
                end = start + dash_length
                if end > dist:
                    end = dist
                start_x = x1 + (dx * start / dist)
                start_y = y1 + (dy * start / dist)
                end_x = x1 + (dx * end / dist)
                end_y = y1 + (dy * end / dist)
                draw.line((start_x, start_y, end_x, end_y), fill=fill, width=width)

        def draw_upload(draw):
            draw.line((icon_size//2, 2, icon_size//2, icon_size-5), fill="white", width=2) # Arrow shaft
            draw.polygon([(icon_size//2, 2), (icon_size//2 - 5, 7), (icon_size//2 + 5, 7)], fill="white") # Arrow head
            draw.line((2, icon_size-3, icon_size-2, icon_size-3), fill="white", width=2) # Base line

        def draw_explore(draw):
            draw.rectangle((2,2,8,8), outline="white", width=2)
            draw.rectangle((12,2,18,8), outline="white", width=2)
            draw.rectangle((2,12,8,18), outline="white", width=2)
            draw.rectangle((12,12,18,18), outline="white", width=2)

        def draw_regression(draw):
            draw.line((2, 18, 8, 12), fill="white", width=2)
            draw.line((8, 12, 14, 16), fill="white", width=2)
            draw.line((14, 16, 18, 4), fill="white", width=2)
            draw.ellipse((1.5, 17.5, 4.5, 20.5), fill="white", outline="white")
            draw.ellipse((7.5, 11.5, 10.5, 14.5), fill="white", outline="white")
            draw.ellipse((13.5, 15.5, 16.5, 18.5), fill="white", outline="white")
            draw.ellipse((17.5, 3.5, 20.5, 6.5), fill="white", outline="white")

        def draw_forecast(draw):
            # Línea hasta el último punto conocido
            draw.line((2, 18, 8, 12), fill="white", width=2)
            draw.line((8, 12, 14, 16), fill="white", width=2)

    # Línea discontinua para la predicción (dibujada manualmente)
            draw_dashed_line(draw, (14, 16, 18, 10), dash_length=4, space_length=2, fill="white", width=2)

    # Puntos de datos (algunos históricos, algunos pronosticados)
            draw.ellipse((1.5, 17.5, 4.5, 20.5), fill="white", outline="white")
            draw.ellipse((7.5, 11.5, 10.5, 14.5), fill="white", outline="white")
            draw.ellipse((13.5, 15.5, 16.5, 18.5), fill="white", outline="white") # último punto real
            draw.ellipse((17.5, 9.5, 20.5, 12.5), fill="white", outline="white")  # punto predicho



        def draw_export_text(draw):
            draw.line((4,4,16,4), fill="white", width=2)
            draw.line((4,9,16,9), fill="white", width=2)
            draw.line((4,14,12,14), fill="white", width=2)
            draw.line((4,18,14,18), fill="white", width=2)

        def draw_export_plot(draw):
            draw.line((2,18,18,18), fill="white", width=2) # Eje X
            draw.line((2,18,2,6), fill="white", width=2)   # Eje Y

            # Barras corregidas (de arriba a abajo)
            draw.rectangle((4, 10, 7, 18), fill="#45a29e", outline="#45a29e")
            draw.rectangle((9, 6, 12, 18), fill="#45a29e", outline="#45a29e")
            draw.rectangle((14, 14, 17, 18), fill="#45a29e", outline="#45a29e")


        icon_map = {
            "upload": draw_upload,
            "explore": draw_explore,
            "regression": draw_regression,
            "forecast": draw_forecast,
            "export_text": draw_export_text,
            "export_plot": draw_export_plot
        }

        for name, draw_func in icon_map.items():
            img = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw_func(draw)
            icons[name] = ImageTk.PhotoImage(img)
        return icons

    def _create_widgets(self):
        # --- Main Layout ---
        self.main_frame = tk.Frame(self, bg="#1f2833")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Navigation Sidebar
        self.sidebar = tk.Frame(self.main_frame, bg="#2c3e50", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="DATA SUITE", font=self.heading2_font, fg="#66fcf1", bg="#2c3e50").pack(pady=20)
        
        AnimatedButton(self.sidebar, text="Cargar Datos", command=self.load_csv, icon=self.icons["upload"]).pack(pady=5, padx=10)
        tk.Frame(self.sidebar, height=2, bg="#45a29e").pack(fill=tk.X, padx=20, pady=15)

        AnimatedButton(self.sidebar, text="Análisis Exploratorio", command=lambda: self.show_view("exploratory"), icon=self.icons["explore"]).pack(pady=5, padx=10)
        AnimatedButton(self.sidebar, text="Análisis de Regresión", command=lambda: self.show_view("regression"), icon=self.icons["regression"]).pack(pady=5, padx=10)
        AnimatedButton(self.sidebar, text="Análisis de Series de Tiempo", command=lambda: self.show_view("time_series"), icon=self.icons["forecast"]).pack(pady=5, padx=10)

        # 2. Content Area
        self.content_area = tk.Frame(self.main_frame, bg="#1f2833")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # --- Content Views (Frames that swap) ---
        self.views = {
            "welcome": self._create_welcome_view(),
            "exploratory": self._create_exploratory_view(),
            "regression": self._create_regression_view(),
            "time_series": self._create_time_series_view()
        }
        self.current_view = None
        self.current_view_name_str = "welcome" # Keep track of the current view name

    def _create_welcome_view(self):
        frame = tk.Frame(self.content_area, bg="#1f2833")
        tk.Label(frame, text="Bienvenido a la Suite de Análisis de Datos", font=self.heading1_font, fg="#66fcf1", bg="#1f2833").pack(pady=(150, 20))
        tk.Label(frame, text="Cargue un archivo CSV para comenzar su análisis.", font=self.subheading_font, fg="white", bg="#1f2833").pack()
        return frame

    def _create_exploratory_view(self):
        frame = tk.Frame(self.content_area, bg="#1f2833")
        
        # Controls Frame
        controls = tk.Frame(frame, bg="#2c3e50")
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(controls, text="Análisis Exploratorio", font=self.subheading_font, fg="white", bg="#2c3e50").pack(pady=10)
        AnimatedButton(controls, text="Resumen Descriptivo", command=lambda: self.run_analysis("desc")).pack(pady=5, padx=5)
        AnimatedButton(controls, text="Mapa de Correlación", command=lambda: self.run_analysis("corr")).pack(pady=5, padx=5)
        
        tk.Label(controls, text="Distribución de Variable", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.exp_var_combo = ttk.Combobox(controls, state="readonly", font=self.label_font)
        self.exp_var_combo.pack(pady=5, padx=5)
        AnimatedButton(controls, text="Generar Gráfico", command=lambda: self.run_analysis("dist")).pack(pady=5, padx=5)

        # Results Area
        results_frame = tk.Frame(frame, bg="#1f2833")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._setup_results_area(results_frame)

        return frame

    def _create_regression_view(self):
        frame = tk.Frame(self.content_area, bg="#1f2833")
        
        # Controls Frame
        controls = tk.Frame(frame, bg="#2c3e50")
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(controls, text="Análisis de Regresión", font=self.subheading_font, fg="white", bg="#2c3e50").pack(pady=10)
        
        tk.Label(controls, text="Variable Dependiente (Y):", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.reg_y_combo = ttk.Combobox(controls, state="readonly", font=self.label_font)
        self.reg_y_combo.pack(pady=5, padx=5)

        tk.Label(controls, text="Variables Independientes (X):", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.reg_x_listbox = tk.Listbox(controls, selectmode='multiple', bg="#0b0c10", fg="white", highlightthickness=0, exportselection=False, font=self.monospace_font, relief='flat', height=10)
        self.reg_x_listbox.pack(pady=5, padx=5, fill=tk.Y, expand=True)
        
        # Add scrollbar to listbox
        reg_x_scrollbar = ttk.Scrollbar(controls, orient="vertical", command=self.reg_x_listbox.yview)
        reg_x_scrollbar.pack(side="right", fill="y", in_=self.reg_x_listbox)
        self.reg_x_listbox.config(yscrollcommand=reg_x_scrollbar.set)

        AnimatedButton(controls, text="Ejecutar Regresión", command=lambda: self.run_analysis("regr")).pack(pady=10, padx=5)
        
        # Results Area
        results_frame = tk.Frame(frame, bg="#1f2833")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._setup_results_area(results_frame)

        return frame

    def _create_time_series_view(self):
        frame = tk.Frame(self.content_area, bg="#1f2833")
        
        # Controls Frame
        controls = tk.Frame(frame, bg="#2c3e50")
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(controls, text="Análisis de Series de Tiempo", font=self.subheading_font, fg="white", bg="#2c3e50").pack(pady=10)
        
        tk.Label(controls, text="Columna de Tiempo:", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.ts_time_combo = ttk.Combobox(controls, state="readonly", font=self.label_font)
        self.ts_time_combo.pack(pady=5, padx=5)

        tk.Label(controls, text="Columna de Valor (Target):", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.ts_target_combo = ttk.Combobox(controls, state="readonly", font=self.label_font)
        self.ts_target_combo.pack(pady=5, padx=5)

        tk.Label(controls, text="Orden ARIMA (p,d,q):", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        order_frame = tk.Frame(controls, bg="#2c3e50")
        order_frame.pack(pady=5, padx=5)
        self.p_entry = ttk.Entry(order_frame, width=5, font=self.label_font, justify='center')
        self.p_entry.insert(0, "5")
        self.p_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(order_frame, text=",", fg="white", bg="#2c3e50").pack(side=tk.LEFT)
        self.d_entry = ttk.Entry(order_frame, width=5, font=self.label_font, justify='center')
        self.d_entry.insert(0, "1")
        self.d_entry.pack(side=tk.LEFT, padx=2)
        tk.Label(order_frame, text=",", fg="white", bg="#2c3e50").pack(side=tk.LEFT)
        self.q_entry = ttk.Entry(order_frame, width=5, font=self.label_font, justify='center')
        self.q_entry.insert(0, "0")
        self.q_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(controls, text="Pasos de Pronóstico:", fg="white", bg="#2c3e50", font=self.label_font).pack(pady=(10,0))
        self.forecast_steps_entry = ttk.Entry(controls, width=10, font=self.label_font, justify='center')
        self.forecast_steps_entry.insert(0, "10")
        self.forecast_steps_entry.pack(pady=5, padx=5)

        AnimatedButton(controls, text="Ejecutar ARIMA", command=lambda: self.run_analysis("arima")).pack(pady=10, padx=5)
        
        # Results Area
        results_frame = tk.Frame(frame, bg="#1f2833")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._setup_results_area(results_frame)

        return frame
            
    def _setup_results_area(self, parent_frame):
        # Top frame for buttons and title
        top_frame = tk.Frame(parent_frame, bg="#1f2833")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.result_title = tk.Label(top_frame, text="Resultados del Análisis", font=self.subheading_font, fg="#66fcf1", bg="#1f2833")
        self.result_title.pack(side=tk.LEFT)
        
        # Export buttons
        AnimatedButton(top_frame, text="Exportar Gráfico", command=self.export_plot, width=160, icon=self.icons["export_plot"]).pack(side=tk.RIGHT, padx=5)
        AnimatedButton(top_frame, text="Exportar PDF", command=self.export_pdf, width=200, icon=self.icons["export_text"]).pack(side=tk.RIGHT, padx=5)
        
        # Notebook to show text results and interactive plots
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        
        style.configure("TNotebook", background="#1f2833", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2c3e50", foreground="white", padding=[10, 5], font=self.label_font)
        style.map("TNotebook.Tab", background=[("selected", "#45a29e")], foreground=[("selected", "white")])
        
        notebook = ttk.Notebook(parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_tab = tk.Frame(notebook, bg="#1f2833")
        plot_tab = tk.Frame(notebook, bg="#1f2833")
        
        notebook.add(text_tab, text="📄 Resumen de Texto")
        notebook.add(plot_tab, text="📈 Gráfico Interactivo")
        
        # Store references to be able to access them
        parent_frame.text_widget = scrolledtext.ScrolledText(text_tab, wrap=tk.WORD, bg="#0b0c10", fg="white", font=self.monospace_font, relief='flat', insertbackground='white')
        parent_frame.text_widget.pack(expand=True, fill='both')
        
        parent_frame.plot_widget_frame = tk.Frame(plot_tab, bg="#1f2833")
        parent_frame.plot_widget_frame.pack(expand=True, fill='both')

    def show_view(self, view_name):
        if self.current_view:
            self.current_view.pack_forget()
        
        self.current_view = self.views.get(view_name)
        self.current_view_name_str = view_name # Update the tracker
        if self.current_view:
            self.current_view.pack(fill=tk.BOTH, expand=True)
    
    def _show_welcome_view(self):
        self.show_view("welcome")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")])
        if not file_path:
            return
        try:
            temp_df = pd.read_csv(file_path)
            if temp_df.empty:
                raise ValueError("El archivo CSV está vacío o no contiene datos válidos.")
            self.data = temp_df.copy() # Store a copy of the loaded data
            self._populate_variable_selectors()
            messagebox.showinfo("Éxito", f"Archivo '{os.path.basename(file_path)}' cargado correctamente. Puedes iniciar el análisis.")
            self.show_view("exploratory") # Move to exploratory view after data load
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo: {e}\nAsegúrese de que es un CSV válido y no está corrupto.")

    def _populate_variable_selectors(self):
        if self.data is None: return
        numeric_cols = self.data.select_dtypes(include=np.number).columns.tolist()
        all_cols = self.data.columns.tolist()
        datetime_cols = self._get_datetime_cols(self.data)

        # Exploratory selector
        self.exp_var_combo['values'] = all_cols
        if all_cols: self.exp_var_combo.set(all_cols[0])
        else: self.exp_var_combo.set("") # Clear if no columns

        # Regression selectors
        self.reg_y_combo['values'] = numeric_cols
        if numeric_cols: self.reg_y_combo.set(numeric_cols[0])
        else: self.reg_y_combo.set("")

        self.reg_x_listbox.delete(0, tk.END)
        for col in numeric_cols:
            self.reg_x_listbox.insert(tk.END, col)
        
        # Time Series selectors
        self.ts_time_combo['values'] = datetime_cols
        if datetime_cols: self.ts_time_combo.set(datetime_cols[0])
        else: self.ts_time_combo.set("")

        self.ts_target_combo['values'] = numeric_cols
        if numeric_cols: self.ts_target_combo.set(numeric_cols[0])
        else: self.ts_target_combo.set("")

    def _get_datetime_cols(self, df):
        """Identifies columns that can be converted to datetime."""
        datetime_cols = []
        for col in df.columns:
            # Check for non-null values before trying conversion
            if not df[col].dropna().empty:
                try:
                    # Attempt conversion on a small sample to be efficient
                    # If conversion is successful for all, it's a candidate
                    if pd.to_datetime(df[col].dropna(), errors='coerce').notna().all():
                        datetime_cols.append(col)
                except Exception:
                    continue
        return datetime_cols
            
    def run_analysis(self, analysis_type):
        if self.data is None:
            messagebox.showwarning("Sin Datos", "Por favor, carga un archivo CSV primero para realizar análisis.")
            return

        # Clear previous results immediately
        active_view_frame = self.views[self.current_view_name_str]
        active_view_frame.text_widget.delete(1.0, tk.END)
        for widget in active_view_frame.plot_widget_frame.winfo_children():
            widget.destroy()
        self.result_title.config(text="Calculando...") # Indicate processing
        self.current_plot = None
        self.current_text_result = ""
        self.current_data_table = None

        # Launch the analysis in a thread
        thread = threading.Thread(target=self._analysis_thread_worker, args=(analysis_type,))
        thread.start()

    def _analysis_thread_worker(self, analysis_type):
        try:
            plot = None
            text_result = ""
            title = "Resultado"
            data_table = None # Initialize data_table to None

            if analysis_type == "desc":
                analyzer = AnalizadorExploratorio(self.data)
                text_result, data_table = analyzer.get_resumen_descriptivo()
                title = "Resumen Estadístico Descriptivo"
            
            elif analysis_type == "corr":
                analyzer = AnalizadorExploratorio(self.data)
                plot, text_result_corr = analyzer.plot_correlacion()
                text_result = f"Matriz de Correlación calculada. Consulte el gráfico interactivo.\n\n{text_result_corr}"
                title = "Análisis de Correlación"
            
            elif analysis_type == "dist":
                analyzer = AnalizadorExploratorio(self.data)
                var = self.exp_var_combo.get()
                if not var:
                    raise ValueError("Selecciona una variable para el análisis de distribución.")
                
                plot, plot_info_text = analyzer.plot_distribucion(var)
                freq_text, freq_df = analyzer.get_distribucion_frecuencias(var)
                
                text_result = f"{plot_info_text}\n\n{freq_text}"
                data_table = freq_df # This will be either categorical freq or binned numeric freq
                title = f"Distribución de '{var}'"

            elif analysis_type == "regr":
                analyzer = AnalizadorRegresion(self.data)
                y_var = self.reg_y_combo.get()
                x_vars_indices = self.reg_x_listbox.curselection()
                x_vars = [self.reg_x_listbox.get(i) for i in x_vars_indices]
                if not y_var:
                    raise ValueError("Debes seleccionar la variable dependiente (Y).")
                if not x_vars:
                    raise ValueError("Debes seleccionar al menos una variable independiente (X).")
                
                text_result_full, results_obj = analyzer.ejecutar_regresion(y_var, x_vars)
                plot = analyzer.plot_diagnosticos_regresion()
                title = "Análisis de Regresión Múltiple"
                text_result = text_result_full
                
                # Prepare coefficients table for PDF export
                if results_obj:
                    params_df = results_obj.params.to_frame(name='Coeficiente')
                    params_df['Std Error'] = results_obj.bse
                    params_df['t Value'] = results_obj.tvalues
                    params_df['P > |t|'] = results_obj.pvalues
                    params_df['[0.025'] = results_obj.conf_int()[0]
                    params_df['0.975]'] = results_obj.conf_int()[1]
                    data_table = params_df.round(4) # Round for better display in PDF table

            elif analysis_type == "arima":
                analyzer = AnalizadorSeriesTiempo(self.data)
                time_var = self.ts_time_combo.get()
                target_var = self.ts_target_combo.get()
                
                # Validate inputs for ARIMA order and steps
                try:
                    p = int(self.p_entry.get())
                    d = int(self.d_entry.get())
                    q = int(self.q_entry.get())
                    steps = int(self.forecast_steps_entry.get())
                    if not all(x >= 0 for x in [p, d, q, steps]):
                        raise ValueError("Los valores de p, d, q y pasos de pronóstico deben ser no negativos.")
                except ValueError:
                    raise ValueError("Por favor, introduce números enteros válidos para el orden ARIMA y los pasos de pronóstico.")

                if not time_var or not target_var:
                    raise ValueError("Selecciona las columnas de tiempo y valor objetivo para el pronóstico ARIMA.")
                
                text_report, ts_data_hist, forecast_df_res = analyzer.ejecutar_arima(time_var, target_var, order=(p,d,q), steps=steps)
                plot = analyzer.plot_arima_forecast(ts_data_hist, forecast_df_res)
                title = "Pronóstico ARIMA"
                text_result = text_report
                data_table = forecast_df_res.round(4) # Export forecast as a table, rounded

            self.current_plot = plot
            self.current_text_result = text_result
            self.current_data_table = data_table # Store the DataFrame
            self.after(0, self.update_ui_with_results, plot, text_result, title)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error en Análisis", f"Ocurrió un error durante el análisis: {e}"))
            self.after(0, lambda: self.result_title.config(text="Error en Análisis")) # Reset title on error

    def update_ui_with_results(self, plot, text_result, title):
        active_view_frame = self.views[self.current_view_name_str]
        
        self.result_title.config(text=title)
        active_view_frame.text_widget.delete(1.0, tk.END)
        active_view_frame.text_widget.insert(tk.END, text_result)

        # Clear plot frame
        for widget in active_view_frame.plot_widget_frame.winfo_children():
            widget.destroy()

        if plot:
            # Save as temporary HTML and open in browser for full interactivity
            temp_dir = os.path.join(os.getcwd(), "temp_plots")
            os.makedirs(temp_dir, exist_ok=True)
            path = os.path.join(temp_dir, f"interactive_plot_{self.current_view_name_str}.html")
            plot.write_html(path, auto_open=False) # Do not auto_open here, we'll open it with webbrowser

            # Display a message and a button to open in browser
            plot_frame = active_view_frame.plot_widget_frame
            tk.Label(plot_frame, text="El gráfico interactivo se ha generado y está listo para abrir en tu navegador.", font=self.label_font, fg="white", bg="#1f2833").pack(pady=20)
            tk.Label(plot_frame, text="Haz clic en el botón de abajo para explorarlo:", font=self.label_font, fg="white", bg="#1f2833").pack()
            
            open_button = ttk.Button(plot_frame, text="Abrir Gráfico en Navegador", command=lambda: webbrowser.open('file://' + os.path.abspath(path)), style="TButton")
            open_button.pack(pady=10)

            # Style for the new ttk.Button (defined here to ensure it's applied)
            style = ttk.Style()
            style.configure("TButton", font=self.button_font, background="#45a29e", foreground="white", borderwidth=0, relief="flat", padding=10)
            style.map("TButton", background=[("active", "#66fcf1")], foreground=[("active", "black")])

        else:
            plot_frame = active_view_frame.plot_widget_frame
            tk.Label(plot_frame, text="No hay un gráfico interactivo disponible para este análisis o no se pudo generar.", font=self.label_font, fg="white", bg="#1f2833").pack(pady=20)


    def export_pdf(self):
        if not self.current_text_result and self.current_data_table is None:
            messagebox.showwarning("Vacío", "No hay resultados de texto o tablas para exportar a PDF.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            story = []

            # Add a title
            story.append(Paragraph(f"<b>Reporte de Análisis: {self.result_title['text']}</b>", styles['h1']))
            story.append(Spacer(1, 0.2 * inch))

            # Add the text result
            if self.current_text_result:
                story.append(Paragraph("<b>Resultados Detallados y Resumen:</b>", styles['h2']))
                # Use a monospace font for preformatted text like summaries
                code_style = styles['Code']
                code_style.fontSize = 8 # Smaller font for dense output
                code_style.leading = 9 # Line spacing
                # Replace newline characters with <br/> for ReportLab's Paragraph to interpret them
                story.append(Paragraph(self.current_text_result.replace('\n', '<br/>'), code_style))
                story.append(Spacer(1, 0.2 * inch))

            # Add the DataFrame as a table if available
            if self.current_data_table is not None and not self.current_data_table.empty:
                story.append(Paragraph("<b>Tabla de Datos Adicional:</b>", styles['h2']))
                # Prepare data for ReportLab table, including index as the first column
                # Convert DataFrame to list of lists, ensuring all elements are strings for consistency in PDF
                data_to_export = [self.current_data_table.columns.insert(0, self.current_data_table.index.name if self.current_data_table.index.name else 'Index').tolist()] # Header
                
                for index, row in self.current_data_table.iterrows():
                    # Format float values to a consistent precision, convert everything to string
                    formatted_row = [f"{x:.4f}" if isinstance(x, (float, np.float_)) else str(x) for x in row.tolist()]
                    data_to_export.append([str(index)] + formatted_row)
                
                table = Table(data_to_export)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#45a29e")), # Header background
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Header text color
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'), # Header text alignment
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#34495e")), # Body background
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#1f2833")), # Grid lines
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.white), # Body text color
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'), # Align index column left
                    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), # Align numeric data right
                ]))
                story.append(table)
                story.append(Spacer(1, 0.2 * inch))

            doc.build(story)
            messagebox.showinfo("Éxito", f"Reporte PDF guardado exitosamente en:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo guardar el PDF: {e}")

    def export_plot(self):
        if self.current_plot is None:
            messagebox.showwarning("Sin Gráfico", "No hay gráfico interactivo disponible para exportar.")
            return
        
        # Suggest a default filename based on the current analysis type
        default_filename = f"{self.current_view_name_str}_plot"
        
        path = filedialog.asksaveasfilename(
            defaultextension=".html", 
            filetypes=[("Gráfico Interactivo HTML", "*.html"), ("Imagen PNG", "*.png"), ("Imagen JPEG", "*.jpeg")],
            initialfile=default_filename
        )
        if path:
            try:
                if path.endswith(".html"):
                    self.current_plot.write_html(path, auto_open=False)
                elif path.endswith(".png"):
                    self.current_plot.write_image(path, scale=2) # Higher resolution
                elif path.endswith(".jpeg") or path.endswith(".jpg"):
                    self.current_plot.write_image(path, scale=2, format='jpeg') # Explicitly set format for JPEG
                messagebox.showinfo("Éxito", f"Gráfico guardado exitosamente en:\n{path}")
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"No se pudo guardar el gráfico. Asegúrate de tener 'kaleido' instalado para exportar PNG/JPEG: {e}\n(pip install kaleido)")

if __name__ == "__main__":
    app = DataSuiteApp()
    app.mainloop()