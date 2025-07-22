import os
import time
import random
import math
import colorama
from colorama import Fore, Back, Style

# Inicializar colorama para trabajar con colores en la consola
colorama.init(autoreset=True)

class Rectangulo:
    def __init__(self, base, altura, color, nombre="", edad=0, intereses=None, ubicacion=""):
        self.base = base
        self.altura = altura
        self.color = color
        self.nombre = nombre or f"Rect-{random.randint(1000, 9999)}"
        self.edad = edad or random.randint(18, 45)
        self.intereses = intereses or ["geometría", "matemáticas", "simetría"]
        self.ubicacion = ubicacion or random.choice(["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"])
        self.likes_recibidos = 0
        self.matches = 0
        
    def calcular_area(self):
        return self.base * self.altura
    
    def calcular_perimetro(self):
        return 2 * self.base + 2 * self.altura
    
    def dibujar(self):
        """Dibuja el rectángulo en la consola con caracteres ASCII"""
        color_map = {
            "rojo": Fore.RED,
            "verde": Fore.GREEN, 
            "azul": Fore.BLUE,
            "amarillo": Fore.YELLOW,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "blanco": Fore.WHITE,
            "naranja": Fore.YELLOW + Style.BRIGHT
        }
        
        color_code = color_map.get(self.color.lower(), Fore.WHITE)
        
        # Limitar el tamaño para la consola
        base_vis = min(self.base, 20)
        altura_vis = min(self.altura, 10)
        
        print(f"\n{color_code}╔{'═' * (base_vis * 2)}╗")
        for _ in range(altura_vis):
            print(f"{color_code}║{' ' * (base_vis * 2)}║")
        print(f"{color_code}╚{'═' * (base_vis * 2)}╝")
    
    def mostrar_perfil(self):
        """Muestra el perfil completo del rectángulo"""
        color_map = {
            "rojo": Fore.RED,
            "verde": Fore.GREEN, 
            "azul": Fore.BLUE,
            "amarillo": Fore.YELLOW,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "blanco": Fore.WHITE,
            "naranja": Fore.YELLOW + Style.BRIGHT
        }
        
        color_code = color_map.get(self.color.lower(), Fore.WHITE)
        
        print(f"\n{Fore.CYAN}{'═' * 50}")
        print(f"{Fore.CYAN}║ {Style.BRIGHT}{self.nombre}, {self.edad} años{' ' * (37 - len(self.nombre) - len(str(self.edad)))}║")
        print(f"{Fore.CYAN}║ {Style.RESET_ALL}📍 {self.ubicacion}{' ' * (46 - len(self.ubicacion))}║")
        print(f"{Fore.CYAN}║{' ' * 48}║")
        
        self.dibujar()
        
        print(f"{Fore.CYAN}║{' ' * 48}║")
        print(f"{Fore.CYAN}║ {color_code}Color: {self.color.capitalize()}{' ' * (41 - len(self.color))}║")
        print(f"{Fore.CYAN}║ 📐 Base: {self.base} | Altura: {self.altura}{' ' * (32 - len(str(self.base)) - len(str(self.altura)))}║")
        print(f"{Fore.CYAN}║ 🔷 Área: {self.calcular_area()}{' ' * (42 - len(str(self.calcular_area())))}║")
        print(f"{Fore.CYAN}║ 📏 Perímetro: {self.calcular_perimetro()}{' ' * (37 - len(str(self.calcular_perimetro())))}║")
        print(f"{Fore.CYAN}║{' ' * 48}║")
        
        intereses_str = ", ".join(self.intereses[:3])
        print(f"{Fore.CYAN}║ {Fore.MAGENTA}❤ Intereses: {intereses_str}{' ' * (36 - len(intereses_str))}║")
        print(f"{Fore.CYAN}║ 👍 Likes: {self.likes_recibidos} | 💕 Matches: {self.matches}{' ' * (31 - len(str(self.likes_recibidos)) - len(str(self.matches)))}║")
        print(f"{Fore.CYAN}{'═' * 50}")

