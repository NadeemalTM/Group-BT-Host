"""
GUI Components Module
Creates the user interface for the Bluetooth Multi-Device Music Player.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, List, Callable

class MusicPlayerGUI:
    def __init__(self, root: tk.Tk, app_controller):
        self.root = root
        self.app = app_controller
        
        # GUI State
        self.discovered_devices = []
        self.connected_devices = {}
        self.current_song = "No file loaded"
        self.is_playing = False
        
        # Create the main interface
        self.create_widgets()
        self.setup_layout()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Bluetooth Multi-Device Music Player",
            font=("Arial", 16, "bold")
        )
        
        # Device Discovery Section
        self.device_frame = ttk.LabelFrame(self.main_frame, text="Bluetooth Devices", padding="10")
        
        self.discover_btn = ttk.Button(
            self.device_frame,
            text="Discover Devices",
            command=self.discover_devices
        )
        
        self.refresh_btn = ttk.Button(
            self.device_frame,
            text="Refresh",
            command=self.refresh_devices
        )
        
        # Device list
        self.device_tree = ttk.Treeview(
            self.device_frame,
            columns=("Name", "Address", "Audio", "Signal"),
            show="tree headings",
            height=6
        )
        
        self.device_tree.heading("#0", text="", anchor="w")
        self.device_tree.heading("Name", text="Device Name", anchor="w")
        self.device_tree.heading("Address", text="Address", anchor="w")
        self.device_tree.heading("Audio", text="Audio Support", anchor="center")
        self.device_tree.heading("Signal", text="Signal", anchor="center")
        
        self.device_tree.column("#0", width=30, minwidth=30)
        self.device_tree.column("Name", width=200, minwidth=150)
        self.device_tree.column("Address", width=150, minwidth=120)
        self.device_tree.column("Audio", width=100, minwidth=80)
        self.device_tree.column("Signal", width=80, minwidth=60)
        
        # Device control buttons
        self.connect_btn = ttk.Button(
            self.device_frame,
            text="Connect",
            command=self.connect_selected_device
        )
        
        self.disconnect_btn = ttk.Button(
            self.device_frame,
            text="Disconnect",
            command=self.disconnect_selected_device
        )
        
        # Scrollbar for device list
        self.device_scrollbar = ttk.Scrollbar(self.device_frame, orient="vertical", command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=self.device_scrollbar.set)
        
        # Connected Devices Section
        self.connected_frame = ttk.LabelFrame(self.main_frame, text="Connected Devices", padding="10")
        
        self.connected_listbox = tk.Listbox(self.connected_frame, height=4)
        self.connected_scrollbar = ttk.Scrollbar(self.connected_frame, orient="vertical", command=self.connected_listbox.yview)
        self.connected_listbox.configure(yscrollcommand=self.connected_scrollbar.set)
        
        # Music Control Section
        self.music_frame = ttk.LabelFrame(self.main_frame, text="Music Player", padding="10")
        
        # File selection
        self.file_frame = ttk.Frame(self.music_frame)
        self.load_btn = ttk.Button(
            self.file_frame,
            text="Load Music File",
            command=self.load_music_file
        )
        
        self.current_song_label = ttk.Label(
            self.file_frame,
            text=self.current_song,
            font=("Arial", 10),
            foreground="blue"
        )
        
        # Playback controls
        self.control_frame = ttk.Frame(self.music_frame)
        
        self.play_btn = ttk.Button(
            self.control_frame,
            text="▶ Play",
            command=self.play_music,
            state="disabled"
        )
        
        self.pause_btn = ttk.Button(
            self.control_frame,
            text="⏸ Pause",
            command=self.pause_music,
            state="disabled"
        )
        
        self.stop_btn = ttk.Button(
            self.control_frame,
            text="⏹ Stop",
            command=self.stop_music,
            state="disabled"
        )
        
        # Volume control
        self.volume_frame = ttk.Frame(self.music_frame)
        self.volume_label = ttk.Label(self.volume_frame, text="Volume:")
        
        self.volume_var = tk.IntVar(value=70)
        self.volume_scale = ttk.Scale(
            self.volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
            command=self.on_volume_change
        )
        
        self.volume_value_label = ttk.Label(self.volume_frame, text="70%")
        
        # Status Section
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready - Click 'Discover Devices' to begin",
            relief="sunken",
            anchor="w",
            padding="5"
        )
        
        # Settings Section
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        
        # Sync delay setting
        self.sync_frame = ttk.Frame(self.settings_frame)
        self.sync_label = ttk.Label(self.sync_frame, text="Sync Delay (ms):")
        self.sync_var = tk.IntVar(value=150)
        self.sync_spinbox = ttk.Spinbox(
            self.sync_frame,
            from_=0,
            to=1000,
            textvariable=self.sync_var,
            width=10,
            command=self.on_sync_delay_change
        )
        
        # Auto-connect setting
        self.auto_connect_var = tk.BooleanVar(value=False)
        self.auto_connect_check = ttk.Checkbutton(
            self.settings_frame,
            text="Auto-connect to known devices",
            variable=self.auto_connect_var
        )
        
    def setup_layout(self):
        """Set up the layout of all widgets."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Configure main frame grid weights
        self.main_frame.grid_rowconfigure(1, weight=1)  # Device frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Device Discovery Section
        self.device_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Discovery buttons
        button_frame = ttk.Frame(self.device_frame)
        button_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        self.discover_btn.grid(row=0, column=0, padx=(0, 5))
        self.refresh_btn.grid(row=0, column=1, padx=(0, 5))
        self.connect_btn.grid(row=0, column=2, padx=(0, 5))
        self.disconnect_btn.grid(row=0, column=3)
        
        # Device tree
        self.device_tree.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.device_scrollbar.grid(row=1, column=3, sticky="ns")
        
        # Configure device frame grid weights
        self.device_frame.grid_rowconfigure(1, weight=1)
        self.device_frame.grid_columnconfigure(0, weight=1)
        
        # Connected Devices Section
        self.connected_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.connected_listbox.grid(row=0, column=0, sticky="ew")
        self.connected_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.connected_frame.grid_columnconfigure(0, weight=1)
        
        # Music Control Section
        self.music_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # File selection
        self.file_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        self.load_btn.grid(row=0, column=0, padx=(0, 10))
        self.current_song_label.grid(row=0, column=1, sticky="w")
        
        # Playback controls
        self.control_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.play_btn.grid(row=0, column=0, padx=(0, 5))
        self.pause_btn.grid(row=0, column=1, padx=(0, 5))
        self.stop_btn.grid(row=0, column=2)
        
        # Volume control
        self.volume_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.volume_label.grid(row=0, column=0, padx=(0, 10))
        self.volume_scale.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.volume_value_label.grid(row=0, column=2)
        
        self.volume_frame.grid_columnconfigure(1, weight=1)
        
        # Settings Section
        self.settings_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        self.sync_frame.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.sync_label.grid(row=0, column=0, padx=(0, 10))
        self.sync_spinbox.grid(row=0, column=1)
        
        self.auto_connect_check.grid(row=1, column=0, sticky="w")
        
        # Status Section
        self.status_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.status_label.grid(row=0, column=0, sticky="ew")
        
        self.status_frame.grid_columnconfigure(0, weight=1)
        
    def discover_devices(self):
        """Handle device discovery button click."""
        def discovery_thread():
            self.update_status("Discovering Bluetooth devices...")
            self.discover_btn.configure(state="disabled")
            try:
                devices = self.app.discover_devices()
                self.root.after(0, lambda: self.discover_btn.configure(state="normal"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Discovery failed: {str(e)}"))
                self.root.after(0, lambda: self.discover_btn.configure(state="normal"))
        
        threading.Thread(target=discovery_thread, daemon=True).start()
    
    def refresh_devices(self):
        """Refresh the device list."""
        self.discover_devices()
    
    def connect_selected_device(self):
        """Connect to the selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device to connect")
            return
        
        item = selection[0]
        device_data = self.device_tree.item(item)
        
        if device_data['values']:
            device_name = device_data['values'][0]
            device_address = device_data['values'][1]
            
            def connect_thread():
                success = self.app.connect_device(device_address, device_name)
                if not success:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Connection Failed", 
                        f"Could not connect to {device_name}"
                    ))
            
            threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect_selected_device(self):
        """Disconnect the selected connected device."""
        selection = self.connected_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a connected device to disconnect")
            return
        
        device_info = self.connected_listbox.get(selection[0])
        device_address = device_info.split(" - ")[1] if " - " in device_info else ""
        
        if device_address:
            self.app.disconnect_device(device_address)
    
    def load_music_file(self):
        """Handle music file loading."""
        success = self.app.load_music_file()
        if success:
            self.play_btn.configure(state="normal")
    
    def play_music(self):
        """Handle play button click."""
        self.app.play_music()
    
    def pause_music(self):
        """Handle pause button click."""
        self.app.pause_music()
    
    def stop_music(self):
        """Handle stop button click."""
        self.app.stop_music()
    
    def on_volume_change(self, value):
        """Handle volume slider change."""
        volume = int(float(value))
        self.volume_value_label.configure(text=f"{volume}%")
        self.app.set_volume(volume)
    
    def on_sync_delay_change(self):
        """Handle sync delay setting change."""
        delay_ms = self.sync_var.get()
        delay_s = delay_ms / 1000.0
        self.app.audio_engine.set_sync_delay(delay_s)
    
    def update_device_list(self, devices: List[Dict]):
        """Update the device list display."""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
        
        # Add new devices
        for i, device in enumerate(devices):
            audio_support = "✓" if device.get('has_audio', False) else "✗"
            signal_strength = f"{device.get('rssi', -100)} dBm"
            
            self.device_tree.insert(
                "",
                "end",
                text=str(i+1),
                values=(
                    device.get('name', 'Unknown'),
                    device.get('address', ''),
                    audio_support,
                    signal_strength
                )
            )
        
        self.discovered_devices = devices
    
    def update_connected_devices(self, connected_devices: Dict):
        """Update the connected devices display."""
        self.connected_listbox.delete(0, tk.END)
        
        for address, device_info in connected_devices.items():
            device_name = device_info.get('name', 'Unknown Device')
            self.connected_listbox.insert(tk.END, f"{device_name} - {address}")
        
        self.connected_devices = connected_devices
    
    def update_current_song(self, song_name: str):
        """Update the current song display."""
        self.current_song = song_name
        display_name = song_name if len(song_name) <= 50 else song_name[:47] + "..."
        self.current_song_label.configure(text=display_name)
    
    def update_playback_controls(self, is_playing: bool):
        """Update playback control button states."""
        if is_playing:
            self.play_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self.stop_btn.configure(state="normal")
        else:
            self.play_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")
            self.stop_btn.configure(state="disabled")
        
        self.is_playing = is_playing
    
    def update_status(self, message: str):
        """Update the status bar."""
        self.status_label.configure(text=message)
        self.root.update_idletasks()

class DeviceInfoDialog:
    """Dialog for showing detailed device information."""
    
    def __init__(self, parent, device_info: Dict):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Device Information")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets(device_info)
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def create_widgets(self, device_info: Dict):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Device name
        ttk.Label(main_frame, text="Device Name:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(main_frame, text=device_info.get('name', 'Unknown')).pack(anchor="w", pady=(0, 10))
        
        # Device address
        ttk.Label(main_frame, text="Bluetooth Address:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(main_frame, text=device_info.get('address', 'Unknown')).pack(anchor="w", pady=(0, 10))
        
        # Audio support
        ttk.Label(main_frame, text="Audio Support:", font=("Arial", 10, "bold")).pack(anchor="w")
        audio_text = "Yes" if device_info.get('has_audio', False) else "No"
        ttk.Label(main_frame, text=audio_text).pack(anchor="w", pady=(0, 10))
        
        # Signal strength
        ttk.Label(main_frame, text="Signal Strength:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(main_frame, text=f"{device_info.get('rssi', -100)} dBm").pack(anchor="w", pady=(0, 10))
        
        # Services
        ttk.Label(main_frame, text="Available Services:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(main_frame, text=f"{device_info.get('services', 0)} services found").pack(anchor="w", pady=(0, 20))
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack()

class SettingsDialog:
    """Dialog for application settings."""
    
    def __init__(self, parent, app_controller):
        self.app = app_controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        """Create settings dialog widgets."""
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Audio settings tab
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio")
        
        # Bluetooth settings tab
        bluetooth_frame = ttk.Frame(notebook)
        notebook.add(bluetooth_frame, text="Bluetooth")
        
        # Create audio settings
        self.create_audio_settings(audio_frame)
        
        # Create bluetooth settings
        self.create_bluetooth_settings(bluetooth_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="OK", command=self.save_settings).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side="right")
    
    def create_audio_settings(self, parent):
        """Create audio settings widgets."""
        # Audio quality settings
        quality_frame = ttk.LabelFrame(parent, text="Audio Quality", padding="10")
        quality_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(quality_frame, text="Sample Rate:").grid(row=0, column=0, sticky="w", pady=5)
        sample_rate_combo = ttk.Combobox(quality_frame, values=["44100", "48000", "96000"])
        sample_rate_combo.set("44100")
        sample_rate_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        ttk.Label(quality_frame, text="Bit Depth:").grid(row=1, column=0, sticky="w", pady=5)
        bit_depth_combo = ttk.Combobox(quality_frame, values=["16", "24", "32"])
        bit_depth_combo.set("16")
        bit_depth_combo.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        quality_frame.grid_columnconfigure(1, weight=1)
    
    def create_bluetooth_settings(self, parent):
        """Create bluetooth settings widgets."""
        # Connection settings
        conn_frame = ttk.LabelFrame(parent, text="Connection Settings", padding="10")
        conn_frame.pack(fill="x", padx=10, pady=10)
        
        auto_reconnect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(conn_frame, text="Auto-reconnect to devices", variable=auto_reconnect_var).pack(anchor="w", pady=5)
        
        discovery_timeout_frame = ttk.Frame(conn_frame)
        discovery_timeout_frame.pack(fill="x", pady=5)
        
        ttk.Label(discovery_timeout_frame, text="Discovery Timeout (seconds):").pack(side="left")
        timeout_spinbox = ttk.Spinbox(discovery_timeout_frame, from_=5, to=60, width=10)
        timeout_spinbox.set("10")
        timeout_spinbox.pack(side="right")
    
    def save_settings(self):
        """Save settings and close dialog."""
        # Here you would save the settings to the application
        self.dialog.destroy()