import tkinter as tk
from tkinter import simpledialog, messagebox
from abc import ABC, abstractmethod
import time
import threading

# Interfaces SOLID
class IHanoiSolver(ABC):
    """Interface for a Hanoi Tower solver."""
    @abstractmethod
    def solve(self):
        """Initiates the solving process."""
        pass

class IMoveVisualizer(ABC):
    """Interface for visualizing disk movements."""
    @abstractmethod
    def visualize_move(self, from_peg_index: int, to_peg_index: int, disk_size: int):
        """
        Visualizes a disk move from one peg to another.
        Args:
            from_peg_index (int): Index of the source peg (0, 1, or 2).
            to_peg_index (int): Index of the destination peg (0, 1, or 2).
            disk_size (int): The size of the disk being moved.
        """
        pass
    
    @abstractmethod
    def is_valid_move(self, from_peg_index: int, to_peg_index: int) -> bool:
        """
        Checks if a manual move from one peg to another is valid according to Hanoi rules.
        Args:
            from_peg_index (int): Index of the source peg.
            to_peg_index (int): Index of the destination peg.
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        pass

# Lógica de resolución automática
class HanoiSolver(IHanoiSolver):
    """
    Solves the Towers of Hanoi puzzle recursively and notifies a visualizer
    about each move.
    """
    def __init__(self, num_disks: int, visualizer: IMoveVisualizer):
        self.num_disks = num_disks
        self.visualizer = visualizer
        self.solving = False # Flag to control automatic solving process

    def solve(self):
        """Starts the automatic solving process."""
        self.solving = True
        # _move(n, source, destination, auxiliary)
        self._move(self.num_disks, 0, 2, 1) 
        self.solving = False

    def _move(self, n, from_peg, to_peg, aux_peg):
        """
        Recursive function to solve the Towers of Hanoi.
        Args:
            n (int): The number of disks to move.
            from_peg (int): Index of the source peg.
            to_peg (int): Index of the destination peg.
            aux_peg (int): Index of the auxiliary peg.
        """
        if not self.solving:  # Allow cancellation of the solving process
            return
        if n == 1:
            # Move the smallest disk from source to destination
            self.visualizer.visualize_move(from_peg, to_peg, n)
        else:
            # Move n-1 disks from source to auxiliary peg
            self._move(n - 1, from_peg, aux_peg, to_peg)
            if self.solving:
                # Move the nth (largest) disk from source to destination
                self.visualizer.visualize_move(from_peg, to_peg, n)
            # Move n-1 disks from auxiliary to destination peg
            self._move(n - 1, aux_peg, to_peg, from_peg)

    def stop_solving(self):
        """Stops the automatic solving process."""
        self.solving = False

# Visualizador principal con interactividad
class HanoiGame(IMoveVisualizer):
    """
    A Tkinter-based interactive and automatic Towers of Hanoi game.
    Allows manual dragging of disks and automatic solving visualization.
    """
    def __init__(self, num_disks: int):
        self.num_disks = num_disks
        self.root = tk.Tk()
        self.root.title("Torres de Hanoi - Interactivo y Automático")
        self.root.geometry("700x550") # Increased height for better layout
        self.root.resizable(False, False) # Prevent resizing

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="lightgray", bd=2, relief="groove")
        self.canvas.pack(pady=10)
        
        # Game state:
        # self.pegs stores the *logical* disk sizes (integers) on each peg.
        # Example: [[3, 2, 1], [], []] means peg 0 has disks 3 (bottom), 2, 1 (top)
        self.pegs = [[], [], []] 
        
        # self.disk_objects stores the Tkinter canvas IDs for each disk.
        # This list is indexed by disk size (e.g., self.disk_objects[0] is for disk size 1, etc.)
        self.disk_objects = [None] * self.num_disks 
        
        # self.disk_widths stores the visual width of each disk based on its size.
        # Indexed by disk size (e.g., self.disk_widths[0] is for disk size 1, etc.)
        self.disk_widths = [0] * self.num_disks
        
        self.moves_count = 0
        
        # Variables for manual movement
        self.moving_disk_id = None # Canvas ID of the disk being dragged
        self.orig_tower_index = None # Index of the tower from which the disk was picked up
        
        # Visual configuration
        self.peg_x = [100, 300, 500] # X-coordinates for the center of each peg
        self.peg_width = 10
        self.peg_height = 200
        self.disk_height = 20
        self.disk_colors = ["#FF6347", "#4682B4", "#3CB371", "#9370DB", "#FFD700", "#FF69B4", "#00CED1", "#F4A460"]
        
        # Automatic solver
        self.solver = HanoiSolver(num_disks, self)
        self.auto_solving = False
        self.solver_thread = None # To hold the reference to the solving thread

        self._setup_ui()
        self._initialize_game()

    def _setup_ui(self):
        """Sets up the user interface elements (buttons, labels)."""
        # Frame for controls
        control_frame = tk.Frame(self.root, pady=5)
        control_frame.pack()
        
        # Buttons
        tk.Button(control_frame, text="Resolver Automáticamente", 
                  command=self._auto_solve, bg="#A2D9CE", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Reiniciar", 
                  command=self._reset_game, bg="#AED6F1", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Parar Resolución", 
                  command=self._stop_auto_solve, bg="#F1948A", fg="black", 
                  font=("Arial", 10, "bold"), relief="raised", bd=3).pack(side=tk.LEFT, padx=10)
        
        # Moves count label
        self.moves_label = tk.Label(self.root, text="Movimientos: 0", 
                                     font=("Arial", 14, "bold"), fg="#333333")
        self.moves_label.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Modo: Manual - Arrastra los discos", 
                                      font=("Arial", 12), fg="#555555")
        self.status_label.pack(pady=2)

    def _initialize_game(self):
        """Resets and initializes the game state and draws the initial setup."""
        # Stop any ongoing auto-solving process
        self._stop_auto_solve()

        # Clear existing disks from canvas
        self.canvas.delete("disk") 
        self.canvas.delete("disk_text") # Delete text labels on disks

        # Reset game state
        self.pegs = [[], [], []]
        self.disk_objects = [None] * self.num_disks
        self.disk_widths = [0] * self.num_disks
        self.moves_count = 0
        self.moving_disk_id = None
        self.orig_tower_index = None
        
        # Initialize disks on the first peg (logical state)
        # Disks are stored from largest (bottom) to smallest (top)
        for i in range(self.num_disks, 0, -1):
            self.pegs[0].append(i) # Add disk size to the first peg
        
        self._draw_all_elements()
        self._create_and_place_disks_visually()
        self._update_moves_display()
        self._update_status_label("Modo: Manual - Arrastra los discos")

    def _draw_all_elements(self):
        """Draws the pegs and base on the canvas."""
        self.canvas.delete("peg") # Clear existing pegs
        self.canvas.delete("base") # Clear existing bases
        self.canvas.delete("peg_label") # Clear existing peg labels
        
        # Draw pegs
        for i in range(3):
            x = self.peg_x[i]
            # Peg (vertical line)
            self.canvas.create_rectangle(x - self.peg_width // 2, 200, 
                                         x + self.peg_width // 2, 400, 
                                         fill="black", outline="black", tags="peg")
            # Base
            self.canvas.create_rectangle(x - 60, 400, x + 60, 410, 
                                         fill="brown", outline="black", tags="base")
            # Peg label
            labels = ["A", "B", "C"]
            self.canvas.create_text(x, 180, text=labels[i], 
                                    font=("Arial", 16, "bold"), fill="#333333", tags="peg_label")

    def _create_and_place_disks_visually(self):
        """
        Creates the visual disk objects on the canvas based on the current
        logical state in self.pegs. This is called during initialization.
        """
        # Clear previous visual disk elements
        self.canvas.delete("disk")
        self.canvas.delete("disk_text")

        # Iterate through each peg and its disks (from bottom to top)
        for peg_index, disks_on_peg in enumerate(self.pegs):
            for i, disk_size in enumerate(disks_on_peg):
                # Calculate disk width based on its size
                disk_width = 30 + (disk_size - 1) * 15 
                
                # Calculate position on the canvas
                x_center = self.peg_x[peg_index]
                # Y position is calculated from the bottom of the peg, stacking upwards
                y_bottom = 400 - i * self.disk_height 
                
                # Create the rectangle for the disk
                disk_id = self.canvas.create_rectangle(
                    x_center - disk_width // 2, y_bottom - self.disk_height,
                    x_center + disk_width // 2, y_bottom,
                    fill=self.disk_colors[(disk_size - 1) % len(self.disk_colors)],
                    outline="black", width=2, tags="disk"
                )
                
                # Create text for the disk (its size)
                self.canvas.create_text(x_center, y_bottom - self.disk_height // 2, 
                                        text=str(disk_size), fill="white", 
                                        font=("Arial", 10, "bold"), tags="disk_text")
                
                # Store the canvas ID and width for later use
                self.disk_objects[disk_size - 1] = disk_id # Store by disk size (0-indexed)
                self.disk_widths[disk_size - 1] = disk_width # Store by disk size (0-indexed)
        
        # Bind events for manual interaction with all disks
        self.canvas.tag_bind("disk", "<Button-1>", self._start_move)
        self.canvas.tag_bind("disk", "<B1-Motion>", self._drag_disk)
        self.canvas.tag_bind("disk", "<ButtonRelease-1>", self._end_move)

    def _get_tower_index_from_x(self, x_coord: int) -> int:
        """
        Determines which peg index (0, 1, or 2) a given X-coordinate falls into.
        Args:
            x_coord (int): The X-coordinate on the canvas.
        Returns:
            int: The index of the peg (0, 1, or 2).
        """
        if x_coord < (self.peg_x[0] + self.peg_x[1]) / 2:
            return 0
        elif x_coord < (self.peg_x[1] + self.peg_x[2]) / 2:
            return 1
        else:
            return 2

    def _start_move(self, event):
        """
        Handles the start of a manual disk drag.
        Only allows dragging the top disk of a peg.
        """
        if self.auto_solving: # Prevent manual moves during auto-solve
            return
        
        clicked_disk_id = self.canvas.find_withtag("current")[0]
        
        # Find which logical peg the clicked disk belongs to
        for peg_idx in range(3):
            # Get the logical disk size of the top disk on this peg
            if self.pegs[peg_idx]:
                top_logical_disk_size = self.pegs[peg_idx][-1]
                # Get the canvas ID of that top logical disk
                top_visual_disk_id = self.disk_objects[top_logical_disk_size - 1]

                if clicked_disk_id == top_visual_disk_id:
                    # This is the valid disk to move
                    self.moving_disk_id = clicked_disk_id
                    self.orig_tower_index = peg_idx
                    self.canvas.tag_raise(self.moving_disk_id) # Bring to front visually
                    # Also raise its text label
                    text_id = self.canvas.find_withtag(f"disk_text_for_{self.moving_disk_id}")
                    if text_id:
                        self.canvas.tag_raise(text_id)
                    break

    def _drag_disk(self, event):
        """Handles the dragging motion of a disk."""
        if self.moving_disk_id and not self.auto_solving:
            # Get the disk size from its canvas ID to get its width
            disk_size = self._get_disk_size_from_id(self.moving_disk_id)
            disk_width = self.disk_widths[disk_size - 1]
            
            # Update the disk's position on the canvas
            self.canvas.coords(self.moving_disk_id, 
                              event.x - disk_width // 2, event.y - self.disk_height // 2,
                              event.x + disk_width // 2, event.y + self.disk_height // 2)
            
            # Also move the text label along with the disk
            text_id = self.canvas.find_withtag(f"disk_text_for_{self.moving_disk_id}")
            if text_id:
                self.canvas.coords(text_id[0], event.x, event.y)


    def _end_move(self, event):
        """
        Handles the release of a disk after dragging. Validates the move
        and updates the game state and visuals.
        """
        if not self.moving_disk_id or self.auto_solving:
            return
        
        dest_tower_index = self._get_tower_index_from_x(event.x)
        
        # Get the logical disk size of the disk being moved
        moving_disk_size = self._get_disk_size_from_id(self.moving_disk_id)

        # Check if the move is valid using the logical game state
        if self.is_valid_move(self.orig_tower_index, dest_tower_index):
            # Perform the logical move
            self.pegs[self.orig_tower_index].pop() # Remove from source
            self.pegs[dest_tower_index].append(moving_disk_size) # Add to destination
            
            # Update moves count
            self.moves_count += 1
            self._update_moves_display()
            
            # Visually reposition the disk to its final stacked position
            self._reposition_disk_visually(self.moving_disk_id, dest_tower_index)
            
            self._check_victory()
        else:
            # Move is invalid, visually return the disk to its original peg
            messagebox.showerror("Movimiento Inválido", "No puedes colocar un disco más grande sobre uno más pequeño.")
            self._reposition_disk_visually(self.moving_disk_id, self.orig_tower_index)
            
        # Reset moving state
        self.moving_disk_id = None
        self.orig_tower_index = None

    def _get_disk_size_from_id(self, disk_id: int) -> int:
        """
        Retrieves the logical disk size from its canvas ID.
        Args:
            disk_id (int): The canvas ID of the disk.
        Returns:
            int: The logical size of the disk (1 to num_disks).
        """
        for size in range(1, self.num_disks + 1):
            if self.disk_objects[size - 1] == disk_id:
                return size
        return 0 # Should not happen

    def _reposition_disk_visually(self, disk_id: int, target_peg_index: int):
        """
        Repositions a disk on the canvas to its correct stacked position on a peg.
        Args:
            disk_id (int): The canvas ID of the disk to reposition.
            target_peg_index (int): The index of the peg where the disk should be placed.
        """
        disk_size = self._get_disk_size_from_id(disk_id)
        disk_width = self.disk_widths[disk_size - 1]
        
        # Calculate the Y position based on the number of disks already on the target peg
        # The disk will be placed on top of the existing disks
        num_disks_on_target_peg = len(self.pegs[target_peg_index]) 
        
        x_dest = self.peg_x[target_peg_index]
        y_bottom = 400 - (num_disks_on_target_peg - 1) * self.disk_height # Adjusted for the disk itself

        self.canvas.coords(disk_id,
                           x_dest - disk_width // 2, y_bottom - self.disk_height,
                           x_dest + disk_width // 2, y_bottom)
        
        # Reposition the text label as well
        text_id = self.canvas.find_withtag(f"disk_text_for_{disk_id}")
        if text_id:
            self.canvas.coords(text_id[0], x_dest, y_bottom - self.disk_height // 2)


    def is_valid_move(self, from_peg_index: int, to_peg_index: int) -> bool:
        """
        Checks if a move from from_peg_index to to_peg_index is valid
        according to the rules of Towers of Hanoi. This uses the logical state (self.pegs).
        Args:
            from_peg_index (int): Index of the source peg.
            to_peg_index (int): Index of the destination peg.
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if not self.pegs[from_peg_index]: # No disks on the source peg
            return False
        
        # Get the logical size of the top disk on the source peg
        moving_disk_size = self.pegs[from_peg_index][-1]
        
        if not self.pegs[to_peg_index]: # Destination peg is empty
            return True # Any disk can be placed on an empty peg
        
        # Get the logical size of the top disk on the destination peg
        top_disk_on_dest_size = self.pegs[to_peg_index][-1]
        
        # A smaller disk can be placed on a larger disk
        return moving_disk_size < top_disk_on_dest_size

    def visualize_move(self, from_peg_index: int, to_peg_index: int, disk_size: int):
        """
        Visualizes a single move during automatic solving.
        This method is called by the HanoiSolver.
        Args:
            from_peg_index (int): Index of the source peg.
            to_peg_index (int): Index of the destination peg.
            disk_size (int): The logical size of the disk being moved.
        """
        if not self.auto_solving: # Only visualize if auto-solving is active
            return

        # Perform the logical move first
        # Ensure the disk being moved is actually the top disk on the source peg
        if self.pegs[from_peg_index] and self.pegs[from_peg_index][-1] == disk_size:
            self.pegs[from_peg_index].pop()
            self.pegs[to_peg_index].append(disk_size)
        else:
            # This case indicates a discrepancy or an attempt to move a non-top disk
            # during auto-solve, which shouldn't happen if solver logic is correct.
            print(f"Warning: Attempted to visualize invalid logical move for disk {disk_size} from {from_peg_index} to {to_peg_index}")
            return

        # Get the canvas ID of the disk that was logically moved
        moving_disk_id = self.disk_objects[disk_size - 1]
        
        # Update visual position on canvas
        self._reposition_disk_visually(moving_disk_id, to_peg_index)
        
        self.moves_count += 1
        self._update_moves_display()
        
        self.root.update_idletasks() # Update canvas immediately
        time.sleep(0.5) # Pause for visualization effect

    def _auto_solve(self):
        """Starts the automatic solving process in a separate thread."""
        if self.auto_solving:
            return
        
        # Reset game if not already in initial state, or if disks are not all on peg A
        if len(self.pegs[0]) != self.num_disks or self.pegs[0] != list(range(self.num_disks, 0, -1)):
            confirm = messagebox.askyesno("Reiniciar Juego", 
                                          "El juego no está en su estado inicial. ¿Desea reiniciarlo antes de resolver automáticamente?")
            if confirm:
                self._reset_game()
            else:
                return # User chose not to reset, so don't auto-solve

        self.auto_solving = True
        self._update_status_label("Modo: Resolución Automática")
        
        # Execute solver in a separate thread to keep UI responsive
        self.solver_thread = threading.Thread(target=self._run_solver_thread, daemon=True)
        self.solver_thread.start()

    def _run_solver_thread(self):
        """Helper function to run the solver in a thread."""
        self.solver.solve()
        # After solver finishes (or is stopped), update UI on the main thread
        self.root.after(0, self._on_solver_finished)

    def _on_solver_finished(self):
        """Callback executed on the main Tkinter thread after solver finishes."""
        self.auto_solving = False
        self._update_status_label("Modo: Manual - Arrastra los discos")
        self._check_victory()
        self.solver_thread = None # Clear thread reference

    def _stop_auto_solve(self):
        """Stops the automatic solving process."""
        if self.auto_solving:
            self.solver.stop_solving() # Signal the solver to stop
            self.auto_solving = False
            self._update_status_label("Modo: Manual - Arrastra los discos")
            # Wait for the solver thread to actually finish if it's still running
            if self.solver_thread and self.solver_thread.is_alive():
                # A small delay to allow the thread to gracefully exit its current step
                time.sleep(0.1) 
            self.solver_thread = None # Clear thread reference

    def _reset_game(self):
        """Resets the game to its initial state."""
        self._stop_auto_solve() # Ensure solver is stopped first
        self._initialize_game()
        self._update_status_label("Modo: Manual - Arrastra los discos")

    def _update_moves_display(self):
        """Updates the moves counter display."""
        self.moves_label.config(text=f"Movimientos: {self.moves_count}")

    def _update_status_label(self, text: str):
        """Updates the status label text."""
        self.status_label.config(text=text)

    def _check_victory(self):
        """Checks if the game has been won (all disks on peg C)."""
        # Victory condition: all disks are on the last peg (index 2)
        if len(self.pegs[2]) == self.num_disks:
            # Verify they are in correct order (largest at bottom, smallest at top)
            # The list self.pegs[2] should be [num_disks, num_disks-1, ..., 1]
            if self.pegs[2] == list(range(self.num_disks, 0, -1)):
                min_moves = (2 ** self.num_disks) - 1
                message = f"¡Felicidades! Has completado el juego.\n"
                message += f"Movimientos realizados: {self.moves_count}\n"
                message += f"Movimientos mínimos: {min_moves}"
                
                if self.moves_count == min_moves:
                    message += "\n¡Solución óptima!"
                
                messagebox.showinfo("¡Victoria!", message)
            else:
                # Disks are on peg C but not in the correct order (should not happen with valid moves)
                pass # Game not truly won if order is wrong

    def start(self):
        """Starts the Tkinter event loop."""
        self.root.mainloop()

def main():
    """Main function to start the game."""
    # Get number of disks from the user
    root_temp = tk.Tk()
    root_temp.withdraw() # Hide the temporary main window
    
    num_disks = simpledialog.askinteger(
        "Torres de Hanoi", 
        "Ingrese el número de discos (1-8):", 
        minvalue=1, maxvalue=8,
        parent=root_temp # Associate with the temporary root to ensure it's on top
    )
    
    root_temp.destroy() # Destroy the temporary root window
    
    if num_disks:
        game = HanoiGame(num_disks)
        game.start()
    else:
        messagebox.showinfo("Torres de Hanoi", "Juego cancelado.")

if __name__ == "__main__":
    main()