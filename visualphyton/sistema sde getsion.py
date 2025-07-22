import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import random

# Datos simulados de productos e historial de ventas
productos = [
    "Guitarra eléctrica", "Guitarra acústica", "Batería", "Teclado", "Violín",
    "Bajo", "Micrófono", "Amplificador", "Pedal de efectos", "Ukelele"
]

# Simulación de ventas (producto aleatorio con distintas frecuencias)
ventas = [random.choice(productos) for _ in range(200)]  # Simula 200 ventas
tendencias = Counter(ventas).most_common()

# Función para generar recomendaciones
def recomendar():
    recomendaciones = []
    
    # Tomamos los 3 productos más vendidos
    top_ventas = tendencias[:3]
    recomendaciones.extend([producto for producto, _ in top_ventas])

    # Agregamos 2 productos aleatorios que no estén en top 3
    restantes = [p for p in productos if p not in recomendaciones]
    recomendaciones.extend(random.sample(restantes, 2))
    
    mostrar_recomendaciones(recomendaciones)

# Función para mostrar en interfaz
def mostrar_recomendaciones(lista):
    texto.delete(0, tk.END)
    for producto in lista:
        texto.insert(tk.END, f"🎵 {producto}")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Motor de Recomendación - Tienda de Instrumentos")
ventana.geometry("400x350")
ventana.configure(bg="#f0f0f5")

# Estilo
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 12), padding=10, background="#4CAF50", foreground="white")
style.configure("TLabel", font=("Segoe UI", 14), background="#f0f0f5")
style.configure("TListbox", font=("Segoe UI", 12))

# Etiqueta
ttk.Label(ventana, text="Recomendaciones para ti 🎶").pack(pady=15)

# Botón
ttk.Button(ventana, text="Generar recomendaciones", command=recomendar).pack(pady=10)

# Lista de resultados
texto = tk.Listbox(ventana, height=7, width=40, bg="#ffffff", fg="#333333", font=("Segoe UI", 12))
texto.pack(pady=10)

# Ejecutar
ventana.mainloop()
