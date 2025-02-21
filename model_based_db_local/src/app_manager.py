import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import webbrowser
from pathlib import Path
import sqlite3
import json
from datetime import datetime
import threading
import queue
import signal

class AppManager(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("Eco-Vehicle Production System Manager")
        self.geometry("800x600")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Server status variables
        self.server_status = tk.StringVar(value="Stopped")
        self.server_process = None
        self.log_queue = queue.Queue()
        
        # Create GUI elements
        self.create_server_controls()
        self.create_database_controls()
        self.create_log_viewer()
        
        # Start periodic status checks
        self.check_server_status()
        
    def create_server_controls(self):
        # Server control frame
        server_frame = ttk.LabelFrame(self.main_container, text="Server Control", padding=10)
        server_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status display
        ttk.Label(server_frame, text="Server Status:").pack(side=tk.LEFT, padx=(0, 5))
        status_label = ttk.Label(server_frame, textvariable=self.server_status)
        status_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Control buttons
        self.start_btn = ttk.Button(server_frame, text="Start Server", command=self.start_server)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(server_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Open browser button
        self.browser_btn = ttk.Button(server_frame, text="Open Dashboard", command=self.open_dashboard)
        self.browser_btn.pack(side=tk.LEFT, padx=5)
        
    def create_database_controls(self):
        # Database control frame
        db_frame = ttk.LabelFrame(self.main_container, text="Database Management", padding=10)
        db_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Database path display
        ttk.Label(db_frame, text="Database Path:").pack(side=tk.LEFT, padx=(0, 5))
        self.db_path = tk.StringVar(value=os.path.join(Path(__file__).parent.parent, "requirements.db"))
        ttk.Entry(db_frame, textvariable=self.db_path, width=50).pack(side=tk.LEFT, padx=5)
        
        # Studio 3T button
        self.studio3t_btn = ttk.Button(db_frame, text="Open in Studio 3T", command=self.open_studio3t)
        self.studio3t_btn.pack(side=tk.LEFT, padx=5)
        
    def create_log_viewer(self):
        # Log viewer frame
        log_frame = ttk.LabelFrame(self.main_container, text="Server Logs", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
    def start_server(self):
        if not self.server_process:
            try:
                # Start FastAPI server
                cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8004", "--reload"]
                self.server_process = subprocess.Popen(
                    cmd,
                    cwd=os.path.dirname(os.path.abspath(__file__)),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # Start log monitoring thread
                threading.Thread(target=self.monitor_logs, daemon=True).start()
                
                self.server_status.set("Running")
                self.start_btn.configure(state=tk.DISABLED)
                self.stop_btn.configure(state=tk.NORMAL)
                self.log_message("Server started successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start server: {str(e)}")
                self.log_message(f"Error starting server: {str(e)}")
    
    def stop_server(self):
        if self.server_process:
            try:
                # Send SIGTERM signal to the server process
                if sys.platform == "win32":
                    self.server_process.terminate()
                else:
                    os.kill(self.server_process.pid, signal.SIGTERM)
                
                self.server_process = None
                self.server_status.set("Stopped")
                self.start_btn.configure(state=tk.NORMAL)
                self.stop_btn.configure(state=tk.DISABLED)
                self.log_message("Server stopped")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop server: {str(e)}")
                self.log_message(f"Error stopping server: {str(e)}")
    
    def open_dashboard(self):
        webbrowser.open("http://127.0.0.1:8004")
    
    def open_studio3t(self):
        db_path = self.db_path.get()
        if not os.path.exists(db_path):
            messagebox.showerror("Error", "Database file not found!")
            return
            
        # On macOS, Studio 3T is typically installed in /Applications
        studio3t_path = "/Applications/Studio 3T.app"
        
        if os.path.exists(studio3t_path):
            try:
                # Open Studio 3T with the SQLite database
                subprocess.Popen(["open", "-a", "Studio 3T", db_path])
                self.log_message(f"Opening database in Studio 3T: {db_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Studio 3T: {str(e)}")
                self.log_message(f"Error opening Studio 3T: {str(e)}")
        else:
            messagebox.showerror("Error", "Studio 3T not found. Please install it first.")
    
    def monitor_logs(self):
        while self.server_process:
            # Read server output
            output = self.server_process.stdout.readline()
            if output:
                self.log_queue.put(output.strip())
            
            # Check if process is still running
            if self.server_process.poll() is not None:
                break
    
    def check_server_status(self):
        # Update log viewer with new messages
        while not self.log_queue.empty():
            message = self.log_queue.get_nowait()
            self.log_message(message)
        
        # Schedule next check
        self.after(100, self.check_server_status)
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def on_closing(self):
        if self.server_process:
            if messagebox.askokcancel("Quit", "The server is still running. Do you want to stop it and exit?"):
                self.stop_server()
                self.quit()
        else:
            self.quit()

if __name__ == "__main__":
    app = AppManager()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
