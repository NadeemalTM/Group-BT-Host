"""
Simple Test Script for Bluetooth Music Player
Tests basic functionality without external dependencies.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys

class SimpleBluetoothMusicPlayer:
    """Simplified version for testing and demonstration."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bluetooth Multi-Device Music Player (Demo)")
        self.root.geometry("600x500")
        
        # Mock data for testing
        self.mock_devices = [
            {"name": "Bluetooth Speaker 1", "address": "00:11:22:33:44:55", "has_audio": True},
            {"name": "Wireless Headphones", "address": "AA:BB:CC:DD:EE:FF", "has_audio": True},
            {"name": "Bluetooth Earbuds", "address": "11:22:33:44:55:66", "has_audio": True}
        ]
        self.connected_devices = {}
        self.current_file = None
        
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title_label = ttk.Label(main_frame, text="Bluetooth Multi-Device Music Player", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Device discovery section
        device_frame = ttk.LabelFrame(main_frame, text="Bluetooth Devices", padding="10")
        device_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Discovery button
        self.discover_btn = ttk.Button(device_frame, text="Discover Devices", 
                                      command=self.discover_devices)
        self.discover_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Device list
        self.device_listbox = tk.Listbox(device_frame, height=6)
        self.device_listbox.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # Connect/Disconnect buttons
        self.connect_btn = ttk.Button(device_frame, text="Connect", 
                                     command=self.connect_device)
        self.connect_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.disconnect_btn = ttk.Button(device_frame, text="Disconnect", 
                                        command=self.disconnect_device)
        self.disconnect_btn.grid(row=0, column=2)
        
        # Connected devices section
        connected_frame = ttk.LabelFrame(main_frame, text="Connected Devices", padding="10")
        connected_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.connected_listbox = tk.Listbox(connected_frame, height=3)
        self.connected_listbox.grid(row=0, column=0, sticky="ew")
        
        # Music control section
        music_frame = ttk.LabelFrame(main_frame, text="Music Player", padding="10")
        music_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # File selection
        self.load_btn = ttk.Button(music_frame, text="Load Music File", 
                                  command=self.load_file)
        self.load_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(music_frame, text="No file loaded")
        self.file_label.grid(row=0, column=1, sticky="w")
        
        # Playback controls
        control_frame = ttk.Frame(music_frame)
        control_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.play_btn = ttk.Button(control_frame, text="Play", command=self.play_music)
        self.play_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_music)
        self.pause_btn.grid(row=0, column=1, padx=(0, 5))
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_music)
        self.stop_btn.grid(row=0, column=2)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief="sunken", 
                                     anchor="w", padding="5")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        device_frame.grid_columnconfigure(0, weight=1)
        connected_frame.grid_columnconfigure(0, weight=1)
        
    def discover_devices(self):
        """Simulate device discovery."""
        self.update_status("Discovering Bluetooth devices...")
        self.discover_btn.config(state="disabled")
        
        def discovery_worker():
            # Simulate discovery time
            time.sleep(2)
            
            # Update UI from main thread
            self.root.after(0, self._update_device_list)
            self.root.after(0, lambda: self.discover_btn.config(state="normal"))
            self.root.after(0, lambda: self.update_status("Discovery completed"))
        
        threading.Thread(target=discovery_worker, daemon=True).start()
    
    def _update_device_list(self):
        """Update the device list with discovered devices."""
        self.device_listbox.delete(0, tk.END)
        for device in self.mock_devices:
            display_text = f"{device['name']} ({device['address']})"
            self.device_listbox.insert(tk.END, display_text)
    
    def connect_device(self):
        """Simulate connecting to a device."""
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device to connect")
            return
        
        device_index = selection[0]
        device = self.mock_devices[device_index]
        
        if device['address'] not in self.connected_devices:
            self.connected_devices[device['address']] = device
            self._update_connected_devices()
            self.update_status(f"Connected to {device['name']}")
            messagebox.showinfo("Success", f"Connected to {device['name']}")
        else:
            messagebox.showinfo("Info", f"{device['name']} is already connected")
    
    def disconnect_device(self):
        """Simulate disconnecting from a device."""
        selection = self.connected_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a connected device to disconnect")
            return
        
        device_text = self.connected_listbox.get(selection[0])
        # Extract address from display text
        for addr, device in self.connected_devices.items():
            if device['name'] in device_text:
                del self.connected_devices[addr]
                self._update_connected_devices()
                self.update_status(f"Disconnected from {device['name']}")
                break
    
    def _update_connected_devices(self):
        """Update the connected devices list."""
        self.connected_listbox.delete(0, tk.END)
        for device in self.connected_devices.values():
            self.connected_listbox.insert(tk.END, f"{device['name']} - {device['address']}")
    
    def load_file(self):
        """Load a music file."""
        file_path = filedialog.askopenfilename(
            title="Select Music File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename)
            self.update_status(f"Loaded: {filename}")
    
    def play_music(self):
        """Simulate playing music."""
        if not self.current_file:
            messagebox.showwarning("Warning", "Please load a music file first")
            return
        
        if not self.connected_devices:
            messagebox.showwarning("Warning", "Please connect at least one Bluetooth device")
            return
        
        device_count = len(self.connected_devices)
        self.update_status(f"Playing music to {device_count} connected device(s)")
        messagebox.showinfo("Playing", f"Music is now playing to {device_count} Bluetooth device(s)")
    
    def pause_music(self):
        """Simulate pausing music."""
        self.update_status("Music paused")
        messagebox.showinfo("Paused", "Music playback paused")
    
    def stop_music(self):
        """Simulate stopping music."""
        self.update_status("Music stopped")
        messagebox.showinfo("Stopped", "Music playback stopped")
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_label.config(text=message)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    print("Starting Bluetooth Multi-Device Music Player (Demo Mode)")
    print("=" * 50)
    print("This is a demonstration version with simulated Bluetooth functionality.")
    print("In the full version, this would actually connect to real Bluetooth devices.")
    print("=" * 50)
    
    try:
        app = SimpleBluetoothMusicPlayer()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()