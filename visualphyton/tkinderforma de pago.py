import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FinanceManager(tk.Tk):
    """
    Gestor de Finanzas Personales Avanzado con gráficos y análisis detallado
    """
    def __init__(self):
        super().__init__()
        self.title("💰 Gestor de Finanzas Personales Pro")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.configure(bg="#0f172a")
        
        # Variables de datos
        self.current_balance = 0.0
        self.transactions = []
        self.categories = {
            "Ingresos": ["Salario", "Freelance", "Inversiones", "Ventas", "Bonos", "Otros"],
            "Gastos": ["Alimentación", "Transporte", "Entretenimiento", "Servicios", "Salud", "Educación", "Otros"]
        }
        self.accounts = ["Efectivo", "Banco Principal", "Banco Secundario", "Tarjeta de Crédito", "Ahorros"]
        
        self.setup_styles()
        self.create_main_interface()
        self.update_displays()
        
    def setup_styles(self):
        """Configura estilos modernos con tema oscuro"""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Colores del tema oscuro moderno
        colors = {
            'bg_primary': '#0f172a',
            'bg_secondary': '#1e293b',
            'bg_tertiary': '#334155',
            'accent': '#3b82f6',
            'accent_hover': '#2563eb',
            'success': '#10b981',
            'danger': '#ef4444',
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'border': '#475569'
        }
        
        # Estilos para frames
        style.configure('Dark.TFrame', background=colors['bg_secondary'])
        style.configure('Card.TFrame', background=colors['bg_tertiary'], relief='solid', borderwidth=1)
        
        # Estilos para labels
        style.configure('Dark.TLabel', 
                       background=colors['bg_secondary'], 
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10))
        style.configure('Title.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel',
                       background=colors['bg_secondary'],
                       foreground=colors['text_secondary'],
                       font=('Segoe UI', 12, 'bold'))
        style.configure('Balance.TLabel',
                       background=colors['bg_tertiary'],
                       foreground=colors['success'],
                       font=('Segoe UI', 18, 'bold'))
        
        # Estilos para entries y comboboxes
        style.configure('Dark.TEntry',
                       fieldbackground=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       font=('Segoe UI', 10))
        style.configure('Dark.TCombobox',
                       fieldbackground=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       font=('Segoe UI', 10))
        
        # Estilos para botones
        style.configure('Accent.TButton',
                       background=colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        style.map('Accent.TButton',
                 background=[('active', colors['accent_hover'])])
        
        style.configure('Success.TButton',
                       background=colors['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        
        # Estilos para treeview
        style.configure("Dark.Treeview",
                       background=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       fieldbackground=colors['bg_tertiary'],
                       font=('Segoe UI', 9))
        style.configure("Dark.Treeview.Heading",
                       background=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 9, 'bold'))
        
    def create_main_interface(self):
        """Crea la interfaz principal con pestañas"""
        # Frame principal
        main_frame = ttk.Frame(self, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título principal
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="💰 Gestor de Finanzas Pro", 
                 style='Title.TLabel').pack(side='left')
        
        # Botones de utilidad
        utils_frame = ttk.Frame(title_frame, style='Dark.TFrame')
        utils_frame.pack(side='right')
        
        ttk.Button(utils_frame, text="💾 Exportar", 
                  command=self.export_data, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(utils_frame, text="📁 Importar", 
                  command=self.import_data, style='Accent.TButton').pack(side='left', padx=5)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Crear pestañas
        self.create_dashboard_tab()
        self.create_transaction_tab()
        self.create_analytics_tab()
        self.create_budget_tab()
        
    def create_dashboard_tab(self):
        """Crea la pestaña del dashboard principal"""
        dashboard_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Panel de resumen superior
        summary_frame = ttk.Frame(dashboard_frame, style='Dark.TFrame')
        summary_frame.pack(fill='x', pady=(0, 20))
        
        # Tarjetas de resumen
        self.create_summary_cards(summary_frame)
        
        # Panel inferior con gráficos
        charts_frame = ttk.Frame(dashboard_frame, style='Dark.TFrame')
        charts_frame.pack(fill='both', expand=True)
        
        # Gráfico de balance histórico
        self.create_balance_chart(charts_frame)
        
        # Transacciones recientes
        recent_frame = ttk.Frame(charts_frame, style='Card.TFrame')
        recent_frame.pack(side='right', fill='y', padx=(10, 0))
        
        ttk.Label(recent_frame, text="Transacciones Recientes", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        self.recent_tree = ttk.Treeview(recent_frame, style='Dark.Treeview',
                                       columns=("type", "amount", "date"), show="headings", height=10)
        self.recent_tree.heading("type", text="Tipo")
        self.recent_tree.heading("amount", text="Monto")
        self.recent_tree.heading("date", text="Fecha")
        self.recent_tree.column("type", width=100)
        self.recent_tree.column("amount", width=100)
        self.recent_tree.column("date", width=120)
        self.recent_tree.pack(padx=10, pady=(0, 10))
        
    def create_summary_cards(self, parent):
        """Crea las tarjetas de resumen financiero"""
        cards_frame = ttk.Frame(parent, style='Dark.TFrame')
        cards_frame.pack(fill='x')
        
        # Balance actual
        balance_card = ttk.Frame(cards_frame, style='Card.TFrame')
        balance_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(balance_card, text="💰 Balance Actual", 
                 style='Subtitle.TLabel').pack(pady=(10, 5))
        self.balance_label = ttk.Label(balance_card, text="$0.00", 
                                      style='Balance.TLabel')
        self.balance_label.pack(pady=(0, 10))
        
        # Ingresos del mes
        income_card = ttk.Frame(cards_frame, style='Card.TFrame')
        income_card.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(income_card, text="📈 Ingresos del Mes", 
                 style='Subtitle.TLabel').pack(pady=(10, 5))
        self.income_label = ttk.Label(income_card, text="$0.00", 
                                     style='Balance.TLabel')
        self.income_label.pack(pady=(0, 10))
        
        # Gastos del mes
        expense_card = ttk.Frame(cards_frame, style='Card.TFrame')
        expense_card.pack(side='left', fill='both', expand=True)
        
        ttk.Label(expense_card, text="📉 Gastos del Mes", 
                 style='Subtitle.TLabel').pack(pady=(10, 5))
        self.expense_label = ttk.Label(expense_card, text="$0.00", 
                                      style='Balance.TLabel')
        self.expense_label.pack(pady=(0, 10))
        
    def create_balance_chart(self, parent):
        """Crea el gráfico de balance histórico"""
        chart_frame = ttk.Frame(parent, style='Card.TFrame')
        chart_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(chart_frame, text="Balance Histórico", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Configurar matplotlib para tema oscuro
        plt.style.use('dark_background')
        
        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor='#334155')
        self.ax.set_facecolor('#334155')
        
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
    def create_transaction_tab(self):
        """Crea la pestaña de transacciones"""
        transaction_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(transaction_frame, text="💳 Transacciones")
        
        # Panel de entrada
        input_frame = ttk.Frame(transaction_frame, style='Card.TFrame')
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="Nueva Transacción", 
                 style='Subtitle.TLabel').grid(row=0, column=0, columnspan=4, pady=10)
        
        # Campos de entrada mejorados
        ttk.Label(input_frame, text="Persona:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.person_entry = ttk.Entry(input_frame, style='Dark.TEntry', width=20)
        self.person_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Tipo:", style='Dark.TLabel').grid(row=1, column=2, sticky='w', padx=10, pady=5)
        self.type_combo = ttk.Combobox(input_frame, style='Dark.TCombobox', 
                                      values=["Ingreso", "Gasto"], state='readonly', width=15)
        self.type_combo.grid(row=1, column=3, padx=10, pady=5, sticky='ew')
        self.type_combo.bind('<<ComboboxSelected>>', self.update_category_options)
        
        ttk.Label(input_frame, text="Categoría:", style='Dark.TLabel').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.category_combo = ttk.Combobox(input_frame, style='Dark.TCombobox', state='readonly', width=20)
        self.category_combo.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Cuenta:", style='Dark.TLabel').grid(row=2, column=2, sticky='w', padx=10, pady=5)
        self.account_combo = ttk.Combobox(input_frame, style='Dark.TCombobox', 
                                         values=self.accounts, state='readonly', width=15)
        self.account_combo.grid(row=2, column=3, padx=10, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Monto ($):", style='Dark.TLabel').grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.amount_entry = ttk.Entry(input_frame, style='Dark.TEntry', width=20)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Descripción:", style='Dark.TLabel').grid(row=3, column=2, sticky='w', padx=10, pady=5)
        self.description_entry = ttk.Entry(input_frame, style='Dark.TEntry', width=25)
        self.description_entry.grid(row=3, column=3, padx=10, pady=5, sticky='ew')
        
        # Botones
        button_frame = ttk.Frame(input_frame, style='Dark.TFrame')
        button_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="✅ Registrar Transacción", 
                  command=self.add_transaction, style='Success.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="🗑️ Limpiar", 
                  command=self.clear_form, style='Accent.TButton').pack(side='left', padx=10)
        
        # Configurar expansión de columnas
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Historial de transacciones
        history_frame = ttk.Frame(transaction_frame, style='Card.TFrame')
        history_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        ttk.Label(history_frame, text="Historial de Transacciones", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Treeview mejorado
        self.history_tree = ttk.Treeview(history_frame, style='Dark.Treeview',
                                        columns=("person", "type", "category", "account", "amount", "balance", "description", "date"), 
                                        show="headings", height=12)
        
        headings = [
            ("person", "Persona", 100),
            ("type", "Tipo", 80),
            ("category", "Categoría", 100),
            ("account", "Cuenta", 100),
            ("amount", "Monto", 100),
            ("balance", "Balance", 100),
            ("description", "Descripción", 150),
            ("date", "Fecha", 130)
        ]
        
        for col, text, width in headings:
            self.history_tree.heading(col, text=text)
            self.history_tree.column(col, width=width, anchor="center" if col in ["type", "amount", "balance"] else "w")
        
        self.history_tree.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_analytics_tab(self):
        """Crea la pestaña de análisis y gráficos"""
        analytics_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analytics_frame, text="📈 Análisis")
        
        # Panel de filtros
        filter_frame = ttk.Frame(analytics_frame, style='Card.TFrame')
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filter_frame, text="Filtros de Análisis", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        filter_controls = ttk.Frame(filter_frame, style='Dark.TFrame')
        filter_controls.pack(pady=(0, 10))
        
        ttk.Label(filter_controls, text="Período:", style='Dark.TLabel').pack(side='left', padx=10)
        self.period_combo = ttk.Combobox(filter_controls, style='Dark.TCombobox',
                                        values=["Último mes", "Últimos 3 meses", "Últimos 6 meses", "Último año"],
                                        state='readonly', width=15)
        self.period_combo.pack(side='left', padx=10)
        self.period_combo.set("Último mes")
        
        ttk.Button(filter_controls, text="🔄 Actualizar Gráficos", 
                  command=self.update_analytics, style='Accent.TButton').pack(side='left', padx=20)
        
        # Panel de gráficos
        charts_container = ttk.Frame(analytics_frame, style='Dark.TFrame')
        charts_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Gráfico de categorías
        category_frame = ttk.Frame(charts_container, style='Card.TFrame')
        category_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(category_frame, text="Gastos por Categoría", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        self.category_fig, self.category_ax = plt.subplots(figsize=(6, 4), facecolor='#334155')
        self.category_canvas = FigureCanvasTkAgg(self.category_fig, category_frame)
        self.category_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Gráfico de tendencias
        trend_frame = ttk.Frame(charts_container, style='Card.TFrame')
        trend_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        ttk.Label(trend_frame, text="Tendencia Mensual", 
                 style='Subtitle.TLabel').pack(pady=10)
        
        self.trend_fig, self.trend_ax = plt.subplots(figsize=(6, 4), facecolor='#334155')
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, trend_frame)
        self.trend_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
    def create_budget_tab(self):
        """Crea la pestaña de presupuesto"""
        budget_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(budget_frame, text="🎯 Presupuesto")
        
        ttk.Label(budget_frame, text="Gestión de Presupuesto", 
                 style='Title.TLabel').pack(pady=20)
        
        # Aquí se puede agregar funcionalidad de presupuesto
        coming_soon = ttk.Label(budget_frame, text="Funcionalidad de presupuesto próximamente...", 
                               style='Subtitle.TLabel')
        coming_soon.pack(pady=50)
        
    def update_category_options(self, event=None):
        """Actualiza las opciones de categoría según el tipo seleccionado"""
        transaction_type = self.type_combo.get()
        if transaction_type == "Ingreso":
            self.category_combo['values'] = self.categories["Ingresos"]
        elif transaction_type == "Gasto":
            self.category_combo['values'] = self.categories["Gastos"]
        else:
            self.category_combo['values'] = []
        
        self.category_combo.set('')
        
    def add_transaction(self):
        """Añade una nueva transacción con validación mejorada"""
        try:
            person = self.person_entry.get().strip()
            transaction_type = self.type_combo.get()
            category = self.category_combo.get()
            account = self.account_combo.get()
            amount_str = self.amount_entry.get().strip()
            description = self.description_entry.get().strip()
            
            # Validaciones
            if not all([person, transaction_type, category, account, amount_str]):
                messagebox.showwarning("Error", "Por favor complete todos los campos obligatorios.")
                return
                
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a cero.")
                return
                
            # Crear transacción
            transaction = {
                'id': len(self.transactions) + 1,
                'person': person,
                'type': transaction_type,
                'category': category,
                'account': account,
                'amount': amount,
                'description': description,
                'date': datetime.now(),
                'balance_after': 0
            }
            
            # Actualizar balance
            if transaction_type == "Ingreso":
                self.current_balance += amount
                amount_display = f"+${amount:.2f}"
            else:
                if self.current_balance < amount:
                    messagebox.showwarning("Saldo Insuficiente", 
                                         "No hay suficiente saldo para realizar esta transacción.")
                    return
                self.current_balance -= amount
                amount_display = f"-${amount:.2f}"
                
            transaction['balance_after'] = self.current_balance
            self.transactions.append(transaction)
            
            # Añadir al historial
            self.history_tree.insert("", 0, values=(
                person,
                transaction_type,
                category,
                account,
                amount_display,
                f"${self.current_balance:.2f}",
                description,
                transaction['date'].strftime("%Y-%m-%d %H:%M")
            ))
            
            self.update_displays()
            self.clear_form()
            messagebox.showinfo("Éxito", "Transacción registrada correctamente.")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto numérico válido.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            
    def clear_form(self):
        """Limpia el formulario de transacciones"""
        self.person_entry.delete(0, tk.END)
        self.type_combo.set('')
        self.category_combo.set('')
        self.account_combo.set('')
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        
    def update_displays(self):
        """Actualiza todas las visualizaciones"""
        self.update_balance_display()
        self.update_recent_transactions()
        self.update_monthly_summary()
        self.update_balance_chart()
        
    def update_balance_display(self):
        """Actualiza la visualización del balance"""
        self.balance_label.config(text=f"${self.current_balance:.2f}")
        
    def update_recent_transactions(self):
        """Actualiza la lista de transacciones recientes"""
        # Limpiar transacciones anteriores
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
            
        # Mostrar las últimas 10 transacciones
        recent_transactions = sorted(self.transactions, key=lambda x: x['date'], reverse=True)[:10]
        
        for transaction in recent_transactions:
            amount_display = f"+${transaction['amount']:.2f}" if transaction['type'] == "Ingreso" else f"-${transaction['amount']:.2f}"
            self.recent_tree.insert("", "end", values=(
                transaction['type'],
                amount_display,
                transaction['date'].strftime("%m-%d %H:%M")
            ))
            
    def update_monthly_summary(self):
        """Actualiza el resumen mensual"""
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        
        monthly_income = sum(t['amount'] for t in self.transactions 
                           if t['type'] == 'Ingreso' and t['date'] >= start_of_month)
        monthly_expenses = sum(t['amount'] for t in self.transactions 
                             if t['type'] == 'Gasto' and t['date'] >= start_of_month)
        
        self.income_label.config(text=f"${monthly_income:.2f}")
        self.expense_label.config(text=f"${monthly_expenses:.2f}")
        
    def update_balance_chart(self):
        """Actualiza el gráfico de balance histórico"""
        self.ax.clear()
        
        if not self.transactions:
            self.ax.text(0.5, 0.5, 'No hay datos disponibles', 
                        ha='center', va='center', transform=self.ax.transAxes,
                        color='#cbd5e1', fontsize=12)
        else:
            # Crear datos para el gráfico
            dates = [t['date'] for t in sorted(self.transactions, key=lambda x: x['date'])]
            balances = []
            running_balance = 0
            
            for transaction in sorted(self.transactions, key=lambda x: x['date']):
                if transaction['type'] == 'Ingreso':
                    running_balance += transaction['amount']
                else:
                    running_balance -= transaction['amount']
                balances.append(running_balance)
            
            self.ax.plot(dates, balances, color='#10b981', linewidth=2, marker='o', markersize=4)
            self.ax.fill_between(dates, balances, alpha=0.3, color='#10b981')
            
        self.ax.set_facecolor('#334155')
        self.ax.tick_params(colors='#cbd5e1')
        self.ax.set_title('Balance Histórico', color='#f8fafc', fontsize=14, fontweight='bold')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def update_analytics(self):
        """Actualiza los gráficos de análisis"""
        # Implementar actualización de gráficos de análisis
        pass
        
    def export_data(self):
        """Exporta los datos a un archivo JSON"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Exportar datos financieros"
            )
            
            if filename:
                export_data = {
                    'balance': self.current_balance,
                    'transactions': []
                }
                
                for transaction in self.transactions:
                    export_transaction = transaction.copy()
                    export_transaction['date'] = transaction['date'].isoformat()
                    export_data['transactions'].append(export_transaction)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
            
    def import_data(self):
        """Importa datos desde un archivo JSON"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Importar datos financieros"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.current_balance = data.get('balance', 0.0)
                self.transactions = []
                
                for transaction_data in data.get('transactions', []):
                    transaction = transaction_data.copy()
                    transaction['date'] = datetime.fromisoformat(transaction_data['date'])
                    self.transactions.append(transaction)
                
                # Actualizar interfaz
                self.update_displays()
                
                # Reconstruir historial
                for item in self.history_tree.get_children():
                    self.history_tree.delete(item)
                
                for transaction in reversed(self.transactions):
                    amount_display = f"+${transaction['amount']:.2f}" if transaction['type'] == "Ingreso" else f"-${transaction['amount']:.2f}"
                    self.history_tree.insert("", 0, values=(
                        transaction['person'],
                        transaction['type'],
                        transaction['category'],
                        transaction['account'],
                        amount_display,
                        f"${transaction['balance_after']:.2f}",
                        transaction['description'],
                        transaction['date'].strftime("%Y-%m-%d %H:%M")
                    ))
                
                messagebox.showinfo("Éxito", f"Datos importados correctamente desde {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar datos: {str(e)}")

    def update_analytics(self):
        """Actualiza los gráficos de análisis"""
        self.update_category_chart()
        self.update_trend_chart()
        
    def update_category_chart(self):
        """Actualiza el gráfico de gastos por categoría"""
        self.category_ax.clear()
        
        # Filtrar gastos del período seleccionado
        period = self.period_combo.get()
        cutoff_date = self.get_cutoff_date(period)
        
        expenses = [t for t in self.transactions 
                   if t['type'] == 'Gasto' and t['date'] >= cutoff_date]
        
        if not expenses:
            self.category_ax.text(0.5, 0.5, 'No hay gastos en el período seleccionado', 
                                ha='center', va='center', transform=self.category_ax.transAxes,
                                color='#cbd5e1', fontsize=10)
        else:
            # Agrupar por categoría
            category_totals = defaultdict(float)
            for expense in expenses:
                category_totals[expense['category']] += expense['amount']
            
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            
            # Crear gráfico de pastel
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            wedges, texts, autotexts = self.category_ax.pie(amounts, labels=categories, 
                                                          autopct='%1.1f%%', colors=colors,
                                                          textprops={'color': '#f8fafc', 'fontsize': 9})
            
        self.category_ax.set_facecolor('#334155')
        self.category_ax.set_title('Gastos por Categoría', color='#f8fafc', fontsize=12, fontweight='bold')
        
        self.category_fig.tight_layout()
        self.category_canvas.draw()
        
    def update_trend_chart(self):
        """Actualiza el gráfico de tendencias mensuales"""
        self.trend_ax.clear()
        
        if not self.transactions:
            self.trend_ax.text(0.5, 0.5, 'No hay datos disponibles', 
                             ha='center', va='center', transform=self.trend_ax.transAxes,
                             color='#cbd5e1', fontsize=10)
        else:
            # Agrupar transacciones por mes
            monthly_data = defaultdict(lambda: {'income': 0, 'expenses': 0})
            
            for transaction in self.transactions:
                month_key = transaction['date'].strftime('%Y-%m')
                if transaction['type'] == 'Ingreso':
                    monthly_data[month_key]['income'] += transaction['amount']
                else:
                    monthly_data[month_key]['expenses'] += transaction['amount']
            
            months = sorted(monthly_data.keys())
            incomes = [monthly_data[month]['income'] for month in months]
            expenses = [monthly_data[month]['expenses'] for month in months]
            
            x = np.arange(len(months))
            width = 0.35
            
            bars1 = self.trend_ax.bar(x - width/2, incomes, width, label='Ingresos', color='#10b981', alpha=0.8)
            bars2 = self.trend_ax.bar(x + width/2, expenses, width, label='Gastos', color='#ef4444', alpha=0.8)
            
            self.trend_ax.set_xlabel('Mes', color='#f8fafc')
            self.trend_ax.set_ylabel('Monto ($)', color='#f8fafc')
            self.trend_ax.set_xticks(x)
            self.trend_ax.set_xticklabels([datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months], 
                                        rotation=45, ha='right')
            self.trend_ax.legend()
            
        self.trend_ax.set_facecolor('#334155')
        self.trend_ax.tick_params(colors='#cbd5e1')
        self.trend_ax.set_title('Tendencia Mensual', color='#f8fafc', fontsize=12, fontweight='bold')
        
        self.trend_fig.tight_layout()
        self.trend_canvas.draw()
        
    def get_cutoff_date(self, period):
        """Obtiene la fecha de corte según el período seleccionado"""
        now = datetime.now()
        if period == "Último mes":
            return now - timedelta(days=30)
        elif period == "Últimos 3 meses":
            return now - timedelta(days=90)
        elif period == "Últimos 6 meses":
            return now - timedelta(days=180)
        elif period == "Último año":
            return now - timedelta(days=365)
        else:
            return datetime.min

class ModernScrollableFrame(ttk.Frame):
    """Frame con scroll personalizado para mejor UX"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0, bg='#1e293b')
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Dark.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class NotificationSystem:
    """Sistema de notificaciones para alertas y recordatorios"""
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        
    def add_notification(self, message, notification_type="info"):
        """Añade una nueva notificación"""
        notification = {
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now()
        }
        self.notifications.append(notification)
        self.show_notification(notification)
        
    def show_notification(self, notification):
        """Muestra una notificación emergente"""
        colors = {
            'info': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }
        
        # Crear ventana de notificación
        notification_window = tk.Toplevel(self.parent)
        notification_window.title("Notificación")
        notification_window.geometry("300x100")
        notification_window.configure(bg=colors.get(notification['type'], '#3b82f6'))
        notification_window.attributes('-topmost', True)
        
        # Centrar la ventana
        notification_window.transient(self.parent)
        notification_window.grab_set()
        
        # Contenido de la notificación
        message_label = tk.Label(notification_window, 
                               text=notification['message'],
                               bg=colors.get(notification['type'], '#3b82f6'),
                               fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               wraplength=280)
        message_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Auto-cerrar después de 3 segundos
        notification_window.after(3000, notification_window.destroy)

class AdvancedReportGenerator:
    """Generador de reportes financieros avanzados"""
    def __init__(self, transactions, balance):
        self.transactions = transactions
        self.balance = balance
        
    def generate_monthly_report(self, year, month):
        """Genera un reporte mensual detallado"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
        monthly_transactions = [
            t for t in self.transactions 
            if start_date <= t['date'] <= end_date
        ]
        
        total_income = sum(t['amount'] for t in monthly_transactions if t['type'] == 'Ingreso')
        total_expenses = sum(t['amount'] for t in monthly_transactions if t['type'] == 'Gasto')
        net_flow = total_income - total_expenses
        
        report = {
            'period': f"{start_date.strftime('%B %Y')}",
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_flow': net_flow,
            'transaction_count': len(monthly_transactions),
            'average_transaction': (total_income + total_expenses) / len(monthly_transactions) if monthly_transactions else 0,
            'categories': self._analyze_categories(monthly_transactions),
            'accounts': self._analyze_accounts(monthly_transactions)
        }
        
        return report
        
    def _analyze_categories(self, transactions):
        """Analiza gastos por categoría"""
        category_analysis = defaultdict(lambda: {'amount': 0, 'count': 0})
        
        for transaction in transactions:
            if transaction['type'] == 'Gasto':
                category_analysis[transaction['category']]['amount'] += transaction['amount']
                category_analysis[transaction['category']]['count'] += 1
                
        return dict(category_analysis)
        
    def _analyze_accounts(self, transactions):
        """Analiza transacciones por cuenta"""
        account_analysis = defaultdict(lambda: {'income': 0, 'expenses': 0, 'count': 0})
        
        for transaction in transactions:
            account = transaction['account']
            account_analysis[account]['count'] += 1
            
            if transaction['type'] == 'Ingreso':
                account_analysis[account]['income'] += transaction['amount']
            else:
                account_analysis[account]['expenses'] += transaction['amount']
                
        return dict(account_analysis)

class BudgetManager:
    """Gestor de presupuestos y metas financieras"""
    def __init__(self):
        self.budgets = {}
        self.goals = {}
        
    def create_budget(self, category, amount, period='monthly'):
        """Crea un nuevo presupuesto para una categoría"""
        self.budgets[category] = {
            'amount': amount,
            'period': period,
            'spent': 0,
            'created_date': datetime.now()
        }
        
    def update_budget_spending(self, category, amount):
        """Actualiza el gasto del presupuesto"""
        if category in self.budgets:
            self.budgets[category]['spent'] += amount
            
    def check_budget_status(self, category):
        """Verifica el estado del presupuesto"""
        if category not in self.budgets:
            return None
            
        budget = self.budgets[category]
        remaining = budget['amount'] - budget['spent']
        percentage_used = (budget['spent'] / budget['amount']) * 100
        
        status = 'normal'
        if percentage_used >= 100:
            status = 'exceeded'
        elif percentage_used >= 80:
            status = 'warning'
            
        return {
            'remaining': remaining,
            'percentage_used': percentage_used,
            'status': status
        }

# Función principal para ejecutar la aplicación
def main():
    """Función principal para iniciar la aplicación"""
    try:
        app = FinanceManager()
        
        # Configurar el cierre limpio
        def on_closing():
            if messagebox.askokcancel("Salir", "¿Desea guardar los datos antes de salir?"):
                # Aquí se podría implementar auto-guardado
                pass
            app.destroy()
            
        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error Critical", f"No se pudo iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()