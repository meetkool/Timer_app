import tkinter as tk
import ctypes

class WindowShapeManager:
    """Handles custom window shaping - SRP"""
    @staticmethod
    def create_octagon_shape(root: tk.Tk, size: int = 300):
        """Create octagonal window shape for Windows"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        m = int(size * (1 - 1/(2**0.5)))  # Margin for regular octagon
        points = [
            m, 0,                # Top-left vertex
            size - m, 0,         # Top-right vertex
            size, m,             # Right-top vertex
            size, size - m,      # Right-bottom vertex
            size - m, size,      # Bottom-right vertex
            m, size,             # Bottom-left vertex
            0, size - m,         # Left-bottom vertex
            0, m                 # Left-top vertex
        ]
        npoints = len(points) // 2
        PointArray = (ctypes.c_int * len(points))(*points)
        region = ctypes.windll.gdi32.CreatePolygonRgn(PointArray, npoints, 1)
        ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    @staticmethod
    def create_rounded_rectangle_shape(root: tk.Tk, width: int = 300, height: int = 400):
        """Create rounded rectangle window shape for Windows - better for widget"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        corner_radius = 20  # Rounded corner radius
        
        # Create rounded rectangle region
        region = ctypes.windll.gdi32.CreateRoundRectRgn(
            0, 0,           # Left, Top
            width, height,  # Right, Bottom  
            corner_radius * 2, corner_radius * 2  # Corner width, height
        )
        ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    @staticmethod 
    def remove_shape(root: tk.Tk):
        """Remove custom window shape (make rectangular)"""
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        # Set to NULL region to make it rectangular
        ctypes.windll.user32.SetWindowRgn(hwnd, None, True)


class DraggableWindow:
    """Handles window dragging functionality - SRP"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self._offset_x = 0
        self._offset_y = 0
        self.update_callbacks = []  # List of callbacks to update floating elements
        self._setup_dragging()

    def add_update_callback(self, callback):
        """Add a callback to be called when window moves"""
        self.update_callbacks.append(callback)

    def _setup_dragging(self):
        self.root.bind("<ButtonPress-1>", self._start_move)
        self.root.bind("<B1-Motion>", self._do_move)

    def _start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _do_move(self, event):
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f"+{x}+{y}")
        
        # Update all floating elements immediately
        for callback in self.update_callbacks:
            callback()
        
        # Also trigger configure event for any other listeners
        self.root.event_generate("<Configure>")
