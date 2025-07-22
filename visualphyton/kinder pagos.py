import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
import hashlib
import uuid
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re
import csv # Import csv here for export_data

class AuthenticationManager:
    """Gestor de autenticación y usuarios"""
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        """Carga usuarios desde archivo"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_users(self):
        """Guarda usuarios en archivo"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)

    def hash_password(self, password):
        """Hashea la contraseña de forma segura"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register_user(self, username, email, password, payment_method, payment_details):
        """Registra un nuevo usuario"""
        if username in self.users:
            return False, "El nombre de usuario ya existe"

        if not self.validate_email(email):
            return False, "Email inválido"

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"

        # Verificar si el email ya está registrado
        for user_data in self.users.values():
            if user_data.get('email') == email:
                return False, "El email ya está registrado"

        user_id = str(uuid.uuid4())
        self.users[username] = {
            'id': user_id,
            'email': email,
            'password': self.hash_password(password),
            'payment_method': payment_method,
            'payment_details': payment_details,
            'created_date': datetime.now().isoformat(),
            'subscription_status': 'active',
            'subscription_expires': (datetime.now() + timedelta(days=30)).isoformat()
        }

        self.save_users()
        return True, "Usuario registrado exitosamente"

    def login_user(self, username, password):
        """Autentica un usuario"""
        if username not in self.users:
            return False, "Usuario no encontrado"

        user_data = self.users[username]
        if user_data['password'] != self.hash_password(password):
            return False, "Contraseña incorrecta"

        # Verificar suscripción
        expires = datetime.fromisoformat(user_data['subscription_expires'])
        if datetime.now() > expires:
            return False, "Suscripción expirada. Renueva tu suscripción."

        self.current_user = username
        return True, "Inicio de sesión exitoso"

    def get_current_user_data(self):
        """Obtiene datos del usuario actual"""
        if self.current_user:
            return self.users[self.current_user]
        return None

class PaymentProcessor:
    """Procesador de pagos simulado"""
    def __init__(self):
        self.payment_methods = {
            'paypal': 'PayPal',
            'crypto': 'Criptomonedas',
            'credit_card': 'Tarjeta de Crédito'
        }

    def process_payment(self, method, details, amount):
        """Procesa un pago (simulado)"""
        # En una aplicación real, aquí se integrarían las APIs de pago

        if method == 'paypal':
            return self.process_paypal(details, amount)
        elif method == 'crypto':
            return self.process_crypto(details, amount)
        elif method == 'credit_card':
            return self.process_credit_card(details, amount)

        return False, "Método de pago no válido"

    def process_paypal(self, details, amount):
        """Procesa pago con PayPal (simulado)"""
        email = details.get('email', '')
        if not email or '@' not in email:
            return False, "Email de PayPal inválido"

        # Simulación de procesamiento
        return True, f"Pago de ${amount} procesado con PayPal ({email})"

    def process_crypto(self, details, amount):
        """Procesa pago con criptomonedas (simulado)"""
        wallet = details.get('wallet', '')
        crypto_type = details.get('type', 'Bitcoin')

        if not wallet or len(wallet) < 10:
            return False, "Dirección de wallet inválida"

        return True, f"Pago de ${amount} procesado con {crypto_type} ({wallet[:10]}...)"

    def process_credit_card(self, details, amount):
        """Procesa pago con tarjeta de crédito (simulado)"""
        card_number = details.get('number', '').replace(' ', '')
        cvv = details.get('cvv', '')
        expiry = details.get('expiry', '')

        if not card_number or len(card_number) != 16:
            return False, "Número de tarjeta inválido"

        if not cvv or len(cvv) != 3:
            return False, "CVV inválido"

        return True, f"Pago de ${amount} procesado con tarjeta terminada en {card_number[-4:]}"

class LoginWindow:
    """Ventana de inicio de sesión"""
    def __init__(self, auth_manager, payment_processor, on_success_callback):
        self.auth_manager = auth_manager
        self.payment_processor = payment_processor
        self.on_success_callback = on_success_callback

        self.window = tk.Tk()
        self.window.title("💰 Finanzas Pro - Inicio de Sesión")
        self.window.geometry("500x700")
        self.window.configure(bg="#0f172a")
        self.window.resizable(False, False)

        self.setup_styles()
        self.create_login_interface()

    def setup_styles(self):
        """Configura estilos para la ventana de login"""
        style = ttk.Style(self.window)
        style.theme_use('clam')

        colors = {
            'bg_primary': '#0f172a',
            'bg_secondary': '#1e293b',
            'bg_tertiary': '#334155',
            'accent': '#3b82f6',
            'accent_hover': '#2563eb',
            'success': '#10b981',
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'border': '#475569'
        }

        style.configure('Login.TFrame', background=colors['bg_secondary'])
        style.configure('Login.TLabel',
                        background=colors['bg_secondary'],
                        foreground=colors['text_primary'],
                       font=('Segoe UI', 10))
        style.configure('LoginTitle.TLabel',
                       background=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 20, 'bold'))
        style.configure('Login.TEntry',
                       fieldbackground=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       font=('Segoe UI', 11))
        style.configure('LoginButton.TButton',
                       background=colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 10))

    def create_login_interface(self):
        """Crea la interfaz de inicio de sesión"""
        main_frame = ttk.Frame(self.window, style='Login.TFrame')
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Logo y título
        title_frame = ttk.Frame(main_frame, style='Login.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))

        ttk.Label(title_frame, text="💰", font=('Segoe UI', 48)).pack()
        ttk.Label(title_frame, text="Finanzas Pro",
                  style='LoginTitle.TLabel').pack(pady=(10, 0))
        ttk.Label(title_frame, text="Gestor de Finanzas Personales",
                  style='Login.TLabel').pack(pady=(5, 0))

        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(20, 0))

        # Pestaña de inicio de sesión
        self.create_login_tab()

        # Pestaña de registro
        self.create_register_tab()

    def create_login_tab(self):
        """Crea la pestaña de inicio de sesión"""
        login_frame = ttk.Frame(self.notebook, style='Login.TFrame')
        self.notebook.add(login_frame, text="Iniciar Sesión")

        # Campos de login
        ttk.Label(login_frame, text="Usuario:", style='Login.TLabel').pack(pady=(20, 5))
        self.login_username = ttk.Entry(login_frame, style='Login.TEntry', width=30)
        self.login_username.pack(pady=(0, 15))

        ttk.Label(login_frame, text="Contraseña:", style='Login.TLabel').pack(pady=(0, 5))
        self.login_password = ttk.Entry(login_frame, style='Login.TEntry', width=30, show="*")
        self.login_password.pack(pady=(0, 20))

        # Botón de login
        ttk.Button(login_frame, text="Iniciar Sesión",
                   command=self.handle_login, style='LoginButton.TButton').pack(pady=10)

        # Bind Enter key
        self.login_password.bind('<Return>', lambda e: self.handle_login())

    def create_register_tab(self):
        """Crea la pestaña de registro"""
        register_frame = ttk.Frame(self.notebook, style='Login.TFrame')
        self.notebook.add(register_frame, text="Crear Cuenta")

        # Scroll frame para el registro
        canvas = tk.Canvas(register_frame, bg="#1e293b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(register_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Login.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Información básica
        ttk.Label(scrollable_frame, text="Información de Cuenta",
                  style='Login.TLabel', font=('Segoe UI', 12, 'bold')).pack(pady=(10, 15))

        ttk.Label(scrollable_frame, text="Usuario:", style='Login.TLabel').pack(pady=(0, 5))
        self.reg_username = ttk.Entry(scrollable_frame, style='Login.TEntry', width=30)
        self.reg_username.pack(pady=(0, 10))

        ttk.Label(scrollable_frame, text="Email:", style='Login.TLabel').pack(pady=(0, 5))
        self.reg_email = ttk.Entry(scrollable_frame, style='Login.TEntry', width=30)
        self.reg_email.pack(pady=(0, 10))

        ttk.Label(scrollable_frame, text="Contraseña:", style='Login.TLabel').pack(pady=(0, 5))
        self.reg_password = ttk.Entry(scrollable_frame, style='Login.TEntry', width=30, show="*")
        self.reg_password.pack(pady=(0, 10))

        ttk.Label(scrollable_frame, text="Confirmar Contraseña:", style='Login.TLabel').pack(pady=(0, 5))
        self.reg_confirm_password = ttk.Entry(scrollable_frame, style='Login.TEntry', width=30, show="*")
        self.reg_confirm_password.pack(pady=(0, 20))

        # Método de pago
        ttk.Label(scrollable_frame, text="Método de Pago (Suscripción: $9.99/mes)",
                  style='Login.TLabel', font=('Segoe UI', 12, 'bold')).pack(pady=(0, 15))

        self.payment_method = tk.StringVar(value="paypal")

        # PayPal
        paypal_frame = ttk.Frame(scrollable_frame, style='Login.TFrame')
        paypal_frame.pack(fill='x', pady=5)

        ttk.Radiobutton(paypal_frame, text="💳 PayPal", variable=self.payment_method,
                        value="paypal", command=self.update_payment_fields).pack(anchor='w')

        # Criptomonedas
        crypto_frame = ttk.Frame(scrollable_frame, style='Login.TFrame')
        crypto_frame.pack(fill='x', pady=5)

        ttk.Radiobutton(crypto_frame, text="₿ Criptomonedas", variable=self.payment_method,
                        value="crypto", command=self.update_payment_fields).pack(anchor='w')

        # Tarjeta de crédito
        card_frame = ttk.Frame(scrollable_frame, style='Login.TFrame')
        card_frame.pack(fill='x', pady=5)

        ttk.Radiobutton(card_frame, text="💳 Tarjeta de Crédito", variable=self.payment_method,
                        value="credit_card", command=self.update_payment_fields).pack(anchor='w')

        # Frame para campos de pago
        self.payment_fields_frame = ttk.Frame(scrollable_frame, style='Login.TFrame')
        self.payment_fields_frame.pack(fill='x', pady=(15, 0))

        # Inicializar campos de pago
        self.update_payment_fields()

        # Botón de registro
        ttk.Button(scrollable_frame, text="Crear Cuenta y Suscribirse",
                   command=self.handle_register, style='LoginButton.TButton').pack(pady=20)

        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def update_payment_fields(self):
        """Actualiza los campos de pago según el método seleccionado"""
        # Limpiar campos anteriores
        for widget in self.payment_fields_frame.winfo_children():
            widget.destroy()

        method = self.payment_method.get()

        if method == "paypal":
            self.create_paypal_fields()
        elif method == "crypto":
            self.create_crypto_fields()
        elif method == "credit_card":
            self.create_credit_card_fields()

    def create_paypal_fields(self):
        """Crea campos para PayPal"""
        ttk.Label(self.payment_fields_frame, text="Email de PayPal:",
                  style='Login.TLabel').pack(pady=(0, 5))
        self.paypal_email = ttk.Entry(self.payment_fields_frame, style='Login.TEntry', width=30)
        self.paypal_email.pack(pady=(0, 10))

    def create_crypto_fields(self):
        """Crea campos para criptomonedas"""
        ttk.Label(self.payment_fields_frame, text="Tipo de Criptomoneda:",
                  style='Login.TLabel').pack(pady=(0, 5))
        self.crypto_type = ttk.Combobox(self.payment_fields_frame,
                                        values=["Bitcoin", "Ethereum", "Litecoin", "Dogecoin"],
                                       state='readonly', width=27)
        self.crypto_type.set("Bitcoin")
        self.crypto_type.pack(pady=(0, 10))

        ttk.Label(self.payment_fields_frame, text="Dirección de Wallet:",
                  style='Login.TLabel').pack(pady=(0, 5))
        self.crypto_wallet = ttk.Entry(self.payment_fields_frame, style='Login.TEntry', width=30)
        self.crypto_wallet.pack(pady=(0, 10))

    def create_credit_card_fields(self):
        """Crea campos para tarjeta de crédito"""
        ttk.Label(self.payment_fields_frame, text="Número de Tarjeta:",
                  style='Login.TLabel').pack(pady=(0, 5))
        self.card_number = ttk.Entry(self.payment_fields_frame, style='Login.TEntry', width=30)
        self.card_number.pack(pady=(0, 10))

        # Frame para fecha y CVV
        card_details_frame = ttk.Frame(self.payment_fields_frame, style='Login.TFrame')
        card_details_frame.pack(fill='x', pady=(0, 10))

        # Fecha de expiración
        expiry_frame = ttk.Frame(card_details_frame, style='Login.TFrame')
        expiry_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(expiry_frame, text="MM/AA:", style='Login.TLabel').pack()
        self.card_expiry = ttk.Entry(expiry_frame, style='Login.TEntry', width=8)
        self.card_expiry.pack()

        # CVV
        cvv_frame = ttk.Frame(card_details_frame, style='Login.TFrame')
        cvv_frame.pack(side='right', fill='x', expand=True)

        ttk.Label(cvv_frame, text="CVV:", style='Login.TLabel').pack()
        self.card_cvv = ttk.Entry(cvv_frame, style='Login.TEntry', width=8, show="*")
        self.card_cvv.pack()

        # Nombre en la tarjeta
        ttk.Label(self.payment_fields_frame, text="Nombre en la Tarjeta:",
                  style='Login.TLabel').pack(pady=(10, 5))
        self.card_name = ttk.Entry(self.payment_fields_frame, style='Login.TEntry', width=30)
        self.card_name.pack(pady=(0, 10))

    def handle_login(self):
        """Maneja el inicio de sesión"""
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        success, message = self.auth_manager.login_user(username, password)

        if success:
            self.window.destroy()
            self.on_success_callback()
        else:
            messagebox.showerror("Error de Autenticación", message)

    def handle_register(self):
        """Maneja el registro de usuario"""
        # Validar campos básicos
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm_password.get()

        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Obtener detalles de pago
        payment_details = self.get_payment_details()
        if not payment_details:
            return

        # Procesar pago
        success, message = self.payment_processor.process_payment(
            self.payment_method.get(),
            payment_details,
            9.99
        )

        if not success:
            messagebox.showerror("Error de Pago", message)
            return

        # Registrar usuario
        success, message = self.auth_manager.register_user(
            username, email, password,
            self.payment_method.get(),
            payment_details
        )

        if success:
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente. Ahora puede iniciar sesión.")
            self.notebook.select(0)  # Cambiar a pestaña de login
            self.clear_register_form()
        else:
            messagebox.showerror("Error de Registro", message)

    def get_payment_details(self):
        """Obtiene los detalles de pago según el método seleccionado"""
        method = self.payment_method.get()

        if method == "paypal":
            email = self.paypal_email.get().strip()
            if not email:
                messagebox.showerror("Error", "Por favor ingrese su email de PayPal")
                return None
            return {"email": email}

        elif method == "crypto":
            crypto_type = self.crypto_type.get()
            wallet = self.crypto_wallet.get().strip()
            if not wallet:
                messagebox.showerror("Error", "Por favor ingrese su dirección de wallet")
                return None
            return {"type": crypto_type, "wallet": wallet}

        elif method == "credit_card":
            number = self.card_number.get().strip().replace(" ", "")
            expiry = self.card_expiry.get().strip()
            cvv = self.card_cvv.get().strip()
            name = self.card_name.get().strip()

            if not all([number, expiry, cvv, name]):
                messagebox.showerror("Error", "Por favor complete todos los campos de la tarjeta")
                return None

            return {
                "number": number,
                "expiry": expiry,
                "cvv": cvv,
                "name": name
            }

        return None

    def clear_register_form(self):
        """Limpia el formulario de registro"""
        self.reg_username.delete(0, tk.END)
        self.reg_email.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)
        self.reg_confirm_password.delete(0, tk.END)

    def run(self):
        """Ejecuta la ventana de login"""
        self.window.mainloop()

class FinanceManager(tk.Tk):
    """
    Gestor de Finanzas Personales Avanzado con autenticación
    """
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
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
        self.budgets = []
        self.goals = [] # Nuevo: Lista para almacenar las metas

        self.setup_styles()
        self.create_main_interface()
        self.load_user_data()
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
            'warning': '#facc15', # Añadido color de advertencia
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'border': '#475569'
        }

        # Estilos para frames
        style.configure('Dark.TFrame', background=colors['bg_secondary'])
        style.configure('Card.TFrame', background=colors['bg_tertiary'], relief='solid', borderwidth=1, bordercolor=colors['border']) # Borde más visible

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
        # Estilos para progreso de metas
        style.configure('GoalProgress.TLabel',
                        background=colors['bg_tertiary'],
                        foreground=colors['text_primary'],
                        font=('Segoe UI', 10, 'bold'))


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
        style.map('Dark.TCombobox', fieldbackground=[('readonly', colors['bg_tertiary'])])


        # Estilos para botones
        style.configure('Accent.TButton',
                       background=colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       relief='flat')
        style.map('Accent.TButton',
                 background=[('active', colors['accent_hover'])])

        style.configure('Success.TButton',
                       background=colors['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       relief='flat')
        style.map('Success.TButton',
                 background=[('active', colors['success'])]) # No cambia mucho en hover

        style.configure('Danger.TButton',
                       background=colors['danger'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       relief='flat')
        style.map('Danger.TButton',
                 background=[('active', colors['danger'])])

        # Estilos para treeview
        style.configure("Dark.Treeview",
                       background=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       fieldbackground=colors['bg_tertiary'],
                       font=('Segoe UI', 9),
                       bordercolor=colors['border'])
        style.configure("Dark.Treeview.Heading",
                       background=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat')
        style.map('Dark.Treeview.Heading',
                  background=[('active', colors['bg_secondary'])]) # Mantener color en hover
        # Estilos de tags para colorear filas en Treeview
        style.map('Dark.Treeview',
                  background=[('selected', colors['accent'])]) # Color al seleccionar

    def create_main_interface(self):
        """Crea la interfaz principal con pestañas"""
        # Frame principal
        main_frame = ttk.Frame(self, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título principal con información de usuario
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(title_frame, text="💰 Finanzas Pro",
                  style='Title.TLabel').pack(side='left')

        # Información de usuario
        user_info_frame = ttk.Frame(title_frame, style='Dark.TFrame')
        user_info_frame.pack(side='right')

        user_data = self.auth_manager.get_current_user_data()
        if user_data:
            ttk.Label(user_info_frame, text=f"👤 {self.auth_manager.current_user}",
                      style='Dark.TLabel').pack(side='left', padx=10)

            # Información de suscripción
            expires = datetime.fromisoformat(user_data['subscription_expires'])
            days_left = (expires - datetime.now()).days

            status_text = f"📅 {days_left} días restantes"
            if days_left <= 7:
                status_text += " ⚠️"

            ttk.Label(user_info_frame, text=status_text,
                      style='Dark.TLabel').pack(side='left', padx=10)

        # Botones de utilidad
        utils_frame = ttk.Frame(user_info_frame, style='Dark.TFrame')
        utils_frame.pack(side='right', padx=(20, 0))

        ttk.Button(utils_frame, text="Exportar Datos", command=self.export_data, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(utils_frame, text="Cerrar Sesión", command=self.logout, style='Danger.TButton').pack(side='left', padx=5)


        # Notebook para las pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_budget_tab()
        self.create_goals_tab() # Nuevo: Pestaña de Metas
        self.create_reports_tab()

    def create_dashboard_tab(self):
        """Crea la pestaña de resumen (dashboard)"""
        dashboard_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(dashboard_frame, text="📊 Resumen")

        # Top section for Balance and quick stats
        top_dashboard_frame = ttk.Frame(dashboard_frame, style='Dark.TFrame')
        top_dashboard_frame.pack(fill='x', padx=20, pady=20)

        # Balance Actual
        balance_card = ttk.Frame(top_dashboard_frame, style='Card.TFrame', padding=20)
        balance_card.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ttk.Label(balance_card, text="Balance Actual:", style='Subtitle.TLabel').pack(anchor='w')
        self.balance_label = ttk.Label(balance_card, text=f"${self.current_balance:.2f}",
                                       style='Balance.TLabel')
        self.balance_label.pack(anchor='w', pady=(5, 0))

        # Quick Stats (Ingresos/Gastos del mes actual)
        stats_card = ttk.Frame(top_dashboard_frame, style='Card.TFrame', padding=20)
        stats_card.pack(side='right', fill='x', expand=True, padx=(10, 0))
        ttk.Label(stats_card, text="Resumen del Mes Actual:", style='Subtitle.TLabel').pack(anchor='w')
        self.monthly_income_label = ttk.Label(stats_card, text="Ingresos: $0.00", style='Dark.TLabel', foreground='#10b981')
        self.monthly_income_label.pack(anchor='w', pady=(5, 2))
        self.monthly_expenses_label = ttk.Label(stats_card, text="Gastos: $0.00", style='Dark.TLabel', foreground='#ef4444')
        self.monthly_expenses_label.pack(anchor='w', pady=(0, 5))

        # Middle section for Balance Trend
        trend_frame = ttk.Frame(dashboard_frame, style='Card.TFrame', padding=20)
        trend_frame.pack(pady=(0, 20), padx=20, fill='both', expand=True)
        ttk.Label(trend_frame, text="Tendencia del Balance", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 10))

        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor='#1e293b')
        self.ax.set_facecolor('#1e293b')
        self.ax.tick_params(axis='x', colors='#cbd5e1')
        self.ax.tick_params(axis='y', colors='#cbd5e1')
        self.ax.spines['bottom'].set_color('#475569')
        self.ax.spines['top'].set_color('#475569')
        self.ax.spines['right'].set_color('#475569')
        self.ax.spines['left'].set_color('#475569')
        self.ax.title.set_color('#f8fafc')
        self.ax.xaxis.label.set_color('#f8fafc')
        self.ax.yaxis.label.set_color('#f8fafc')
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=trend_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bottom section for Budget Summary (quick glance)
        budget_summary_frame = ttk.Frame(dashboard_frame, style='Card.TFrame', padding=20)
        budget_summary_frame.pack(pady=(0, 20), padx=20, fill='x')
        ttk.Label(budget_summary_frame, text="Presupuestos Activos (Este Mes)", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 10))

        self.dashboard_budget_tree = ttk.Treeview(budget_summary_frame,
                                                  columns=("Categoría", "Monto", "Gastado", "Restante", "Estado"),
                                                  show="headings", style="Dark.Treeview", height=3) # Limit height
        self.dashboard_budget_tree.pack(fill='both', expand=True)

        self.dashboard_budget_tree.heading("Categoría", text="Categoría")
        self.dashboard_budget_tree.heading("Monto", text="Presupuestado")
        self.dashboard_budget_tree.heading("Gastado", text="Gastado")
        self.dashboard_budget_tree.heading("Restante", text="Restante")
        self.dashboard_budget_tree.heading("Estado", text="Estado")

        self.dashboard_budget_tree.column("Categoría", width=120)
        self.dashboard_budget_tree.column("Monto", width=90, anchor='e')
        self.dashboard_budget_tree.column("Gastado", width=90, anchor='e')
        self.dashboard_budget_tree.column("Restante", width=90, anchor='e')
        self.dashboard_budget_tree.column("Estado", width=80, anchor='center')


    def create_transactions_tab(self):
        """Crea la pestaña de transacciones"""
        transactions_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(transactions_frame, text="💸 Transacciones")

        # Frame para añadir nueva transacción
        add_transaction_frame = ttk.Frame(transactions_frame, style='Card.TFrame', padding=20)
        add_transaction_frame.pack(pady=20, padx=20, fill='x')

        ttk.Label(add_transaction_frame, text="Añadir Nueva Transacción",
                  style='Subtitle.TLabel').grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky='w')

        # Descripción
        ttk.Label(add_transaction_frame, text="Descripción:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.transaction_description = ttk.Entry(add_transaction_frame, style='Dark.TEntry', width=40)
        self.transaction_description.grid(row=1, column=1, padx=(0, 10), pady=5, sticky='ew')

        # Monto
        ttk.Label(add_transaction_frame, text="Monto:", style='Dark.TLabel').grid(row=1, column=2, sticky='w', pady=5)
        self.transaction_amount = ttk.Entry(add_transaction_frame, style='Dark.TEntry', width=20)
        self.transaction_amount.grid(row=1, column=3, pady=5, sticky='ew')

        # Tipo (Ingreso/Gasto)
        ttk.Label(add_transaction_frame, text="Tipo:", style='Dark.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.transaction_type = ttk.Combobox(add_transaction_frame,
                                             values=["Ingreso", "Gasto"],
                                             state='readonly', style='Dark.TCombobox', width=37)
        self.transaction_type.set("Gasto")
        self.transaction_type.grid(row=2, column=1, padx=(0, 10), pady=5, sticky='ew')
        self.transaction_type.bind("<<ComboboxSelected>>", self.update_categories_dropdown)


        # Categoría
        ttk.Label(add_transaction_frame, text="Categoría:", style='Dark.TLabel').grid(row=2, column=2, sticky='w', pady=5)
        self.transaction_category = ttk.Combobox(add_transaction_frame,
                                                  values=self.categories["Gastos"],
                                                  state='readonly', style='Dark.TCombobox', width=17)
        self.transaction_category.set("Otros")
        self.transaction_category.grid(row=2, column=3, pady=5, sticky='ew')

        # Cuenta
        ttk.Label(add_transaction_frame, text="Cuenta:", style='Dark.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.transaction_account = ttk.Combobox(add_transaction_frame,
                                                values=self.accounts,
                                                state='readonly', style='Dark.TCombobox', width=37)
        self.transaction_account.set("Efectivo")
        self.transaction_account.grid(row=3, column=1, padx=(0, 10), pady=5, sticky='ew')

        # Fecha
        ttk.Label(add_transaction_frame, text="Fecha (DD-MM-AAAA):", style='Dark.TLabel').grid(row=3, column=2, sticky='w', pady=5)
        self.transaction_date = ttk.Entry(add_transaction_frame, style='Dark.TEntry', width=20)
        self.transaction_date.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.transaction_date.grid(row=3, column=3, pady=5, sticky='ew')

        # Botón de añadir
        ttk.Button(add_transaction_frame, text="Añadir Transacción",
                   command=self.add_transaction, style='Accent.TButton').grid(row=4, column=0, columnspan=4, pady=20)

        add_transaction_frame.columnconfigure(1, weight=1)
        add_transaction_frame.columnconfigure(3, weight=1)


        # Lista de transacciones
        ttk.Label(transactions_frame, text="Historial de Transacciones",
                  style='Subtitle.TLabel').pack(pady=(10, 5), padx=20, anchor='w')

        self.transactions_tree = ttk.Treeview(transactions_frame,
                                              columns=("Fecha", "Tipo", "Descripción", "Categoría", "Monto", "Cuenta"),
                                              show="headings", style="Dark.Treeview")
        self.transactions_tree.pack(pady=10, padx=20, fill='both', expand=True)

        self.transactions_tree.heading("Fecha", text="Fecha")
        self.transactions_tree.heading("Tipo", text="Tipo")
        self.transactions_tree.heading("Descripción", text="Descripción")
        self.transactions_tree.heading("Categoría", text="Categoría")
        self.transactions_tree.heading("Monto", text="Monto")
        self.transactions_tree.heading("Cuenta", text="Cuenta")

        self.transactions_tree.column("Fecha", width=100, anchor='center')
        self.transactions_tree.column("Tipo", width=80, anchor='center')
        self.transactions_tree.column("Descripción", width=250)
        self.transactions_tree.column("Categoría", width=120)
        self.transactions_tree.column("Monto", width=100, anchor='e')
        self.transactions_tree.column("Cuenta", width=120)

        # Botones de edición y eliminación
        action_buttons_frame = ttk.Frame(transactions_frame, style='Dark.TFrame')
        action_buttons_frame.pack(pady=(0, 10), padx=20, fill='x')

        ttk.Button(action_buttons_frame, text="Editar Selección", command=self.edit_transaction, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(action_buttons_frame, text="Eliminar Selección", command=self.delete_transaction, style='Danger.TButton').pack(side='left', padx=5)


    def create_budget_tab(self):
        """Crea la pestaña de presupuestos"""
        budget_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(budget_frame, text="💰 Presupuestos")

        # Frame para añadir presupuesto
        add_budget_frame = ttk.Frame(budget_frame, style='Card.TFrame', padding=20)
        add_budget_frame.pack(pady=20, padx=20, fill='x')

        ttk.Label(add_budget_frame, text="Crear Nuevo Presupuesto",
                  style='Subtitle.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='w')

        # Categoría
        ttk.Label(add_budget_frame, text="Categoría de Gasto:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.budget_category = ttk.Combobox(add_budget_frame,
                                             values=self.categories["Gastos"],
                                             state='readonly', style='Dark.TCombobox', width=30)
        self.budget_category.set("Alimentación")
        self.budget_category.grid(row=1, column=1, pady=5, sticky='ew')

        # Monto
        ttk.Label(add_budget_frame, text="Monto del Presupuesto ($):", style='Dark.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.budget_amount = ttk.Entry(add_budget_frame, style='Dark.TEntry', width=30)
        self.budget_amount.grid(row=2, column=1, pady=5, sticky='ew')

        # Periodo
        ttk.Label(add_budget_frame, text="Periodo:", style='Dark.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.budget_period = ttk.Combobox(add_budget_frame,
                                          values=["Mensual", "Semanal", "Anual"],
                                          state='readonly', style='Dark.TCombobox', width=30)
        self.budget_period.set("Mensual")
        self.budget_period.grid(row=3, column=1, pady=5, sticky='ew')

        # Botón de añadir presupuesto
        ttk.Button(add_budget_frame, text="Guardar Presupuesto",
                   command=self.add_budget, style='Accent.TButton').grid(row=4, column=0, columnspan=2, pady=20)

        add_budget_frame.columnconfigure(1, weight=1)

        # Lista de presupuestos
        ttk.Label(budget_frame, text="Tus Presupuestos",
                  style='Subtitle.TLabel').pack(pady=(10, 5), padx=20, anchor='w')

        self.budget_tree = ttk.Treeview(budget_frame,
                                        columns=("Categoría", "Monto Presupuestado", "Gastado", "Restante", "Periodo", "Estado"),
                                        show="headings", style="Dark.Treeview")
        self.budget_tree.pack(pady=10, padx=20, fill='both', expand=True)

        self.budget_tree.heading("Categoría", text="Categoría")
        self.budget_tree.heading("Monto Presupuestado", text="Monto Presupuestado")
        self.budget_tree.heading("Gastado", text="Gastado")
        self.budget_tree.heading("Restante", text="Restante")
        self.budget_tree.heading("Periodo", text="Periodo")
        self.budget_tree.heading("Estado", text="Estado")

        self.budget_tree.column("Categoría", width=150)
        self.budget_tree.column("Monto Presupuestado", width=150, anchor='e')
        self.budget_tree.column("Gastado", width=100, anchor='e')
        self.budget_tree.column("Restante", width=100, anchor='e')
        self.budget_tree.column("Periodo", width=100, anchor='center')
        self.budget_tree.column("Estado", width=120, anchor='center')

        # Botones de edición y eliminación
        budget_action_buttons_frame = ttk.Frame(budget_frame, style='Dark.TFrame')
        budget_action_buttons_frame.pack(pady=(0, 10), padx=20, fill='x')

        ttk.Button(budget_action_buttons_frame, text="Eliminar Presupuesto", command=self.delete_budget, style='Danger.TButton').pack(side='left', padx=5)

    def create_goals_tab(self): # Nuevo método para la pestaña de Metas
        """Crea la pestaña de metas financieras."""
        goals_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(goals_frame, text="🎯 Metas")

        # Frame para añadir nueva meta
        add_goal_frame = ttk.Frame(goals_frame, style='Card.TFrame', padding=20)
        add_goal_frame.pack(pady=20, padx=20, fill='x')

        ttk.Label(add_goal_frame, text="Añadir Nueva Meta de Ahorro",
                  style='Subtitle.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='w')

        ttk.Label(add_goal_frame, text="Nombre de la Meta:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.goal_name = ttk.Entry(add_goal_frame, style='Dark.TEntry', width=40)
        self.goal_name.grid(row=1, column=1, pady=5, sticky='ew')

        ttk.Label(add_goal_frame, text="Monto Objetivo ($):", style='Dark.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.goal_target_amount = ttk.Entry(add_goal_frame, style='Dark.TEntry', width=40)
        self.goal_target_amount.grid(row=2, column=1, pady=5, sticky='ew')

        ttk.Label(add_goal_frame, text="Fecha Límite (DD-MM-AAAA):", style='Dark.TLabel').grid(row=3, column=0, sticky='w', pady=5)
        self.goal_due_date = ttk.Entry(add_goal_frame, style='Dark.TEntry', width=40)
        self.goal_due_date.insert(0, (datetime.now() + timedelta(days=365)).strftime("%d-%m-%Y"))
        self.goal_due_date.grid(row=3, column=1, pady=5, sticky='ew')

        ttk.Button(add_goal_frame, text="Guardar Meta",
                   command=self.add_goal, style='Accent.TButton').grid(row=4, column=0, columnspan=2, pady=20)

        add_goal_frame.columnconfigure(1, weight=1)

        # Lista de metas
        ttk.Label(goals_frame, text="Tus Metas de Ahorro",
                  style='Subtitle.TLabel').pack(pady=(10, 5), padx=20, anchor='w')

        self.goals_tree = ttk.Treeview(goals_frame,
                                        columns=("Nombre", "Objetivo", "Ahorrado", "Faltante", "Progreso", "Fecha Límite", "Estado"),
                                        show="headings", style="Dark.Treeview")
        self.goals_tree.pack(pady=10, padx=20, fill='both', expand=True)

        self.goals_tree.heading("Nombre", text="Nombre de la Meta")
        self.goals_tree.heading("Objetivo", text="Monto Objetivo")
        self.goals_tree.heading("Ahorrado", text="Ahorrado")
        self.goals_tree.heading("Faltante", text="Faltante")
        self.goals_tree.heading("Progreso", text="Progreso")
        self.goals_tree.heading("Fecha Límite", text="Fecha Límite")
        self.goals_tree.heading("Estado", text="Estado")

        self.goals_tree.column("Nombre", width=150)
        self.goals_tree.column("Objetivo", width=100, anchor='e')
        self.goals_tree.column("Ahorrado", width=100, anchor='e')
        self.goals_tree.column("Faltante", width=100, anchor='e')
        self.goals_tree.column("Progreso", width=80, anchor='center')
        self.goals_tree.column("Fecha Límite", width=100, anchor='center')
        self.goals_tree.column("Estado", width=80, anchor='center')

        # Botones de acción para metas
        goal_action_buttons_frame = ttk.Frame(goals_frame, style='Dark.TFrame')
        goal_action_buttons_frame.pack(pady=(0, 10), padx=20, fill='x')
        ttk.Button(goal_action_buttons_frame, text="Eliminar Meta", command=self.delete_goal, style='Danger.TButton').pack(side='left', padx=5)


    def create_reports_tab(self):
        """Crea la pestaña de informes"""
        reports_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(reports_frame, text="📈 Informes")

        # Opciones de informe
        options_frame = ttk.Frame(reports_frame, style='Card.TFrame', padding=20)
        options_frame.pack(pady=20, padx=20, fill='x')

        ttk.Label(options_frame, text="Generar Informes",
                  style='Subtitle.TLabel').grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky='w')

        ttk.Label(options_frame, text="Tipo de Informe:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.report_type = ttk.Combobox(options_frame,
                                        values=["Gastos por Categoría", "Ingresos por Categoría", "Tendencia Mensual", "Balance Anual", "Análisis de Cuentas"],
                                        state='readonly', style='Dark.TCombobox', width=30)
        self.report_type.set("Gastos por Categoría")
        self.report_type.grid(row=1, column=1, pady=5, sticky='ew')

        ttk.Button(options_frame, text="Generar Informe", command=self.generate_report, style='Accent.TButton').grid(row=1, column=2, padx=(10, 0), pady=5)

        options_frame.columnconfigure(1, weight=1)

        # Área de visualización del informe
        self.report_canvas_frame = ttk.Frame(reports_frame, style='Dark.TFrame')
        self.report_canvas_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.report_fig, self.report_ax = plt.subplots(figsize=(10, 5), facecolor='#1e293b')
        self.report_ax.set_facecolor('#1e293b')
        self.report_ax.tick_params(axis='x', colors='#cbd5e1')
        self.report_ax.tick_params(axis='y', colors='#cbd5e1')
        self.report_ax.spines['bottom'].set_color('#475569')
        self.report_ax.spines['top'].set_color('#475569')
        self.report_ax.spines['right'].set_color('#475569')
        self.report_ax.spines['left'].set_color('#475569')
        self.report_ax.title.set_color('#f8fafc')
        self.report_ax.xaxis.label.set_color('#f8fafc')
        self.report_ax.yaxis.label.set_color('#f8fafc')
        self.report_fig.tight_layout()

        self.report_canvas = FigureCanvasTkAgg(self.report_fig, master=self.report_canvas_frame)
        self.report_canvas_widget = self.report_canvas.get_tk_widget()
        self.report_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def load_user_data(self):
        """Carga los datos de transacciones, presupuestos y metas del usuario actual"""
        username = self.auth_manager.current_user
        if not username:
            return

        user_file = f"{username}_data.json"
        if os.path.exists(user_file):
            try:
                with open(user_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_balance = data.get('balance', 0.0)
                    self.transactions = data.get('transactions', [])
                    self.budgets = data.get('budgets', [])
                    self.goals = data.get('goals', []) # Nuevo: Cargar metas
            except:
                self.current_balance = 0.0
                self.transactions = []
                self.budgets = []
                self.goals = []
        else:
            self.current_balance = 0.0
            self.transactions = []
            self.budgets = []
            self.goals = []

    def save_user_data(self):
        """Guarda los datos de transacciones, presupuestos y metas del usuario actual"""
        username = self.auth_manager.current_user
        if not username:
            return

        user_file = f"{username}_data.json"
        data = {
            'balance': self.current_balance,
            'transactions': self.transactions,
            'budgets': self.budgets,
            'goals': self.goals # Nuevo: Guardar metas
        }
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_displays(self):
        """Actualiza todos los elementos de la interfaz que muestran datos"""
        self.balance_label.config(text=f"${self.current_balance:.2f}")
        self.update_monthly_summary() # Actualizar resumen mensual
        self.update_transactions_tree()
        self.update_budget_tree()
        self.update_dashboard_budget_tree() # Actualizar resumen de presupuestos en dashboard
        self.update_goals_tree() # Nuevo: Actualizar árbol de metas
        self.plot_balance_trend()
        self.generate_report() # Regenerar informe por defecto

    def update_monthly_summary(self):
        """Actualiza los ingresos y gastos del mes actual en el dashboard."""
        current_month = datetime.now().strftime("%Y-%m")
        monthly_income = 0.0
        monthly_expenses = 0.0

        for trans in self.transactions:
            trans_date = datetime.fromisoformat(trans['date'])
            if trans_date.strftime("%Y-%m") == current_month:
                if trans['type'] == 'Ingreso':
                    monthly_income += trans['amount']
                elif trans['type'] == 'Gasto':
                    monthly_expenses += abs(trans['amount'])

        self.monthly_income_label.config(text=f"Ingresos: ${monthly_income:.2f}")
        self.monthly_expenses_label.config(text=f"Gastos: ${monthly_expenses:.2f}")


    def add_transaction(self):
        """Añade una nueva transacción a la lista"""
        description = self.transaction_description.get().strip()
        amount_str = self.transaction_amount.get().strip()
        transaction_type = self.transaction_type.get()
        category = self.transaction_category.get()
        account = self.transaction_account.get()
        date_str = self.transaction_date.get().strip()

        if not all([description, amount_str, transaction_type, category, account, date_str]):
            messagebox.showerror("Error", "Por favor complete todos los campos de la transacción.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "El monto debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        try:
            transaction_date = datetime.strptime(date_str, "%d-%m-%Y").isoformat()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-AAAA.")
            return

        original_amount = amount # Guardar el monto original para el registro
        if transaction_type == "Gasto":
            amount *= -1 # Los gastos son negativos

        transaction = {
            "id": str(uuid.uuid4()),
            "date": transaction_date,
            "type": transaction_type,
            "description": description,
            "category": category,
            "amount": amount, # Este es el monto ajustado (+/-)
            "original_amount": original_amount, # Guardar el monto positivo original
            "account": account
        }

        self.transactions.append(transaction)
        self.current_balance += amount
        self.save_user_data()
        self.update_displays()
        self.clear_transaction_form()
        messagebox.showinfo("Éxito", "Transacción añadida correctamente.")

    def update_transactions_tree(self):
        """Actualiza el Treeview de transacciones"""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        # Ordenar transacciones por fecha descendente
        sorted_transactions = sorted(self.transactions, key=lambda x: x['date'], reverse=True)

        for trans in sorted_transactions:
            date_fmt = datetime.fromisoformat(trans['date']).strftime("%d-%m-%Y")
            display_amount = trans.get('original_amount', abs(trans['amount'])) # Usar original_amount si existe
            amount_fmt = f"${display_amount:.2f}"
            if trans['type'] == 'Gasto':
                amount_fmt = f"- {amount_fmt}" # Mostrar gastos con signo negativo visible
                tag_name = 'expense_row'
                self.transactions_tree.tag_configure(tag_name, foreground='#ef4444')
            else:
                amount_fmt = f"+ {amount_fmt}"
                tag_name = 'income_row'
                self.transactions_tree.tag_configure(tag_name, foreground='#10b981')

            self.transactions_tree.insert("", tk.END, iid=trans['id'], tags=(tag_name,),
                                           values=(date_fmt, trans['type'], trans['description'],
                                                   trans['category'], amount_fmt, trans['account']))

    def clear_transaction_form(self):
        """Limpia los campos del formulario de transacción"""
        self.transaction_description.delete(0, tk.END)
        self.transaction_amount.delete(0, tk.END)
        self.transaction_type.set("Gasto")
        self.transaction_category.set("Otros")
        self.transaction_account.set("Efectivo")
        self.transaction_date.delete(0, tk.END)
        self.transaction_date.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.update_categories_dropdown() # Asegura que la categoría se actualice

    def update_categories_dropdown(self, event=None):
        """Actualiza las opciones de categoría según el tipo de transacción seleccionado."""
        selected_type = self.transaction_type.get()
        if selected_type == "Ingreso":
            self.transaction_category['values'] = self.categories["Ingresos"]
            self.transaction_category.set("Salario")
        elif selected_type == "Gasto":
            self.transaction_category['values'] = self.categories["Gastos"]
            self.transaction_category.set("Alimentación")

    def edit_transaction(self):
        """Permite editar una transacción seleccionada"""
        selected_item = self.transactions_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione una transacción para editar.")
            return

        transaction_id = self.transactions_tree.item(selected_item)['iid']
        transaction_to_edit = next((t for t in self.transactions if t['id'] == transaction_id), None)

        if not transaction_to_edit:
            messagebox.showerror("Error", "Transacción no encontrada.")
            return

        # Abrir una nueva ventana o poblar el formulario de edición
        self.open_edit_transaction_window(transaction_to_edit)

    def open_edit_transaction_window(self, transaction):
        """Abre una ventana para editar los detalles de la transacción."""
        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Transacción")
        edit_window.geometry("400x450")
        edit_window.configure(bg="#1e293b")
        edit_window.resizable(False, False)

        edit_frame = ttk.Frame(edit_window, style='Card.TFrame', padding=20)
        edit_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(edit_frame, text="Descripción:", style='Dark.TLabel').pack(pady=(0, 5))
        edit_description = ttk.Entry(edit_frame, style='Dark.TEntry', width=30)
        edit_description.insert(0, transaction['description'])
        edit_description.pack(pady=(0, 10))

        ttk.Label(edit_frame, text="Monto:", style='Dark.TLabel').pack(pady=(0, 5))
        edit_amount = ttk.Entry(edit_frame, style='Dark.TEntry', width=30)
        edit_amount.insert(0, transaction.get('original_amount', abs(transaction['amount']))) # Usar original_amount si existe
        edit_amount.pack(pady=(0, 10))

        ttk.Label(edit_frame, text="Tipo:", style='Dark.TLabel').pack(pady=(0, 5))
        edit_type = ttk.Combobox(edit_frame, values=["Ingreso", "Gasto"], state='readonly', style='Dark.TCombobox', width=27)
        edit_type.set(transaction['type'])
        edit_type.pack(pady=(0, 10))

        ttk.Label(edit_frame, text="Categoría:", style='Dark.TLabel').pack(pady=(0, 5))
        edit_category = ttk.Combobox(edit_frame, values=self.categories[transaction['type']], state='readonly', style='Dark.TCombobox', width=27)
        edit_category.set(transaction['category'])
        edit_category.pack(pady=(0, 10))

        def update_edit_categories(event):
            selected_type = edit_type.get()
            edit_category['values'] = self.categories[selected_type]
            # Intenta mantener la categoría si es válida para el nuevo tipo, si no, elige la primera
            if edit_category.get() not in self.categories[selected_type]:
                edit_category.set(self.categories[selected_type][0])
        edit_type.bind("<<ComboboxSelected>>", update_edit_categories)


        ttk.Label(edit_frame, text="Cuenta:", style='Dark.TLabel').pack(pady=(0, 5))
        edit_account = ttk.Combobox(edit_frame, values=self.accounts, state='readonly', style='Dark.TCombobox', width=27)
        edit_account.set(transaction['account'])
        edit_account.pack(pady=(0, 10))

        ttk.Label(edit_frame, text="Fecha (DD-MM-AAAA):", style='Dark.TLabel').pack(pady=(0, 5))
        edit_date = ttk.Entry(edit_frame, style='Dark.TEntry', width=30)
        edit_date.insert(0, datetime.fromisoformat(transaction['date']).strftime("%d-%m-%Y"))
        edit_date.pack(pady=(0, 20))

        def save_changes():
            new_description = edit_description.get().strip()
            new_amount_str = edit_amount.get().strip()
            new_type = edit_type.get()
            new_category = edit_category.get()
            new_account = edit_account.get()
            new_date_str = edit_date.get().strip()

            if not all([new_description, new_amount_str, new_type, new_category, new_account, new_date_str]):
                messagebox.showerror("Error", "Por favor complete todos los campos.", parent=edit_window)
                return

            try:
                new_amount_val = float(new_amount_str)
                if new_amount_val <= 0:
                    messagebox.showerror("Error", "El monto debe ser un número positivo.", parent=edit_window)
                    return
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido.", parent=edit_window)
                return

            try:
                new_date = datetime.strptime(new_date_str, "%d-%m-%Y").isoformat()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-AAAA.", parent=edit_window)
                return

            # Ajustar balance actual antes de la actualización
            self.current_balance -= transaction['amount'] # Restar el monto viejo (que ya tiene el signo)

            # Calcular el nuevo monto con el signo correcto
            updated_amount = new_amount_val
            if new_type == "Gasto":
                updated_amount *= -1

            transaction['description'] = new_description
            transaction['amount'] = updated_amount # Este es el monto ajustado (+/-)
            transaction['original_amount'] = new_amount_val # El monto positivo original
            transaction['type'] = new_type
            transaction['category'] = new_category
            transaction['account'] = new_account
            transaction['date'] = new_date

            self.current_balance += updated_amount # Sumar el monto nuevo (ya con el signo)
            self.save_user_data()
            self.update_displays()
            messagebox.showinfo("Éxito", "Transacción actualizada correctamente.", parent=edit_window)
            edit_window.destroy()

        ttk.Button(edit_frame, text="Guardar Cambios", command=save_changes, style='Accent.TButton').pack(pady=10)


    def delete_transaction(self):
        """Elimina una transacción seleccionada de la lista"""
        selected_item = self.transactions_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione una transacción para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta transacción?")
        if confirm:
            transaction_id = self.transactions_tree.item(selected_item)['iid']
            transaction_to_delete = next((t for t in self.transactions if t['id'] == transaction_id), None)

            if transaction_to_delete:
                self.transactions.remove(transaction_to_delete)
                self.current_balance -= transaction_to_delete['amount']
                self.save_user_data()
                self.update_displays()
                messagebox.showinfo("Éxito", "Transacción eliminada correctamente.")
            else:
                messagebox.showerror("Error", "Transacción no encontrada.")

    def add_budget(self):
        """Añade un nuevo presupuesto"""
        category = self.budget_category.get()
        amount_str = self.budget_amount.get().strip()
        period = self.budget_period.get()

        if not all([category, amount_str, period]):
            messagebox.showerror("Error", "Por favor complete todos los campos del presupuesto.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "El monto del presupuesto debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto del presupuesto debe ser un número válido.")
            return

        # Verificar si ya existe un presupuesto para la misma categoría y período
        # Para simplificar, asumiremos que un presupuesto mensual para "Alimentación" es único para ese mes
        # Para periodos semanales/anuales, se necesita una lógica de solapamiento más compleja.
        # Aquí, solo evitamos duplicados exactos.
        for budget in self.budgets:
            if budget['category'] == category and budget['period'] == period:
                messagebox.showerror("Error", f"Ya existe un presupuesto para '{category}' en el periodo '{period}'. Por favor edítelo o elimínelo.")
                return

        budget_item = {
            "id": str(uuid.uuid4()),
            "category": category,
            "budgeted_amount": amount,
            "period": period,
            "start_date": datetime.now().isoformat() # Se asume que el presupuesto empieza hoy
        }

        self.budgets.append(budget_item)
        self.save_user_data()
        self.update_displays() # Actualiza ambos árboles de presupuesto
        self.clear_budget_form()
        messagebox.showinfo("Éxito", "Presupuesto añadido correctamente.")

    def update_budget_tree(self):
        """Actualiza el Treeview de presupuestos en la pestaña de Presupuestos"""
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

        for budget in self.budgets:
            category = budget['category']
            budgeted_amount = budget['budgeted_amount']
            period = budget['period']
            start_date = datetime.fromisoformat(budget['start_date'])

            spent_amount = self.calculate_spent_in_period(category, start_date, period)
            remaining_amount = budgeted_amount - spent_amount

            status, tag_color = self.get_budget_status_and_tag(remaining_amount, budgeted_amount)

            self.budget_tree.insert("", tk.END, iid=budget['id'], tags=(tag_color,),
                                     values=(category, f"${budgeted_amount:.2f}",
                                             f"${spent_amount:.2f}", f"${remaining_amount:.2f}",
                                             period, status))

    def update_dashboard_budget_tree(self):
        """Actualiza el Treeview de presupuestos en el Dashboard (solo mensuales activos)."""
        for item in self.dashboard_budget_tree.get_children():
            self.dashboard_budget_tree.delete(item)

        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for budget in self.budgets:
            # Solo mostrar presupuestos mensuales que estén activos en el mes actual
            if budget['period'] == "Mensual":
                budget_start_date = datetime.fromisoformat(budget['start_date'])
                if budget_start_date.year == current_month_start.year and \
                   budget_start_date.month == current_month_start.month:

                    category = budget['category']
                    budgeted_amount = budget['budgeted_amount']
                    period = budget['period']
                    
                    spent_amount = self.calculate_spent_in_period(category, budget_start_date, period)
                    remaining_amount = budgeted_amount - spent_amount

                    status, tag_color = self.get_budget_status_and_tag(remaining_amount, budgeted_amount)

                    self.dashboard_budget_tree.insert("", tk.END, iid=budget['id'], tags=(tag_color,),
                                                     values=(category, f"${budgeted_amount:.2f}",
                                                             f"${spent_amount:.2f}", f"${remaining_amount:.2f}",
                                                             status))
        # Ensure tags are configured for the dashboard tree too
        self.dashboard_budget_tree.tag_configure('exceeded_budget', foreground='#ef4444')
        self.dashboard_budget_tree.tag_configure('near_budget', foreground='#facc15')
        self.dashboard_budget_tree.tag_configure('on_track_budget', foreground='#10b981')


    def get_budget_status_and_tag(self, remaining_amount, budgeted_amount):
        """Calcula el estado y el tag de color para un presupuesto."""
        if remaining_amount < 0:
            return "Excedido", 'exceeded_budget'
        elif remaining_amount <= budgeted_amount * 0.15: # Aumentado a 15% para 'Cerca'
            return "Cerca", 'near_budget'
        else:
            return "Dentro", 'on_track_budget'


    def calculate_spent_in_period(self, category, start_date, period):
        """Calcula el monto gastado para una categoría en un período dado."""
        spent = 0.0

        # Define el rango de fechas para el período de presupuesto
        period_start = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        period_end = datetime.now() # Por defecto, hasta la fecha actual

        if period == "Mensual":
            # Si el presupuesto es mensual, calculamos gastos desde el inicio del mes del start_date hasta el final del mes actual
            period_end = period_start.replace(day=28) + timedelta(days=4) # Va al siguiente mes
            period_end = period_end - timedelta(days=period_end.day) # Regresa al último día del mes
            period_end = period_end.replace(hour=23, minute=59, second=59, microsecond=999999) # Fin del día
        elif period == "Semanal":
            period_end = period_start + timedelta(days=7)
            period_end = period_end.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == "Anual":
            period_end = period_start.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

        # Si el periodo del presupuesto es en el futuro, o el actual es anterior al periodo de inicio, no hay gastos
        if datetime.now() < period_start:
            return 0.0
        # Asegurarse de que no contamos gastos futuros en el periodo actual
        if datetime.now() < period_end:
            period_end = datetime.now()


        for trans in self.transactions:
            trans_date = datetime.fromisoformat(trans['date'])
            if trans['type'] == 'Gasto' and trans['category'] == category and period_start <= trans_date <= period_end:
                spent += abs(trans['amount'])
        return spent

    def clear_budget_form(self):
        """Limpia los campos del formulario de presupuesto"""
        self.budget_category.set("Alimentación")
        self.budget_amount.delete(0, tk.END)
        self.budget_period.set("Mensual")

    def delete_budget(self):
        """Elimina un presupuesto seleccionado"""
        selected_item = self.budget_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un presupuesto para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este presupuesto?")
        if confirm:
            budget_id = self.budget_tree.item(selected_item)['iid']
            budget_to_delete = next((b for b in self.budgets if b['id'] == budget_id), None)

            if budget_to_delete:
                self.budgets.remove(budget_to_delete)
                self.save_user_data()
                self.update_displays()
                messagebox.showinfo("Éxito", "Presupuesto eliminado correctamente.")
            else:
                messagebox.showerror("Error", "Presupuesto no encontrado.")

    def add_goal(self):
        """Añade una nueva meta financiera."""
        name = self.goal_name.get().strip()
        target_amount_str = self.goal_target_amount.get().strip()
        due_date_str = self.goal_due_date.get().strip()

        if not all([name, target_amount_str, due_date_str]):
            messagebox.showerror("Error", "Por favor complete todos los campos de la meta.")
            return

        try:
            target_amount = float(target_amount_str)
            if target_amount <= 0:
                messagebox.showerror("Error", "El monto objetivo debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto objetivo debe ser un número válido.")
            return

        try:
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y").isoformat()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha límite inválido. Use DD-MM-AAAA.")
            return

        goal_item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "target_amount": target_amount,
            "saved_amount": 0.0, # Se inicia en 0, se puede actualizar manualmente o con transacciones dedicadas
            "due_date": due_date,
            "created_date": datetime.now().isoformat()
        }

        self.goals.append(goal_item)
        self.save_user_data()
        self.update_goals_tree()
        self.clear_goal_form()
        messagebox.showinfo("Éxito", "Meta de ahorro añadida correctamente.")

    def update_goals_tree(self):
        """Actualiza el Treeview de metas."""
        for item in self.goals_tree.get_children():
            self.goals_tree.delete(item)

        for goal in self.goals:
            name = goal['name']
            target_amount = goal['target_amount']
            saved_amount = goal['saved_amount']
            due_date_fmt = datetime.fromisoformat(goal['due_date']).strftime("%d-%m-%Y")

            remaining_amount = target_amount - saved_amount
            progress_percent = (saved_amount / target_amount) * 100 if target_amount > 0 else 0

            status = "En Progreso"
            tag_color = 'on_track_goal'
            if saved_amount >= target_amount:
                status = "Completada ✅"
                tag_color = 'completed_goal'
            elif datetime.now() > datetime.fromisoformat(goal['due_date']) and saved_amount < target_amount:
                status = "Vencida ❌"
                tag_color = 'overdue_goal'
            elif progress_percent < 50 and datetime.now() + timedelta(days=30) > datetime.fromisoformat(goal['due_date']): # Menos del 50% y menos de 30 días
                status = "Atrasada ⚠️"
                tag_color = 'behind_goal'


            self.goals_tree.insert("", tk.END, iid=goal['id'], tags=(tag_color,),
                                     values=(name, f"${target_amount:.2f}", f"${saved_amount:.2f}",
                                             f"${remaining_amount:.2f}", f"{progress_percent:.1f}%",
                                             due_date_fmt, status))
        # Configure tags for goals treeview
        self.goals_tree.tag_configure('completed_goal', foreground='#10b981', font=('Segoe UI', 9, 'bold'))
        self.goals_tree.tag_configure('overdue_goal', foreground='#ef4444', font=('Segoe UI', 9, 'bold'))
        self.goals_tree.tag_configure('behind_goal', foreground='#facc15', font=('Segoe UI', 9, 'bold'))
        self.goals_tree.tag_configure('on_track_goal', foreground='#f8fafc')


    def clear_goal_form(self):
        """Limpia los campos del formulario de metas."""
        self.goal_name.delete(0, tk.END)
        self.goal_target_amount.delete(0, tk.END)
        self.goal_due_date.delete(0, tk.END)
        self.goal_due_date.insert(0, (datetime.now() + timedelta(days=365)).strftime("%d-%m-%Y"))


    def delete_goal(self):
        """Elimina una meta seleccionada."""
        selected_item = self.goals_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione una meta para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta meta?")
        if confirm:
            goal_id = self.goals_tree.item(selected_item)['iid']
            goal_to_delete = next((g for g in self.goals if g['id'] == goal_id), None)

            if goal_to_delete:
                self.goals.remove(goal_to_delete)
                self.save_user_data()
                self.update_goals_tree()
                messagebox.showinfo("Éxito", "Meta eliminada correctamente.")
            else:
                messagebox.showerror("Error", "Meta no encontrada.")


    def plot_balance_trend(self):
        """Grafica la tendencia del balance a lo largo del tiempo."""
        # Limpiar gráfico anterior
        self.ax.clear()
        self.ax.set_facecolor('#1e293b') # Fondo para el área del plot

        if not self.transactions:
            self.ax.text(0.5, 0.5, "No hay transacciones para mostrar la tendencia.",
                         horizontalalignment='center', verticalalignment='center',
                         color='#cbd5e1', transform=self.ax.transAxes, fontsize=12)
            self.canvas.draw()
            return

        # Agrupar transacciones por fecha para calcular el balance acumulado
        # Usamos un OrderedDict para mantener el orden si hay varias transacciones en el mismo día
        daily_changes = defaultdict(float)
        for trans in self.transactions:
            trans_date = datetime.fromisoformat(trans['date']).date()
            daily_changes[trans_date] += trans['amount']

        sorted_dates = sorted(daily_changes.keys())
        
        cumulative_balances = []
        current_cumulative_balance = 0.0
        for date in sorted_dates:
            current_cumulative_balance += daily_changes[date]
            cumulative_balances.append(current_cumulative_balance)

        # Plotting
        self.ax.plot(sorted_dates, cumulative_balances, marker='o', linestyle='-', color='#3b82f6', linewidth=2, markersize=5)
        self.ax.fill_between(sorted_dates, 0, cumulative_balances, color='#3b82f6', alpha=0.3) # Área bajo la curva

        self.ax.set_title("Tendencia del Balance Acumulado", color='#f8fafc', fontsize=14, pad=15)
        self.ax.set_xlabel("Fecha", color='#f8fafc', labelpad=10)
        self.ax.set_ylabel("Balance ($)", color='#f8fafc', labelpad=10)
        self.ax.grid(True, linestyle='--', alpha=0.6, color='#475569')

        # Formato de las fechas en el eje X
        self.fig.autofmt_xdate(rotation=30, ha='right')
        self.canvas.draw()

    def generate_report(self):
        """Genera un informe según el tipo seleccionado y lo muestra en el gráfico."""
        self.report_ax.clear()
        self.report_ax.set_facecolor('#1e293b')
        self.report_ax.tick_params(axis='x', colors='#cbd5e1')
        self.report_ax.tick_params(axis='y', colors='#cbd5e1')
        self.report_ax.spines['bottom'].set_color('#475569')
        self.report_ax.spines['top'].set_color('#475569')
        self.report_ax.spines['right'].set_color('#475569')
        self.report_ax.spines['left'].set_color('#475569')
        self.report_ax.title.set_color('#f8fafc')
        self.report_ax.xaxis.label.set_color('#f8fafc')
        self.report_ax.yaxis.label.set_color('#f8fafc')

        report_type = self.report_type.get()

        if not self.transactions:
            self.report_ax.text(0.5, 0.5, "No hay transacciones para generar informes.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            self.report_canvas.draw()
            return

        if report_type == "Gastos por Categoría":
            self._plot_expenses_by_category()
        elif report_type == "Ingresos por Categoría":
            self._plot_income_by_category()
        elif report_type == "Tendencia Mensual":
            self._plot_monthly_trend()
        elif report_type == "Balance Anual":
            self._plot_annual_balance()
        elif report_type == "Análisis de Cuentas":
            self._plot_account_analysis()

        self.report_fig.tight_layout()
        self.report_canvas.draw()

    def _plot_expenses_by_category(self):
        """Genera un gráfico de pastel de gastos por categoría."""
        expenses_by_category = defaultdict(float)
        for trans in self.transactions:
            if trans['type'] == 'Gasto':
                expenses_by_category[trans['category']] += abs(trans['amount'])

        if not expenses_by_category:
            self.report_ax.text(0.5, 0.5, "No hay gastos registrados.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            return

        categories = list(expenses_by_category.keys())
        amounts = list(expenses_by_category.values())

        # Colores más vibrantes y con mejor contraste
        colors = plt.cm.Dark2(np.linspace(0, 1, len(categories)))
        wedges, texts, autotexts = self.report_ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90,
                                                    colors=colors, wedgeprops=dict(width=0.4, edgecolor='#1e293b')) # Dona
        # Mejora la visibilidad del texto en el gráfico de pastel
        for text in texts:
            text.set_color('#f8fafc')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)


        self.report_ax.set_title("Distribución de Gastos por Categoría", color='#f8fafc', fontsize=14, pad=15)
        self.report_ax.axis('equal') # Asegura que el pastel sea circular

    def _plot_income_by_category(self):
        """Genera un gráfico de pastel de ingresos por categoría."""
        income_by_category = defaultdict(float)
        for trans in self.transactions:
            if trans['type'] == 'Ingreso':
                income_by_category[trans['category']] += trans['amount']

        if not income_by_category:
            self.report_ax.text(0.5, 0.5, "No hay ingresos registrados.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            return

        categories = list(income_by_category.keys())
        amounts = list(income_by_category.values())

        colors = plt.cm.Set2(np.linspace(0, 1, len(categories)))
        wedges, texts, autotexts = self.report_ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90,
                                                    colors=colors, wedgeprops=dict(width=0.4, edgecolor='#1e293b'))
        for text in texts:
            text.set_color('#f8fafc')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)


        self.report_ax.set_title("Distribución de Ingresos por Categoría", color='#f8fafc', fontsize=14, pad=15)
        self.report_ax.axis('equal')

    def _plot_monthly_trend(self):
        """Genera un gráfico de barras agrupadas de ingresos y gastos mensuales."""
        monthly_data = defaultdict(lambda: {'income': 0.0, 'expenses': 0.0})

        for trans in self.transactions:
            trans_date = datetime.fromisoformat(trans['date'])
            month_year = trans_date.strftime("%Y-%m")
            if trans['type'] == 'Ingreso':
                monthly_data[month_year]['income'] += trans['amount']
            elif trans['type'] == 'Gasto':
                monthly_data[month_year]['expenses'] += abs(trans['amount'])

        if not monthly_data:
            self.report_ax.text(0.5, 0.5, "No hay datos mensuales para graficar.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            return

        sorted_months = sorted(monthly_data.keys())
        incomes = [monthly_data[m]['income'] for m in sorted_months]
        expenses = [monthly_data[m]['expenses'] for m in sorted_months]

        bar_width = 0.35
        r = np.arange(len(sorted_months))

        bars_income = self.report_ax.bar(r - bar_width/2, incomes, color='#10b981', width=bar_width, label='Ingresos', edgecolor='#1e293b')
        bars_expenses = self.report_ax.bar(r + bar_width/2, expenses, color='#ef4444', width=bar_width, label='Gastos', edgecolor='#1e293b')

        self.report_ax.set_xlabel("Mes", color='#f8fafc', labelpad=10)
        self.report_ax.set_ylabel("Monto ($)", color='#f8fafc', labelpad=10)
        self.report_ax.set_title("Ingresos y Gastos Mensuales", color='#f8fafc', fontsize=14, pad=15)
        self.report_ax.set_xticks(r)
        self.report_ax.set_xticklabels(sorted_months, rotation=45, ha="right", color='#cbd5e1')
        self.report_ax.legend(facecolor='#1e293b', edgecolor='#475569', labelcolor='#f8fafc', fontsize=9)
        self.report_ax.grid(axis='y', linestyle='--', alpha=0.6, color='#475569') # Solo grid en Y

        # Añadir valores en las barras
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                self.report_ax.annotate(f'${height:.0f}',
                                        xy=(bar.get_x() + bar.get_width() / 2, height),
                                        xytext=(0, 3),  # 3 points vertical offset
                                        textcoords="offset points",
                                        ha='center', va='bottom', color='#f8fafc', fontsize=8)
        autolabel(bars_income)
        autolabel(bars_expenses)


    def _plot_annual_balance(self):
        """Genera un gráfico de barras del balance anual."""
        annual_balance = defaultdict(float)

        for trans in self.transactions:
            trans_date = datetime.fromisoformat(trans['date'])
            year = trans_date.year
            annual_balance[year] += trans['amount']

        if not annual_balance:
            self.report_ax.text(0.5, 0.5, "No hay datos anuales para graficar.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            return

        sorted_years = sorted(annual_balance.keys())
        balances = [annual_balance[y] for y in sorted_years]

        colors = ['#10b981' if b >= 0 else '#ef4444' for b in balances]
        bars = self.report_ax.bar(sorted_years, balances, color=colors, edgecolor='#1e293b')

        self.report_ax.set_xlabel("Año", color='#f8fafc', labelpad=10)
        self.report_ax.set_ylabel("Balance ($)", color='#f8fafc', labelpad=10)
        self.report_ax.set_title("Balance Anual por Año", color='#f8fafc', fontsize=14, pad=15)
        self.report_ax.set_xticks(sorted_years)
        self.report_ax.tick_params(axis='x', rotation=45, colors='#cbd5e1')
        self.report_ax.grid(axis='y', linestyle='--', alpha=0.6, color='#475569')

        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            self.report_ax.annotate(f'${height:.2f}',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3 if height >= 0 else -15), # Offset según el signo
                                    textcoords="offset points",
                                    ha='center', va='bottom' if height >= 0 else 'top',
                                    color='#f8fafc', fontsize=8)

    def _plot_account_analysis(self):
        """Genera un gráfico de barras mostrando el balance actual por cuenta."""
        account_balances = defaultdict(float)
        for trans in self.transactions:
            account_balances[trans['account']] += trans['amount']

        if not account_balances:
            self.report_ax.text(0.5, 0.5, "No hay transacciones para analizar cuentas.",
                                 horizontalalignment='center', verticalalignment='center',
                                 color='#cbd5e1', transform=self.report_ax.transAxes, fontsize=12)
            return

        accounts = list(account_balances.keys())
        balances = [account_balances[acc] for acc in accounts]

        colors = ['#3b82f6' if b >= 0 else '#ef4444' for b in balances] # Color azul para positivo, rojo para negativo
        bars = self.report_ax.bar(accounts, balances, color=colors, edgecolor='#1e293b')

        self.report_ax.set_xlabel("Cuenta", color='#f8fafc', labelpad=10)
        self.report_ax.set_ylabel("Balance ($)", color='#f8fafc', labelpad=10)
        self.report_ax.set_title("Balance por Cuenta", color='#f8fafc', fontsize=14, pad=15)
        self.report_ax.tick_params(axis='x', rotation=45, colors='#cbd5e1')
        self.report_ax.grid(axis='y', linestyle='--', alpha=0.6, color='#475569')

        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            self.report_ax.annotate(f'${height:.2f}',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3 if height >= 0 else -15),
                                    textcoords="offset points",
                                    ha='center', va='bottom' if height >= 0 else 'top',
                                    color='#f8fafc', fontsize=8)


    def export_data(self):
        """Exporta los datos de transacciones a un archivo CSV."""
        if not self.transactions:
            messagebox.showinfo("Información", "No hay transacciones para exportar.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                   filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                   title="Guardar Transacciones como CSV")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Fecha", "Tipo", "Descripción", "Categoría", "Monto", "Cuenta"])
                    for trans in self.transactions:
                        # Asegurarse de exportar el monto positivo para la columna "Monto"
                        export_amount = abs(trans['amount']) if trans['type'] == 'Gasto' else trans['amount']
                        writer.writerow([trans['id'],
                                         datetime.fromisoformat(trans['date']).strftime("%Y-%m-%d %H:%M:%S"),
                                         trans['type'],
                                         trans['description'],
                                         trans['category'],
                                         export_amount,
                                         trans['account']])
                messagebox.showinfo("Éxito", f"Datos exportados a: {file_path}")
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"No se pudieron exportar los datos: {e}")

    def logout(self):
        """Cierra la sesión del usuario actual y vuelve a la ventana de login."""
        confirm = messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?")
        if confirm:
            self.auth_manager.current_user = None
            self.destroy() # Cierra la ventana actual de FinanceManager
            # Reabre la ventana de login
            auth_manager = AuthenticationManager()
            payment_processor = PaymentProcessor()
            login_window = LoginWindow(auth_manager, payment_processor, lambda: FinanceManager(auth_manager).mainloop())
            login_window.run()


def main():
    auth_manager = AuthenticationManager()
    payment_processor = PaymentProcessor()

    def start_finance_app():
        app = FinanceManager(auth_manager)
        app.mainloop()

    login_window = LoginWindow(auth_manager, payment_processor, start_finance_app)
    login_window.run()

if __name__ == "__main__":
    main()