class TinderRectangulos:
    def __init__(self):
        self.rectangulos = []
        self.usuario = None
        self.inicializar_datos()
    
    def inicializar_datos(self):
        """Crea una serie de rectángulos para la aplicación"""
        colores = ["rojo", "verde", "azul", "amarillo", "magenta", "cyan", "blanco", "naranja"]
        nombres = ["Cuadrado", "Alargado", "Compacto", "Panorámico", "Fino", "Grande", "Pequeño", "Mediano"]
        ubicaciones = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga", "Zaragoza", "Murcia"]
        
        intereses_posibles = [
            "matemáticas", "geometría", "simetría", "arte moderno", "arquitectura", 
            "diseño gráfico", "minimalismo", "origami", "pixelart", "fotografía"
        ]
        
        # Crear 10 rectángulos aleatorios
        for i in range(10):
            base = random.randint(3, 20)
            altura = random.randint(2, 10)
            color = random.choice(colores)
            nombre = f"{random.choice(nombres)}-{random.randint(100, 999)}"
            edad = random.randint(18, 45)
            
            # Seleccionar 2-4 intereses aleatorios
            num_intereses = random.randint(2, 4)
            intereses = random.sample(intereses_posibles, num_intereses)
            
            ubicacion = random.choice(ubicaciones)
            
            self.rectangulos.append(Rectangulo(base, altura, color, nombre, edad, intereses, ubicacion))
    
    def crear_usuario(self):
        """Permite al usuario crear su propio rectángulo"""
        limpiar_pantalla()
        print(f"{Fore.CYAN}{'═' * 50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}¡Bienvenido a TinderRectangulos!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}")
        print("\nVamos a crear tu perfil de rectángulo:\n")
        
        try:
            nombre = input("Nombre (Enter para aleatorio): ").strip()
            base = int(input("Base (1-20): ").strip())
            altura = int(input("Altura (1-10): ").strip())
            
            print("\nColores disponibles:")
            colores = ["rojo", "verde", "azul", "amarillo", "magenta", "cyan", "blanco", "naranja"]
            for i, color in enumerate(colores):
                color_map = {
                    "rojo": Fore.RED,
                    "verde": Fore.GREEN, 
                    "azul": Fore.BLUE,
                    "amarillo": Fore.YELLOW,
                    "magenta": Fore.MAGENTA,
                    "cyan": Fore.CYAN,
                    "blanco": Fore.WHITE,
                    "naranja": Fore.YELLOW + Style.BRIGHT
                }
                print(f"{color_map.get(color)}{i+1}. {color}")
            
            color_idx = int(input(f"\n{Style.RESET_ALL}Elige un color (1-{len(colores)}): ").strip())
            color = colores[color_idx - 1]
            
            edad = input("Edad (Enter para aleatorio): ").strip()
            edad = int(edad) if edad else random.randint(18, 45)
            
            ubicacion = input("Ubicación (Enter para aleatorio): ").strip()
            
            print("\nIntereses (separados por comas, Enter para aleatorios):")
            intereses_str = input().strip()
            if intereses_str:
                intereses = [interes.strip() for interes in intereses_str.split(",")]
            else:
                intereses = None
                
            self.usuario = Rectangulo(base, altura, color, nombre, edad, intereses, ubicacion)
            print(f"\n{Fore.GREEN}¡Perfil creado con éxito!")
            time.sleep(1)
            
        except (ValueError, IndexError) as e:
            print(f"\n{Fore.RED}Error: Entrada no válida. Creando perfil aleatorio.")
            self.usuario = Rectangulo(
                random.randint(3, 20),
                random.randint(2, 10),
                random.choice(colores)
            )
            time.sleep(2)
    
    def mostrar_menu(self):
        """Muestra el menú principal de la aplicación"""
        while True:
            limpiar_pantalla()
            print(f"{Fore.CYAN}{'═' * 50}")
            print(f"{Fore.CYAN}{Style.BRIGHT}TinderRectangulos - Menú Principal{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 50}")
            
            if self.usuario:
                print(f"\n{Fore.YELLOW}Hola, {self.usuario.nombre}!")
                print(f"Tienes {self.usuario.matches} matches y {self.usuario.likes_recibidos} likes.")
            
            print(f"\n{Fore.WHITE}1. Ver mi perfil")
            print("2. Explorar rectángulos")
            print("3. Ver mis matches")
            print("4. Editar mi perfil")
            print("5. Salir")
            
            opcion = input(f"\n{Fore.CYAN}Elige una opción: ")
            
            if opcion == "1":
                self.ver_mi_perfil()
            elif opcion == "2":
                self.explorar_rectangulos()
            elif opcion == "3":
                self.ver_matches()
            elif opcion == "4":
                self.editar_perfil()
            elif opcion == "5":
                print(f"\n{Fore.YELLOW}¡Gracias por usar TinderRectangulos!")
                time.sleep(1)
                break
            else:
                print(f"\n{Fore.RED}Opción no válida. Inténtalo de nuevo.")
                time.sleep(1)
    
    def ver_mi_perfil(self):
        """Muestra el perfil del usuario"""
        limpiar_pantalla()
        print(f"{Fore.CYAN}{'═' * 50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Mi Perfil{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}")
        
        if not self.usuario:
            print(f"\n{Fore.RED}No tienes un perfil creado.")
            input("\nPresiona Enter para continuar...")
            return
        
        self.usuario.mostrar_perfil()
        input("\nPresiona Enter para volver al menú...")
    
    def explorar_rectangulos(self):
        """Permite al usuario explorar otros rectángulos"""
        if not self.rectangulos:
            print(f"\n{Fore.RED}No hay rectángulos disponibles para explorar.")
            input("\nPresiona Enter para continuar...")
            return
        
        # Mezclar los rectángulos para mostrarlos en orden aleatorio
        random.shuffle(self.rectangulos)
        
        for rectangulo in self.rectangulos:
            limpiar_pantalla()
            print(f"{Fore.CYAN}{'═' * 50}")
            print(f"{Fore.CYAN}{Style.BRIGHT}Explorando Rectángulos{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 50}")
            
            # Mostrar compatibilidad basada en similitud de área/perímetro
            compatibilidad = self.calcular_compatibilidad(self.usuario, rectangulo)
            
            print(f"\n{Fore.YELLOW}Compatibilidad: {compatibilidad}%")
            
            rectangulo.mostrar_perfil()
            
            print(f"\n{Fore.CYAN}¿Qué quieres hacer?")
            print(f"{Fore.GREEN}1. Me gusta ❤")
            print(f"{Fore.RED}2. Siguiente ➡")
            print(f"{Fore.YELLOW}3. Volver al menú principal")
            
            opcion = input(f"\n{Fore.CYAN}Elige una opción: ")
            
            if opcion == "1":
                # Simular matching con 40% de probabilidad
                rectangulo.likes_recibidos += 1
                
                if random.random() < 0.4:
                    self.usuario.matches += 1
                    rectangulo.matches += 1
                    limpiar_pantalla()
                    print(f"\n{Fore.MAGENTA}{'═' * 50}")
                    print(f"{Fore.MAGENTA}{Style.BRIGHT}¡TIENES UN NUEVO MATCH!{Style.RESET_ALL}")
                    print(f"{Fore.MAGENTA}{'═' * 50}")
                    print(f"\n{Fore.YELLOW}¡Has hecho match con {rectangulo.nombre}!")
                    self.mostrar_animacion_match()
                    input("\nPresiona Enter para continuar...")
                else:
                    print(f"\n{Fore.GREEN}Le has dado like a {rectangulo.nombre}.")
                    time.sleep(1)
            elif opcion == "3":
                break
    
    def ver_matches(self):
        """Muestra los matches del usuario"""
        limpiar_pantalla()
        print(f"{Fore.CYAN}{'═' * 50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Mis Matches{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}")
        
        if not self.usuario or self.usuario.matches == 0:
            print(f"\n{Fore.YELLOW}No tienes matches todavía. ¡Sigue explorando!")
            input("\nPresiona Enter para continuar...")
            return
        
        # Seleccionar algunos rectángulos como matches
        matches = random.sample(self.rectangulos, min(self.usuario.matches, len(self.rectangulos)))
        
        for i, match in enumerate(matches):
            print(f"\n{Fore.MAGENTA}Match #{i+1}:")
            match.mostrar_perfil()
        
        input("\nPresiona Enter para volver al menú...")
    
    def editar_perfil(self):
        """Permite al usuario editar su perfil"""
        if not self.usuario:
            print(f"\n{Fore.RED}No tienes un perfil creado.")
            input("\nPresiona Enter para continuar...")
            return
            
        limpiar_pantalla()
        print(f"{Fore.CYAN}{'═' * 50}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Editar Perfil{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}")
        
        print("\nDeja en blanco para mantener el valor actual:")
        
        nombre = input(f"Nombre [{self.usuario.nombre}]: ").strip()
        if nombre:
            self.usuario.nombre = nombre
            
        try:
            base_str = input(f"Base [{self.usuario.base}]: ").strip()
            if base_str:
                self.usuario.base = int(base_str)
                
            altura_str = input(f"Altura [{self.usuario.altura}]: ").strip()
            if altura_str:
                self.usuario.altura = int(altura_str)
                
            print("\nColores disponibles:")
            colores = ["rojo", "verde", "azul", "amarillo", "magenta", "cyan", "blanco", "naranja"]
            for i, color in enumerate(colores):
                color_map = {
                    "rojo": Fore.RED,
                    "verde": Fore.GREEN, 
                    "azul": Fore.BLUE,
                    "amarillo": Fore.YELLOW,
                    "magenta": Fore.MAGENTA,
                    "cyan": Fore.CYAN,
                    "blanco": Fore.WHITE,
                    "naranja": Fore.YELLOW + Style.BRIGHT
                }
                print(f"{color_map.get(color)}{i+1}. {color}")
                
            color_idx_str = input(f"\n{Style.RESET_ALL}Elige un color (1-{len(colores)}) [actual: {self.usuario.color}]: ").strip()
            if color_idx_str:
                color_idx = int(color_idx_str)
                self.usuario.color = colores[color_idx - 1]
                
        except (ValueError, IndexError):
            print(f"\n{Fore.RED}Entrada no válida. Algunos campos no se han actualizado.")
            
        print(f"\n{Fore.GREEN}¡Perfil actualizado con éxito!")
        time.sleep(1)
    
    def calcular_compatibilidad(self, rect1, rect2):
        """Calcula la compatibilidad entre dos rectángulos"""
        # Similitud de área (0-40%)
        area1 = rect1.calcular_area()
        area2 = rect2.calcular_area()
        max_area = max(area1, area2)
        min_area = min(area1, area2)
        similitud_area = (min_area / max_area) * 40 if max_area > 0 else 0
        
        # Similitud de proporciones (0-30%)
        prop1 = rect1.base / rect1.altura if rect1.altura > 0 else 0
        prop2 = rect2.base / rect2.altura if rect2.altura > 0 else 0
        max_prop = max(prop1, prop2)
        min_prop = min(prop1, prop2)
        similitud_prop = (min_prop / max_prop) * 30 if max_prop > 0 else 0
        
        # Bonus por color (0 o 20%)
        bonus_color = 20 if rect1.color == rect2.color else 0
        
        # Bonus por intereses comunes (0-10%)
        intereses_comunes = set(rect1.intereses).intersection(set(rect2.intereses))
        bonus_intereses = len(intereses_comunes) * 3
        bonus_intereses = min(bonus_intereses, 10)  # Máximo 10%
        
        return int(similitud_area + similitud_prop + bonus_color + bonus_intereses)
    
    def mostrar_animacion_match(self):
        """Muestra una animación de match"""
        frames = [
            "  ❤   ❤  ",
            " ❤❤  ❤❤ ",
            "❤❤❤ ❤❤❤",
            " ❤MATCH❤ ",
            "❤❤❤ ❤❤❤",
            " ❤❤  ❤❤ ",
            "  ❤   ❤  ",
        ]
        
        for _ in range(3):  # Repetir 3 veces
            for frame in frames:
                print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{frame}")
                time.sleep(0.15)
                limpiar_pantalla()
                print(f"\n{Fore.MAGENTA}{'═' * 50}")
                print(f"{Fore.MAGENTA}{Style.BRIGHT}¡TIENES UN NUEVO MATCH!{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}{'═' * 50}")

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Función principal del programa"""
    limpiar_pantalla()
    
    # Mostrar logo de la aplicación
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("  ████████╗██╗███╗   ██╗██████╗ ███████╗██████╗   ")
    print("  ╚══██╔══╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗  ")
    print("     ██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝  ")
    print("     ██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗  ")
    print("     ██║   ██║██║ ╚████║██████╔╝███████╗██║  ██║  ")
    print("     ╚═╝   ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝  ")
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("     ██████╗ ███████╗ ██████╗████████╗ █████╗     ")
    print("     ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗    ")
    print("     ██████╔╝█████╗  ██║        ██║   ███████║    ")
    print("     ██╔══██╗██╔══╝  ██║        ██║   ██╔══██║    ")
    print("     ██║  ██║███████╗╚██████╗   ██║   ██║  ██║    ")
    print("     ╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝    ")
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}¡Donde los rectángulos encuentran el amor!{Style.RESET_ALL}")
    
    input("\nPresiona Enter para continuar...")
    
    app = TinderRectangulos()
    app.crear_usuario()
    app.mostrar_menu()

if __name__ == "__main__":
    main()