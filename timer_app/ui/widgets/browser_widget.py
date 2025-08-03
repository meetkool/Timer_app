import webview
import threading
import tkinter as tk
from tkinter import messagebox
import os
import sys

class BrowserWidget:
    """Browser widget that opens takeuforward.org with cookie support"""
    
    def __init__(self):
        self.window = None
        self.is_browser_open = False
        
    def open_takeuforward(self):
        """Open takeuforward.org in a browser window with cookie persistence"""
        if self.is_browser_open:
            messagebox.showinfo("Browser", "Browser is already open!")
            return
            
        try:
            # Create a separate thread for the browser to avoid blocking the main app
            browser_thread = threading.Thread(target=self._create_browser_window, daemon=True)
            browser_thread.start()
            
        except Exception as e:
            messagebox.showerror("Browser Error", f"Failed to open browser: {str(e)}")
    
    def _create_browser_window(self):
        """Create the browser window in a separate thread"""
        try:
            self.is_browser_open = True
            
            # Create the webview window
            self.window = webview.create_window(
                'TakeUForward - Coding Practice',
                'https://takeuforward.org/',
                width=1200,
                height=800,
                resizable=True,
                fullscreen=False,
                minimized=False,
                on_top=False,
                shadow=True,
                focus=True,
                text_select=True
            )
            
            # Set up cookie storage directory
            cookie_dir = self._get_cookie_directory()
            
            # Configure webview with cookie persistence
            webview.start(
                debug=False,
                private_mode=False,  # Enable cookies and local storage
                storage_path=cookie_dir,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
        except Exception as e:
            print(f"Browser error: {e}")
            messagebox.showerror("Browser Error", f"Failed to create browser: {str(e)}")
        finally:
            self.is_browser_open = False
    
    def _get_cookie_directory(self):
        """Get or create a directory for storing browser cookies and data"""
        # Create a storage directory in the app's directory
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        storage_dir = os.path.join(app_dir, 'storage', 'browser_data')
        
        # Create the directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        return storage_dir
    
    def close_browser(self):
        """Close the browser window"""
        if self.window and self.is_browser_open:
            try:
                self.window.destroy()
                self.is_browser_open = False
            except:
                pass
    
    def is_open(self):
        """Check if browser is currently open"""
        return self.is_browser_open


class BrowserManager:
    """Singleton manager for browser instances"""
    _instance = None
    _browser = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
            cls._browser = BrowserWidget()
        return cls._instance
    
    def open_takeuforward(self):
        """Open takeuforward.org browser"""
        return self._browser.open_takeuforward()
    
    def close_browser(self):
        """Close browser if open"""
        return self._browser.close_browser()
    
    def is_browser_open(self):
        """Check if browser is open"""
        return self._browser.is_open()