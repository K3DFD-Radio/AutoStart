import json
import subprocess
import time
import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path
import threading

class AutoStart:
    def __init__(self, config_file='autostart.json'):
        self.config_file = config_file
        self.pid_file = 'autostart_pids.json'
        self.config = None
        self.running_processes = {}
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            return True, "Configuration loaded successfully"
        except FileNotFoundError:
            return False, f"{self.config_file} not found!"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON format: {e}"
    
    def start_sequence(self, callback=None):
        """Start applications in sequence"""
        if not self.config or 'startup' not in self.config:
            return False, "No startup sequence defined"
        
        startup = self.config['startup']
        
        for idx, item in enumerate(startup, 1):
            path = item.get('path', '')
            delay = item.get('delay', 0)
            
            if callback:
                callback(f"[{idx}/{len(startup)}] Starting: {Path(path).name}")
            
            try:
                process = subprocess.Popen(path)
                self.running_processes[path] = process.pid
                
                if callback:
                    callback(f" Started (PID: {process.pid})")
                
                if idx < len(startup) and delay > 0:
                    if callback:
                        callback(f" Waiting {delay} seconds...")
                    time.sleep(delay)
                    
            except Exception as e:
                if callback:
                    callback(f" Failed: {e}")
        
        self._save_pids()
        return True, "Startup complete!"
    
    def stop_sequence(self, callback=None):
        """Stop applications in sequence"""
        if not self.config or 'shutdown' not in self.config:
            return False, "No shutdown sequence defined"
        
        shutdown = self.config['shutdown']
        self._load_pids()
        
        for idx, item in enumerate(shutdown, 1):
            path = item.get('path', '')
            delay = item.get('delay', 0)
            exe_name = Path(path).stem
            
            if callback:
                callback(f"[{idx}/{len(shutdown)}] Stopping: {Path(path).name}")
            
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/IM', f'{exe_name}.exe'],
                    capture_output=True,
                    text=True
                )
                
                if callback:
                    if result.returncode == 0:
                        callback(f"  Stopped")
                    else:
                        callback(f"  Process may not be running")
                
                if idx < len(shutdown) and delay > 0:
                    if callback:
                        callback(f"  Waiting {delay} seconds...")
                    time.sleep(delay)
                    
            except Exception as e:
                if callback:
                    callback(f"  Failed: {e}")
        
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
        
        return True, "Shutdown complete!"
    
    def _save_pids(self):
        """Save process IDs to file"""
        try:
            with open(self.pid_file, 'w') as f:
                json.dump(self.running_processes, f, indent=2)
        except Exception:
            pass
    
    def _load_pids(self):
        """Load process IDs from file"""
        try:
            if os.path.exists(self.pid_file):
                with open(self.pid_file, 'r') as f:
                    self.running_processes = json.load(f)
        except Exception:
            pass


class AutoStartGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoStart Sequencer")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.autostart = AutoStart()
        self.is_running = False
        
        self.setup_ui()
        self.load_initial_config()
    
    def setup_ui(self):
        """Create the GUI layout"""
        """Be careful when making GUI changes"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=file_menu)
        file_menu.add_command(label="Edit Run/Stop File", command=self.edit_config)
        file_menu.add_command(label="Reload Run/Stop File", command=self.load_initial_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#f0f0f0', height=50)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame, 
            text="AutoStart Ready", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        self.status_label.pack(expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        # START button
        self.start_button = tk.Button(
            button_frame,
            text="START",
            font=('Arial', 20, 'bold'),
            bg='#00cc00',
            fg='white',
            width=15,
            height=2,
            command=self.start_apps,
            relief=tk.RAISED,
            bd=4,
            activebackground='#00ff00'
        )
        self.start_button.pack(pady=10)
        
        # STOP button
        self.stop_button = tk.Button(
            button_frame,
            text="STOP",
            font=('Arial', 20, 'bold'),
            bg='#cc0000',
            fg='white',
            width=15,
            height=2,
            command=self.stop_apps,
            relief=tk.RAISED,
            bd=4,
            activebackground='#ff0000'
        )
        self.stop_button.pack(pady=10)
        
        # Log frame
        log_frame = tk.LabelFrame(self.root, text="Run/Stop Status View", font=('Arial', 10))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Clear log button
        clear_btn = tk.Button(
            log_frame,
            text="Clear Log",
            command=self.clear_log,
            font=('Arial', 8)
        )
        clear_btn.pack(pady=5)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log window"""
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, message, color='#333333'):
        """Update status label"""
        self.status_label.config(text=message, fg=color)
    
    def load_initial_config(self):
        """Load configuration at startup"""
        success, message = self.autostart.load_config()
        if success:
            self.log("Configuration loaded")
            self.update_status("Ready", '#00aa00')
            
            # Show what's configured
            if self.autostart.config:
                startup_count = len(self.autostart.config.get('startup', []))
                shutdown_count = len(self.autostart.config.get('shutdown', []))
                self.log(f"  Startup: {startup_count} apps")
                self.log(f"  Shutdown: {shutdown_count} apps")
        else:
            self.log(f" {message}")
            self.update_status("Configuration Error", '#cc0000')
            messagebox.showerror("Configuration Error", message)
    
    def edit_config(self):
        """Open configuration file in default editor"""
        try:
            if sys.platform == 'win32':
                os.startfile('autostart.json')
            elif sys.platform == 'darwin':
                subprocess.call(['open', 'autostart.json'])
            else:
                subprocess.call(['xdg-open', 'autostart.json'])
            self.log("Opened autostart.json for editing")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def start_apps(self):
        """Start applications in sequence"""
        if self.is_running:
            messagebox.showwarning("Busy", "Operation already in progress")
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Starting applications...", '#0066cc')
        self.log("\nStarting sequence...")
        
        def run():
            success, message = self.autostart.start_sequence(callback=self.log)
            self.root.after(0, lambda: self.operation_complete(success, message, "start"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop_apps(self):
        """Stop applications in sequence"""
        if self.is_running:
            messagebox.showwarning("Busy", "Operation already in progress")
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Stopping applications...", '#cc6600')
        self.log("\nStopping sequence...")
        
        def run():
            success, message = self.autostart.stop_sequence(callback=self.log)
            self.root.after(0, lambda: self.operation_complete(success, message, "stop"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def operation_complete(self, success, message, operation):
        """Handle completion of start/stop operation"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        
        if success:
            self.log(f" {message}")
            self.update_status("Ready", '#00aa00')
        else:
            self.log(f" {message}")
            self.update_status("Error", '#cc0000')
            messagebox.showerror("Error", message)


def main():
    root = tk.Tk()
    app = AutoStartGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()