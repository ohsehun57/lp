import tkinter as tk
from tkinter import simpledialog, messagebox
from abc import ABC, abstractmethod
import time
import threading
import math

# --- Interfaces SOLID ---
class IHanoiSolver(ABC):
    """Interfaz para un solucionador de las Torres de Hanoi."""
    @abstractmethod
    def solve(self):
        """Inicia el proceso de resolución."""
        pass

class IMoveVisualizer(ABC):
    """Interfaz para visualizar los movimientos de los discos."""
    @abstractmethod
    def visualize_move(self, from_peg_index: int, to_peg_index: int, disk_size: int):
        """
        Visualiza un movimiento de disco de una torre a otra.
        Args:
            from_peg_index (int): Índice de la torre de origen (0, 1 o 2).
            to_peg_index (int): Índice de la torre de destino (0, 1 o 2).
            disk_size (int): El tamaño del disco que se mueve.
        """
        pass
    
    @abstractmethod
    def is_valid_move(self, from_peg_index: int, to_peg_index: int) -> bool:
        """
        Verifica si un movimiento manual de una torre a otra es válido según las reglas de Hanoi.
        Args:
            from_peg_index (int): Índice de la torre de origen.
            to_peg_index (int): Índice de la torre de destino.
        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        pass

# --- Lógica de resolución automática ---
class HanoiSolver(IHanoiSolver):
    """
    Resuelve el rompecabezas de las Torres de Hanoi de forma recursiva y notifica a un visualizador
    sobre cada movimiento.
    """
    def __init__(self, num_disks: int, visualizer: IMoveVisualizer):
        self.num_disks = num_disks
        self.visualizer = visualizer
        self.solving = False # Bandera para controlar el proceso de resolución automática

    def solve(self):
        """Inicia el proceso de resolución automática."""
        self.solving = True
        # _move(n, origen, destino, auxiliar)
        self._move(self.num_disks, 0, 2, 1) 
        self.solving = False
        # Notificar al visualizador que la resolución ha terminado
        if self.visualizer and hasattr(self.visualizer, '_auto_solve_finished'):
            self.visualizer._auto_solve_finished()

    def _move(self, n, from_peg, to_peg, aux_peg):
        """
        Función recursiva para resolver las Torres de Hanoi.
        Args:
            n (int): El número de discos a mover.
            from_peg (int): Índice de la torre de origen.
            to_peg (int): Índice de la torre de destino.
            aux_peg (int): Índice de la torre auxiliar.
        """
        if not self.solving:  # Permitir la cancelación del proceso de resolución
            return
        if n == 1:
            # Mover el disco más pequeño de origen a destino
            self.visualizer.visualize_move(from_peg, to_peg, n)
        else:
            # Mover n-1 discos de origen a la torre auxiliar
            self._move(n - 1, from_peg, aux_peg, to_peg)
            if self.solving: # Verificar de nuevo si la resolución no ha sido detenida
                # Mover el enésimo (más grande) disco de origen a destino
                self.visualizer.visualize_move(from_peg, to_peg, n)
            self._move(n - 1, aux_peg, to_peg, from_peg)

    def stop_solving(self):
        """Detiene el proceso de resolución automática."""
        self.solving = False

# --- Ventana de Detalles de Resolución ---
class ResolutionDetailsWindow:
    """
    Ventana separada para mostrar los detalles de la resolución de las Torres de Hanoi.
    """
    def __init__(self, master, num_disks: int):
        self.master = master
        self.num_disks = num_disks
        self.window = tk.Toplevel(master)
        self.window.title("Detalles de la Resolución")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing) # Manejar el cierre de la ventana

        self.start_time = None
        self.elapsed_time = 0
        self.running_timer = False

        self._setup_ui()
        self.update_optimal_moves(num_disks)

    def _setup_ui(self):
        """Configura los elementos de la interfaz de usuario de la ventana de detalles."""
        tk.Label(self.window, text="Número de Discos:", font=("Arial", 12, "bold")).pack(pady=5)
        self.disks_label = tk.Label(self.window, text=str(self.num_disks), font=("Arial", 12))
        self.disks_label.pack()

        tk.Label(self.window, text="Movimientos Actuales:", font=("Arial", 12, "bold")).pack(pady=5)
        self.moves_label = tk.Label(self.window, text="0", font=("Arial", 12))
        self.moves_label.pack()

        tk.Label(self.window, text="Movimientos Óptimos:", font=("Arial", 12, "bold")).pack(pady=5)
        self.optimal_moves_label = tk.Label(self.window, text="0", font=("Arial", 12))
        self.optimal_moves_label.pack()

        tk.Label(self.window, text="Tiempo Transcurrido:", font=("Arial", 12, "bold")).pack(pady=5)
        self.time_label = tk.Label(self.window, text="00:00:00", font=("Arial", 12))
        self.time_label.pack()

    def update_moves(self, count: int):
        """Actualiza el contador de movimientos."""
        self.moves_label.config(text=str(count))

    def update_optimal_moves(self, num_disks: int):
        """Actualiza los movimientos óptimos basados en el número de discos."""
        optimal = (2 ** num_disks) - 1
        self.optimal_moves_label.config(text=str(optimal))

    def start_timer(self):
        """Inicia el temporizador."""
        if not self.running_timer:
            self.start_time = time.time() - self.elapsed_time # Para reanudar correctamente
            self.running_timer = True
            self._update_timer()

    def stop_timer(self):
        """Detiene el temporizador."""
        self.running_timer = False

    def reset_timer(self):
        """Reinicia el temporizador."""
        self.stop_timer()
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00")

    def _update_timer(self):
        """Actualiza el tiempo transcurrido en la ventana."""
        if self.running_timer:
            self.elapsed_time = time.time() - self.start_time
            hours, rem = divmod(self.elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            self.time_label.config(text=time_str)
            self.window.after(1000, self._update_timer) # Actualizar cada segundo

    def _on_closing(self):
        """Maneja el evento de cierre de la ventana de detalles."""
        self.stop_timer()
        self.window.destroy()

# --- Visualizador principal con interactividad ---
class HanoiGame(IMoveVisualizer):
    """
    Un juego de Torres de Hanoi interactivo y automático basado en Tkinter.
    Permite arrastrar discos manualmente y visualizar la resolución automática.
    """
    DISK_HEIGHT = 20
    PEG_WIDTH = 10
    BASE_HEIGHT = 10
    PEG_Y_BOTTOM = 400
    PEG_Y_TOP = 200
    DISK_MIN_WIDTH = 30
    DISK_WIDTH_INCREMENT = 15
    ANIMATION_DELAY_MS = 10 # Retraso entre cada paso de la animación
    AUTO_SOLVE_STEP_DELAY_S = 0.3 # Retraso entre cada movimiento completo en auto-solve

    def __init__(self, num_disks: int, master: tk.Tk):
        self.num_disks = num_disks
        self.root = master
        self.root.title("Torres de Hanoi - Interactivo y Automático")
        self.root.geometry("700x550") # Altura aumentada para mejor diseño
        self.root.resizable(False, False) # Prevenir el redimensionamiento

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="#E0FFFF", bd=2, relief="groove")
        self.canvas.pack(pady=10)
        
        # Estado del juego:
        # self.pegs almacena los tamaños de los discos *lógicos* (enteros) en cada torre.
        # Ejemplo: [[3, 2, 1], [], []] significa que la torre 0 tiene los discos 3 (abajo), 2, 1 (arriba)
        self.pegs = [[], [], []] 
        
        # self.disk_objects almacena los IDs del canvas de Tkinter para cada disco.
        # Esta lista se indexa por el tamaño del disco (ej., self.disk_objects[0] es para el disco de tamaño 1, etc.)
        self.disk_objects = [None] * self.num_disks 
        
        # self.disk_widths almacena el ancho visual de cada disco basado en su tamaño.
        # Indexado por el tamaño del disco (ej., self.disk_widths[0] es para el disco de tamaño 1, etc.)
        self.disk_widths = [0] * self.num_disks
        
        self.moves_count = 0
        
        # Variables para movimiento manual (arrastrar y soltar)
        self.moving_disk_id = None # ID del canvas del disco que se está arrastrando
        self.orig_tower_index = None # Índice de la torre de la que se recogió el disco
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Variables para movimiento manual (clic para mover)
        self.selected_disk_id = None # ID del canvas del disco seleccionado
        self.selected_disk_size = None # Tamaño lógico del disco seleccionado
        self.selected_disk_orig_peg = None # Índice de la torre original del disco seleccionado

        # Configuración visual
        self.peg_x = [100, 300, 500] # Coordenadas X centrales para cada torre
        # Colores de discos más vibrantes
        self.disk_colors = ["#FF6347", "#4682B4", "#3CB371", "#9370DB", "#FFD700", "#FF69B4", "#00CED1", "#F4A460", "#DA70D6", "#8A2BE2"]
        
        # Solucionador automático
        self.solver = HanoiSolver(num_disks, self)
        self.auto_solving = False
        self.solver_thread = None # Para mantener la referencia al hilo de resolución

        # Ventana de detalles
        self.details_window = ResolutionDetailsWindow(self.root, self.num_disks)

        self._setup_ui()
        self._initialize_game()

        # Vincular el evento de clic en el canvas para soltar discos en modo clic-para-mover
        self.canvas.bind("<Button-1>", self._handle_canvas_click_or_disk_press)

    def _setup_ui(self):
        """Configura los elementos de la interfaz de usuario (botones, etiquetas)."""
        # Marco para controles
        control_frame = tk.Frame(self.root, pady=5, bg="#F0F0F0")
        control_frame.pack()
        
        # Botones
        tk.Button(control_frame, text="Resolver Automáticamente", 
                  command=self._auto_solve, bg="#A2D9CE", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3,
                  activebackground="#88C0B5").pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Reiniciar", 
                  command=self._reset_game, bg="#AED6F1", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3,
                  activebackground="#9AC1D9").pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Parar Resolución", 
                  command=self._stop_auto_solve, bg="#F1948A", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3,
                  activebackground="#D98075").pack(side=tk.LEFT, padx=10)
        
        # Etiqueta de contador de movimientos
        self.moves_label = tk.Label(self.root, text="Movimientos: 0", 
                                     font=("Arial", 14, "bold"), fg="#333333", bg="#F0F0F0")
        self.moves_label.pack(pady=5)
        
        # Etiqueta de estado
        self.status_label = tk.Label(self.root, text="Modo: Manual - Arrastra o haz clic en los discos", 
                                      font=("Arial", 12), fg="#555555", bg="#F0F0F0")
        self.status_label.pack(pady=2)

    def _initialize_game(self):
        """Reinicia e inicializa el estado del juego y dibuja la configuración inicial."""
        # Detener cualquier proceso de resolución automática en curso
        self._stop_auto_solve()
        self.details_window.stop_timer()
        self.details_window.reset_timer()

        # Limpiar discos existentes del canvas
        self.canvas.delete("disk") 
        self.canvas.delete("disk_text") # Eliminar etiquetas de texto en los discos

        # Reiniciar estado del juego
        self.pegs = [[], [], []]
        self.disk_objects = [None] * self.num_disks
        self.disk_widths = [0] * self.num_disks
        self.moves_count = 0
        self.moving_disk_id = None
        self.orig_tower_index = None
        self.selected_disk_id = None
        self.selected_disk_size = None
        self.selected_disk_orig_peg = None
        
        # Inicializar discos en la primera torre (estado lógico)
        # Los discos se almacenan del más grande (abajo) al más pequeño (arriba)
        for i in range(self.num_disks, 0, -1):
            self.pegs[0].append(i) # Añadir tamaño de disco a la primera torre
        
        self._draw_all_elements()
        self._create_and_place_disks_visually()
        self._update_moves_display()
        self._update_status_label("Modo: Manual - Arrastra o haz clic en los discos")
        self.details_window.start_timer() # Iniciar el temporizador al inicio del juego

    def _draw_all_elements(self):
        """Dibuja las torres y la base en el canvas."""
        self.canvas.delete("peg") # Limpiar torres existentes
        self.canvas.delete("base") # Limpiar bases existentes
        self.canvas.delete("peg_label") # Limpiar etiquetas de torre existentes
        
        # Dibujar base del juego
        self.canvas.create_rectangle(50, self.PEG_Y_BOTTOM, 550, self.PEG_Y_BOTTOM + self.BASE_HEIGHT, 
                                     fill="#8B4513", outline="#5A2C0A", width=2, tags="base") # Marrón oscuro

        # Dibujar torres
        for i in range(3):
            x = self.peg_x[i]
            # Torre (línea vertical)
            self.canvas.create_rectangle(x - self.PEG_WIDTH // 2, self.PEG_Y_TOP, 
                                         x + self.PEG_WIDTH // 2, self.PEG_Y_BOTTOM, 
                                         fill="#36454F", outline="#2C3E50", width=2, tags="peg") # Gris oscuro
            # Etiqueta de la torre
            labels = ["A", "B", "C"]
            self.canvas.create_text(x, self.PEG_Y_TOP - 20, text=labels[i], 
                                     font=("Arial", 16, "bold"), fill="#333333", tags="peg_label")

    def _create_and_place_disks_visually(self):
        """
        Crea los objetos visuales de los discos en el canvas basándose en el estado lógico actual
        en self.pegs. Esto se llama durante la inicialización y el reinicio.
        """
        # Limpiar elementos visuales de discos anteriores
        self.canvas.delete("disk")
        self.canvas.delete("disk_text")

        # Iterar a través de cada torre y sus discos (de abajo hacia arriba)
        for peg_index, disks_on_peg in enumerate(self.pegs):
            for i, disk_size in enumerate(disks_on_peg):
                # Calcular el ancho del disco según su tamaño
                disk_width = self.DISK_MIN_WIDTH + (disk_size - 1) * self.DISK_WIDTH_INCREMENT 
                
                # Calcular la posición en el canvas
                x_center = self.peg_x[peg_index]
                # La posición Y se calcula desde la parte inferior de la torre, apilando hacia arriba
                y_bottom = self.PEG_Y_BOTTOM - i * self.DISK_HEIGHT 
                
                # Crear el rectángulo para el disco con bordes redondeados y un efecto de relieve
                disk_id = self.canvas.create_rectangle(
                    x_center - disk_width // 2, y_bottom - self.DISK_HEIGHT,
                    x_center + disk_width // 2, y_bottom,
                    fill=self.disk_colors[(disk_size - 1) % len(self.disk_colors)],
                    outline="black", width=2, tags="disk",
                    stipple="gray50" # Efecto de relieve
                )
                
                # Crear texto para el disco (su tamaño)
                text_id = self.canvas.create_text(x_center, y_bottom - self.DISK_HEIGHT // 2, 
                                                   text=str(disk_size), fill="white", 
                                                   font=("Arial", 10, "bold"), tags=f"disk_text_for_{disk_id}")
                
                # Almacenar el ID del canvas y el ancho para uso posterior
                self.disk_objects[disk_size - 1] = disk_id # Almacenar por tamaño de disco (índice 0)
                self.disk_widths[disk_size - 1] = disk_width # Almacenar por tamaño de disco (índice 0)
        
        # Vincular eventos para la interactividad manual con todos los discos
        # El evento principal se vincula al canvas en __init__ para manejar clics generales y arrastres
        # específicos de discos.

    def _get_tower_index_from_x(self, x_coord: int) -> int:
        """
        Determina a qué índice de torre (0, 1 o 2) corresponde una coordenada X dada.
        Args:
            x_coord (int): La coordenada X en el canvas.
        Returns:
            int: El índice de la torre (0, 1 o 2).
        """
        # Calcular el centro de cada zona de torre
        if x_coord < (self.peg_x[0] + self.peg_x[1]) / 2:
            return 0
        elif x_coord < (self.peg_x[1] + self.peg_x[2]) / 2:
            return 1
        else:
            return 2

    def _handle_canvas_click_or_disk_press(self, event):
        """
        Maneja el evento de presionar el botón del ratón en el canvas.
        Diferencia entre un clic en un disco (para seleccionar/arrastrar)
        o un clic en el canvas (para soltar un disco seleccionado).
        """
        if self.auto_solving: # Prevenir movimientos manuales durante la resolución automática
            return

        clicked_items = self.canvas.find_withtag("current")
        if clicked_items and "disk" in self.canvas.gettags(clicked_items[0]):
            # Se hizo clic en un disco
            clicked_disk_id = clicked_items[0]
            disk_size = self._get_disk_size_from_id(clicked_disk_id)

            # Si ya hay un disco seleccionado (modo clic para mover)
            if self.selected_disk_id is not None:
                # Si se hace clic en el mismo disco seleccionado, deseleccionarlo y devolverlo
                if clicked_disk_id == self.selected_disk_id:
                    self._deselect_disk(return_to_orig=True)
                else:
                    # Intentar soltar el disco seleccionado en la torre del disco clicado
                    target_peg_index = self._get_tower_index_from_x(event.x)
                    self._try_move_selected_disk(target_peg_index)
            else:
                # No hay disco seleccionado, intentar seleccionar o iniciar arrastre
                current_peg_index = -1
                for peg_idx in range(3):
                    if self.pegs[peg_idx] and self.disk_objects[self.pegs[peg_idx][-1] - 1] == clicked_disk_id:
                        current_peg_index = peg_idx
                        break
                
                if current_peg_index == -1: # Esto no debería ocurrir si el disco está en una torre
                    return

                # Verificar si es el disco superior de la torre
                if self.pegs[current_peg_index] and self.pegs[current_peg_index][-1] == disk_size:
                    # Es el disco superior, ahora decidir si es arrastre o clic
                    self.moving_disk_id = clicked_disk_id
                    self.orig_tower_index = current_peg_index
                    
                    # Vincular temporalmente los eventos de arrastre
                    self.canvas.bind("<B1-Motion>", self._drag_disk)
                    self.canvas.bind("<ButtonRelease-1>", self._end_drag)

                    # Calcular offset para el arrastre
                    x1, y1, x2, y2 = self.canvas.coords(clicked_disk_id)
                    self.drag_offset_x = event.x - (x1 + x2) / 2
                    self.drag_offset_y = event.y - (y1 + y2) / 2
                    
                    # Traer el disco al frente visualmente
                    self.canvas.tag_raise(self.moving_disk_id)
                    self.canvas.tag_raise(f"disk_text_for_{self.moving_disk_id}")

                    # Iniciar un temporizador para decidir si es un clic o un arrastre
                    # Si el ratón se mueve significativamente antes de este tiempo, es arrastre.
                    # Si no, al soltar el botón, se considera un clic.
                    self.click_timer_id = self.root.after(200, lambda: self._set_as_drag_mode())
                else:
                    messagebox.showerror("Movimiento Inválido", "Solo puedes mover el disco superior de una torre.")
        else:
            # Se hizo clic en el canvas (no en un disco)
            if self.selected_disk_id is not None:
                # Si hay un disco seleccionado, intentar soltarlo en la torre del clic
                target_peg_index = self._get_tower_index_from_x(event.x)
                self._try_move_selected_disk(target_peg_index)

    def _set_as_drag_mode(self):
        """Se activa si el temporizador de clic expira sin un movimiento significativo, indicando arrastre."""
        # Si el temporizador expira, significa que el usuario mantuvo presionado el botón,
        # por lo que el modo principal es arrastre.
        # En este punto, ya se han vinculado los eventos de arrastre en _handle_canvas_click_or_disk_press.
        # No se necesita hacer nada más aquí, ya está en modo arrastre.
        pass

    def _drag_disk(self, event):
        """Maneja el movimiento de arrastre de un disco."""
        if self.moving_disk_id and not self.auto_solving:
            # Cancelar el temporizador de clic si el arrastre comienza
            if hasattr(self, 'click_timer_id') and self.click_timer_id is not None:
                self.root.after_cancel(self.click_timer_id)
                self.click_timer_id = None

            disk_size = self._get_disk_size_from_id(self.moving_disk_id)
            disk_width = self.disk_widths[disk_size - 1]
            
            # Actualizar la posición del disco en el canvas
            self.canvas.coords(self.moving_disk_id, 
                               event.x - disk_width // 2, event.y - self.DISK_HEIGHT // 2,
                               event.x + disk_width // 2, event.y + self.DISK_HEIGHT // 2)
            
            # Mover también la etiqueta de texto junto con el disco
            text_id_tag = f"disk_text_for_{self.moving_disk_id}"
            text_id = self.canvas.find_withtag(text_id_tag)
            if text_id:
                self.canvas.coords(text_id[0], event.x, event.y)

    def _end_drag(self, event):
        """
        Maneja la liberación de un disco después de arrastrarlo. Valida el movimiento
        y actualiza el estado del juego y los elementos visuales.
        """
        # Desvincular los eventos de arrastre
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        # Si el temporizador de clic aún está activo, significa que fue un clic, no un arrastre
        if hasattr(self, 'click_timer_id') and self.click_timer_id is not None:
            self.root.after_cancel(self.click_timer_id)
            self.click_timer_id = None
            self._handle_disk_click_for_selection(event) # Llamar al manejador de clic
            self.moving_disk_id = None # Asegurarse de que no esté en estado de arrastre
            self.orig_tower_index = None
            return

        if not self.moving_disk_id or self.auto_solving:
            return
        
        dest_tower_index = self._get_tower_index_from_x(event.x)
        
        # Obtener el tamaño lógico del disco que se está moviendo
        moving_disk_size = self._get_disk_size_from_id(self.moving_disk_id)

        # Verificar si el movimiento es válido usando el estado lógico del juego
        is_valid_drag_start = (self.pegs[self.orig_tower_index] and 
                               self.pegs[self.orig_tower_index][-1] == moving_disk_size)

        if is_valid_drag_start and self.is_valid_move(self.orig_tower_index, dest_tower_index):
            # Realizar el movimiento lógico
            self.pegs[self.orig_tower_index].pop() # Eliminar del origen
            self.pegs[dest_tower_index].append(moving_disk_size) # Añadir al destino
            
            # Actualizar contador de movimientos
            self.moves_count += 1
            self._update_moves_display()
            
            # Reposicionar visualmente el disco en su posición apilada final
            self._reposition_disk_visually(self.moving_disk_id, dest_tower_index)
            
            self._check_victory()
        else:
            # Movimiento inválido, devolver visualmente el disco a su torre original
            messagebox.showerror("Movimiento Inválido", "No puedes colocar un disco más grande sobre uno más pequeño o mover un disco no superior.")
            # Asegurarse de que el disco esté de vuelta en su torre lógica si se sacó temporalmente.
            # En la lógica actual, el pop solo ocurre si el movimiento es válido.
            # Si es inválido, el disco nunca se sacó lógicamente, solo se movió visualmente.
            # Por lo tanto, solo necesitamos reposicionarlo visualmente.
            self._reposition_disk_visually(self.moving_disk_id, self.orig_tower_index)

        # Reiniciar estado de movimiento
        self.moving_disk_id = None
        self.orig_tower_index = None

    def _handle_disk_click_for_selection(self, event):
        """
        Maneja un clic en un disco para el modo "clic para mover".
        Selecciona un disco o intenta mover un disco seleccionado.
        """
        clicked_disk_id = self.canvas.find_withtag("current")[0]
        disk_size = self._get_disk_size_from_id(clicked_disk_id)

        # Si no hay disco seleccionado
        if self.selected_disk_id is None:
            current_peg_index = -1
            for peg_idx in range(3):
                if self.pegs[peg_idx] and self.disk_objects[self.pegs[peg_idx][-1] - 1] == clicked_disk_id:
                    current_peg_index = peg_idx
                    break
            
            if current_peg_index == -1: # No debería ocurrir
                return

            # Verificar si es el disco superior de la torre
            if self.pegs[current_peg_index] and self.pegs[current_peg_index][-1] == disk_size:
                self.selected_disk_id = clicked_disk_id
                self.selected_disk_size = disk_size
                self.selected_disk_orig_peg = current_peg_index
                
                # Resaltar visualmente el disco seleccionado
                self.canvas.itemconfig(self.selected_disk_id, outline="blue", width=3)
                
                # Eliminar lógicamente el disco de su torre temporalmente
                self.pegs[self.selected_disk_orig_peg].pop()
                self._update_status_label(f"Modo: Manual - Disco {disk_size} seleccionado. Haz clic en una torre para soltar.")
            else:
                messagebox.showerror("Movimiento Inválido", "Solo puedes seleccionar el disco superior de una torre.")
        else:
            # Ya hay un disco seleccionado, intentar soltarlo
            # Determinar la torre de destino (la torre del disco clicado)
            target_peg_index = -1
            for peg_idx in range(3):
                if self.pegs[peg_idx] and self.disk_objects[self.pegs[peg_idx][-1] - 1] == clicked_disk_id:
                    target_peg_index = peg_idx
                    break
            
            # Si se hizo clic en un disco que NO es el seleccionado, intentar mover a esa torre
            if target_peg_index != -1:
                self._try_move_selected_disk(target_peg_index)
            else:
                # Esto significa que se hizo clic en un área vacía del canvas o en un peg sin discos
                # Ya se maneja en _handle_canvas_click_or_disk_press si el clic no fue en un disco.
                pass 

    def _try_move_selected_disk(self, target_peg_index: int):
        """
        Intenta mover el disco actualmente seleccionado a la torre de destino.
        """
        if self.selected_disk_id is None:
            return # No hay disco seleccionado para mover

        moving_disk_size = self.selected_disk_size
        
        if self.is_valid_move(self.selected_disk_orig_peg, target_peg_index):
            # Realizar el movimiento lógico
            # El disco ya fue "popped" lógicamente en _handle_disk_click_for_selection
            self.pegs[target_peg_index].append(moving_disk_size) # Añadir al destino
            
            self.moves_count += 1
            self._update_moves_display()
            
            # Reposicionar visualmente el disco
            self._reposition_disk_visually(self.selected_disk_id, target_peg_index)
            
            self._deselect_disk() # Deseleccionar el disco después de un movimiento exitoso
            self._check_victory()
        else:
            messagebox.showerror("Movimiento Inválido", "No puedes colocar un disco más grande sobre uno más pequeño.")
            self._deselect_disk(return_to_orig=True) # Deseleccionar y devolver al origen

    def _deselect_disk(self, return_to_orig: bool = False):
        """
        Deselecciona el disco actual, opcionalmente devolviéndolo a su torre original.
        Args:
            return_to_orig (bool): Si es True, el disco se devuelve a su torre original
                                   lógica y visualmente.
        """
        if self.selected_disk_id:
            # Restablecer el contorno visual del disco
            self.canvas.itemconfig(self.selected_disk_id, outline="black", width=2)
            
            if return_to_orig:
                # Si se debe devolver al origen, reinsertar lógicamente
                if self.selected_disk_size not in self.pegs[self.selected_disk_orig_peg]:
                    self.pegs[self.selected_disk_orig_peg].append(self.selected_disk_size)
                    self.pegs[self.selected_disk_orig_peg].sort(reverse=True) # Mantener orden
                self._reposition_disk_visually(self.selected_disk_id, self.selected_disk_orig_peg)
            
            # Reiniciar variables de estado de selección
            self.selected_disk_id = None
            self.selected_disk_size = None
            self.selected_disk_orig_peg = None
            self._update_status_label("Modo: Manual - Arrastra o haz clic en los discos")

    def _get_disk_size_from_id(self, disk_id: int) -> int:
        """
        Recupera el tamaño lógico del disco a partir de su ID de canvas.
        Args:
            disk_id (int): El ID del canvas del disco.
        Returns:
            int: El tamaño lógico del disco (1 a num_disks).
        """
        for size in range(1, self.num_disks + 1):
            if self.disk_objects[size - 1] == disk_id:
                return size
        return 0 # No debería ocurrir

    def _reposition_disk_visually(self, disk_id: int, target_peg_index: int):
        """
        Reposiciona un disco en el canvas a su posición apilada correcta en una torre.
        Args:
            disk_id (int): El ID del canvas del disco a reposicionar.
            target_peg_index (int): El índice de la torre donde se debe colocar el disco.
        """
        disk_size = self._get_disk_size_from_id(disk_id)
        disk_width = self.disk_widths[disk_size - 1]
        
        # Calcular la posición Y basándose en el número de discos ya en la torre de destino
        # El disco se colocará encima de los discos existentes
        # Se resta 1 porque el disco que se está moviendo ya está lógicamente en la pila
        num_disks_on_target_peg_logical = len(self.pegs[target_peg_index])
        
        x_dest = self.peg_x[target_peg_index]
        y_bottom = self.PEG_Y_BOTTOM - (num_disks_on_target_peg_logical - 1) * self.DISK_HEIGHT 

        # Obtener las coordenadas actuales del disco
        current_coords = self.canvas.coords(disk_id)
        if not current_coords: # Si el disco no existe en el canvas, salir
            return

        current_x, current_y = (current_coords[0] + current_coords[2]) / 2, (current_coords[1] + current_coords[3]) / 2
        
        # Coordenadas objetivo
        target_x = x_dest
        target_y = y_bottom - self.DISK_HEIGHT / 2

        # Animar el movimiento
        self._animate_disk_movement(disk_id, current_x, current_y, target_x, target_y)

    def _animate_disk_movement(self, disk_id, start_x, start_y, end_x, end_y):
        """
        Realiza una animación suave del movimiento de un disco.
        """
        # Mover la etiqueta de texto junto con el disco
        text_id_tag = f"disk_text_for_{disk_id}"
        text_id = self.canvas.find_withtag(text_id_tag)
        text_obj_id = text_id[0] if text_id else None

        steps = 20
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        for i in range(steps + 1):
            current_x = start_x + i * dx
            current_y = start_y + i * dy
            
            disk_width = self.disk_widths[self._get_disk_size_from_id(disk_id) - 1]
            self.canvas.coords(disk_id, 
                               current_x - disk_width // 2, current_y - self.DISK_HEIGHT // 2,
                               current_x + disk_width // 2, current_y + self.DISK_HEIGHT // 2)
            if text_obj_id:
                self.canvas.coords(text_obj_id, current_x, current_y)
            
            self.root.update_idletasks()
            time.sleep(self.ANIMATION_DELAY_MS / 1000.0) # Pausa para la animación

    def is_valid_move(self, from_peg_index: int, to_peg_index: int) -> bool:
        """
        Verifica si un movimiento de from_peg_index a to_peg_index es válido
        según las reglas de las Torres de Hanoi. Esto usa el estado lógico (self.pegs).
        Args:
            from_peg_index (int): Índice de la torre de origen.
            to_peg_index (int): Índice de la torre de destino.
        Returns:
            bool: True si el movimiento es válido, False en caso contrario.
        """
        # No se puede mover de una torre vacía
        if not self.pegs[from_peg_index]:
            return False

        moving_disk_logical_size = self.pegs[from_peg_index][-1]
        
        # Si la torre de destino está vacía, cualquier disco puede colocarse
        if not self.pegs[to_peg_index]: 
            return True 
        
        # Si no, verificar si el disco superior en la torre de destino es más grande
        top_disk_on_dest_size = self.pegs[to_peg_index][-1]
        
        # Un disco más pequeño puede colocarse sobre uno más grande
        return moving_disk_logical_size < top_disk_on_dest_size

    def visualize_move(self, from_peg_index: int, to_peg_index: int, disk_size: int):
        """
        Visualiza un solo movimiento durante la resolución automática.
        Este método es llamado por HanoiSolver.
        Args:
            from_peg_index (int): Índice de la torre de origen.
            to_peg_index (int): Índice de la torre de destino.
            disk_size (int): El tamaño lógico del disco que se mueve.
        """
        if not self.auto_solving: # Solo visualizar si la resolución automática está activa
            return

        # Realizar el movimiento lógico primero
        # Asegurarse de que el disco que se mueve es realmente el disco superior en la torre de origen
        if self.pegs[from_peg_index] and self.pegs[from_peg_index][-1] == disk_size:
            self.pegs[from_peg_index].pop()
            self.pegs[to_peg_index].append(disk_size)
        else:
            print(f"Advertencia: Se intentó visualizar un movimiento lógico inválido para el disco {disk_size} de {from_peg_index} a {to_peg_index}")
            return

        # Obtener el ID del canvas del disco que se movió lógicamente
        moving_disk_id = self.disk_objects[disk_size - 1]
        
        # Actualizar la posición visual en el canvas con animación
        self._reposition_disk_visually(moving_disk_id, to_peg_index)
        
        self.moves_count += 1
        self._update_moves_display()
        
        self.root.update_idletasks() # Actualizar el canvas inmediatamente
        time.sleep(self.AUTO_SOLVE_STEP_DELAY_S) # Pausa para el efecto de visualización

    def _auto_solve(self):
        """Inicia el proceso de resolución automática en un hilo separado."""
        if self.auto_solving:
            return
        
        # Reiniciar el juego si no está en el estado inicial, o si los discos no están todos en la torre A
        if not (len(self.pegs[0]) == self.num_disks and not self.pegs[1] and not self.pegs[2]):
            self._reset_game() # Reiniciar para asegurar que los discos estén en la torre inicial
            # Dar un pequeño tiempo para que el reinicio se complete visualmente
            self.root.update_idletasks()
            time.sleep(0.1)

        self.auto_solving = True
        self._update_status_label("Modo: Automático - Resolviendo...")
        self.details_window.reset_timer()
        self.details_window.start_timer()

        # Iniciar el solucionador en un hilo separado
        self.solver_thread = threading.Thread(target=self.solver.solve)
        self.solver_thread.start()

    def _stop_auto_solve(self):
        """Detiene el proceso de resolución automática."""
        if self.auto_solving:
            self.solver.stop_solving()
            self.auto_solving = False
            self._update_status_label("Modo: Manual - Resolución detenida.")
            self.details_window.stop_timer()

    def _auto_solve_finished(self):
        """Callback llamado cuando la resolución automática ha terminado."""
        self.auto_solving = False
        self.details_window.stop_timer()
        self.root.after(100, self._check_victory) # Verificar victoria después de un pequeño retraso para asegurar que todos los movimientos se han procesado

    def _reset_game(self):
        """Reinicia el juego a su estado inicial."""
        self._initialize_game()
        messagebox.showinfo("Juego Reiniciado", "El juego ha sido reiniciado.")

    def _update_moves_display(self):
        """Actualiza la etiqueta del contador de movimientos y la ventana de detalles."""
        self.moves_label.config(text=f"Movimientos: {self.moves_count}")
        self.details_window.update_moves(self.moves_count)

    def _update_status_label(self, message: str):
        """Actualiza la etiqueta de estado con un mensaje."""
        self.status_label.config(text=message)

    def _check_victory(self):
        """Verifica si el juego ha sido ganado (todos los discos en la torre final)."""
        if len(self.pegs[2]) == self.num_disks:
            self.details_window.stop_timer()
            messagebox.showinfo("¡Felicidades!", 
                                f"¡Has resuelto las Torres de Hanoi en {self.moves_count} movimientos!\n"
                                f"Movimientos óptimos: {(2**self.num_disks) - 1}")
            self._update_status_label("¡Juego Terminado! Ganaste.")

# --- Función principal para iniciar el juego ---
def main():
    root = tk.Tk()
    
    # Solicitar el número de discos al usuario
    while True:
        try:
            num_disks = simpledialog.askinteger("Configuración del Juego", 
                                                "Introduce el número de discos (3-10):",
                                                parent=root,
                                                minvalue=3, maxvalue=10)
            if num_disks is None: # El usuario canceló
                root.destroy()
                return
            break
        except Exception:
            messagebox.showerror("Entrada Inválida", "Por favor, introduce un número válido.")

    game = HanoiGame(num_disks, root)
    root.mainloop()

if __name__ == "__main__":
    main()