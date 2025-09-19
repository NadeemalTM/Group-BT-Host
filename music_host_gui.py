"""
Music Host by Nadeemal
Professional Audio Streaming Interface

This application captures any audio playing on Windows and streams it
to multiple connected Bluetooth devices simultaneously.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
from datetime import datetime
import subprocess
import sys
from pathlib import Path

class MusicHostGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_variables()
        self.create_widgets()
        self.setup_layout()
        self.load_settings()
        
        # Initialize backend systems
        self.audio_capture = None
        self.bluetooth_manager = None
        self.connected_devices = []
        self.is_streaming = False
        
    def setup_window(self):
        """Configure main window properties."""
        self.root.title("Music Host by Nadeemal - Universal Audio Streaming")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass  # Icon file not found
            
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_styles(self):
        """Configure modern styling for the interface."""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Custom colors - modern dark theme
        self.colors = {
            'bg_primary': '#2C3E50',      # Dark blue-gray
            'bg_secondary': '#34495E',     # Lighter blue-gray  
            'bg_accent': '#3498DB',        # Blue accent
            'text_primary': '#ECF0F1',     # Light gray text
            'text_secondary': '#BDC3C7',   # Medium gray text
            'success': '#27AE60',          # Green
            'warning': '#F39C12',          # Orange
            'danger': '#E74C3C',           # Red
            'info': '#3498DB'              # Blue
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Style ttk widgets
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_secondary'])
        
        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        # Button styles
        style.configure('Action.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 10))
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(15, 8))
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=(15, 8))
        
    def create_variables(self):
        """Create tkinter variables for data binding."""
        self.var_audio_source = tk.StringVar(value="System Audio")
        self.var_streaming_status = tk.StringVar(value="● Stopped")
        self.var_connected_count = tk.StringVar(value="0")
        self.var_volume_level = tk.IntVar(value=75)
        self.var_auto_connect = tk.BooleanVar(value=True)
        self.var_system_tray = tk.BooleanVar(value=False)
        self.var_current_audio = tk.StringVar(value="No audio detected")
        
    def create_widgets(self):
        """Create all GUI widgets."""
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
    def create_header(self):
        """Create application header with title and status."""
        self.header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], pady=20)
        
        # Title
        title_label = ttk.Label(self.header_frame, 
                               text="🎵 Music Host by Nadeemal",
                               style='Title.TLabel')
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(self.header_frame,
                                  text="Stream any Windows audio to multiple Bluetooth devices",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Current audio status
        self.audio_status_frame = tk.Frame(self.header_frame, bg=self.colors['bg_secondary'], pady=10, padx=20)
        self.audio_status_frame.pack(pady=(20, 0), padx=20, fill='x')
        
        ttk.Label(self.audio_status_frame, text="🎶 Currently Playing:",
                 style='Header.TLabel').pack(side='left')
        
        self.current_audio_label = ttk.Label(self.audio_status_frame, 
                                           textvariable=self.var_current_audio,
                                           style='Status.TLabel')
        self.current_audio_label.pack(side='left', padx=(10, 0))
        
    def create_main_content(self):
        """Create main content areas."""
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.main_frame)
        
        # Create tabs
        self.create_devices_tab()
        self.create_audio_tab()
        self.create_settings_tab()
        
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
    def create_devices_tab(self):
        """Create Bluetooth devices management tab."""
        self.devices_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.devices_frame, text="📱 Bluetooth Devices")
        
        # Device discovery section
        discovery_frame = tk.LabelFrame(self.devices_frame, text="Device Discovery",
                                       bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                       font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        discovery_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # Discovery controls
        discovery_controls = tk.Frame(discovery_frame, bg=self.colors['bg_secondary'])
        discovery_controls.pack(fill='x', pady=5)
        
        self.btn_discover = ttk.Button(discovery_controls, text="🔍 Discover Devices",
                                      style='Action.TButton',
                                      command=self.discover_devices)
        self.btn_discover.pack(side='left', padx=(0, 10))
        
        self.btn_refresh = ttk.Button(discovery_controls, text="🔄 Refresh",
                                     command=self.refresh_devices)
        self.btn_refresh.pack(side='left', padx=(0, 10))
        
        # Auto-connect checkbox
        auto_connect_cb = ttk.Checkbutton(discovery_controls, text="Auto-connect to known devices",
                                         variable=self.var_auto_connect)
        auto_connect_cb.pack(side='right')
        
        # Available devices section
        available_frame = tk.LabelFrame(self.devices_frame, text="Available Devices",
                                       bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                       font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        available_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Available devices list
        self.available_tree = ttk.Treeview(available_frame, columns=('type', 'status', 'signal'),
                                          show='tree headings', height=8)
        self.available_tree.heading('#0', text='Device Name', anchor='w')
        self.available_tree.heading('type', text='Type', anchor='center')
        self.available_tree.heading('status', text='Status', anchor='center')
        self.available_tree.heading('signal', text='Signal', anchor='center')
        
        self.available_tree.column('#0', width=300)
        self.available_tree.column('type', width=100)
        self.available_tree.column('status', width=100)
        self.available_tree.column('signal', width=80)
        
        # Scrollbar for available devices
        available_scroll = ttk.Scrollbar(available_frame, orient='vertical', command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=available_scroll.set)
        
        self.available_tree.pack(side='left', fill='both', expand=True, padx=(0, 5))
        available_scroll.pack(side='right', fill='y')
        
        # Device action buttons
        device_actions = tk.Frame(available_frame, bg=self.colors['bg_secondary'])
        device_actions.pack(side='bottom', fill='x', pady=(10, 0))
        
        self.btn_connect = ttk.Button(device_actions, text="🔗 Connect",
                                     style='Success.TButton',
                                     command=self.connect_device)
        self.btn_connect.pack(side='left', padx=(0, 5))
        
        self.btn_disconnect = ttk.Button(device_actions, text="❌ Disconnect",
                                        style='Danger.TButton',
                                        command=self.disconnect_device)
        self.btn_disconnect.pack(side='left', padx=(0, 5))
        
        self.btn_test_audio = ttk.Button(device_actions, text="🔊 Test Audio",
                                        command=self.test_device_audio)
        self.btn_test_audio.pack(side='left')
        
        # Connected devices section
        connected_frame = tk.LabelFrame(self.devices_frame, text="Connected Devices",
                                       bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                       font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        connected_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        # Connected devices display
        self.connected_frame_inner = tk.Frame(connected_frame, bg=self.colors['bg_secondary'])
        self.connected_frame_inner.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Connection count display
        count_frame = tk.Frame(connected_frame, bg=self.colors['bg_secondary'])
        count_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(count_frame, text="Connected Devices:",
                 style='Header.TLabel').pack(side='left')
        
        self.connected_count_label = ttk.Label(count_frame, textvariable=self.var_connected_count,
                                              style='Status.TLabel')
        self.connected_count_label.pack(side='left', padx=(5, 0))
        
    def create_audio_tab(self):
        """Create audio control and monitoring tab."""
        self.audio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.audio_frame, text="🎵 Audio Control")
        
        # Audio source selection
        source_frame = tk.LabelFrame(self.audio_frame, text="Audio Source",
                                    bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        source_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # Source selection controls
        source_controls = tk.Frame(source_frame, bg=self.colors['bg_secondary'])
        source_controls.pack(fill='x', pady=5)
        
        ttk.Label(source_controls, text="Capture:",
                 style='Header.TLabel').pack(side='left')
        
        self.source_combo = ttk.Combobox(source_controls, textvariable=self.var_audio_source,
                                        values=["System Audio", "Microphone", "Application Audio"],
                                        state='readonly', width=20)
        self.source_combo.pack(side='left', padx=(10, 0))
        
        self.btn_refresh_sources = ttk.Button(source_controls, text="🔄 Refresh Sources",
                                             command=self.refresh_audio_sources)
        self.btn_refresh_sources.pack(side='left', padx=(10, 0))
        
        # Streaming controls
        control_frame = tk.LabelFrame(self.audio_frame, text="Streaming Control",
                                     bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Main streaming controls
        main_controls = tk.Frame(control_frame, bg=self.colors['bg_secondary'])
        main_controls.pack(fill='x', pady=5)
        
        self.btn_start_streaming = ttk.Button(main_controls, text="▶️ Start Streaming",
                                             style='Action.TButton',
                                             command=self.start_streaming)
        self.btn_start_streaming.pack(side='left', padx=(0, 10))
        
        self.btn_stop_streaming = ttk.Button(main_controls, text="⏹️ Stop Streaming",
                                            style='Danger.TButton',
                                            command=self.stop_streaming,
                                            state='disabled')
        self.btn_stop_streaming.pack(side='left', padx=(0, 10))
        
        # Streaming status
        status_label = ttk.Label(main_controls, text="Status:",
                                style='Header.TLabel')
        status_label.pack(side='left', padx=(20, 5))
        
        self.streaming_status_label = ttk.Label(main_controls, textvariable=self.var_streaming_status,
                                               style='Status.TLabel')
        self.streaming_status_label.pack(side='left')
        
        # Volume control
        volume_frame = tk.Frame(control_frame, bg=self.colors['bg_secondary'])
        volume_frame.pack(fill='x', pady=(10, 5))
        
        ttk.Label(volume_frame, text="🔊 Volume:",
                 style='Header.TLabel').pack(side='left')
        
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient='horizontal',
                                     variable=self.var_volume_level, length=200,
                                     command=self.on_volume_change)
        self.volume_scale.pack(side='left', padx=(10, 5))
        
        self.volume_label = ttk.Label(volume_frame, text="75%",
                                     style='Status.TLabel')
        self.volume_label.pack(side='left', padx=(5, 0))
        
        # Audio monitoring
        monitor_frame = tk.LabelFrame(self.audio_frame, text="Audio Monitor",
                                     bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        monitor_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Audio level meter (placeholder)
        level_frame = tk.Frame(monitor_frame, bg=self.colors['bg_secondary'])
        level_frame.pack(fill='x', pady=5)
        
        ttk.Label(level_frame, text="Audio Level:",
                 style='Header.TLabel').pack(side='left')
        
        # Simple audio level display
        self.audio_level_canvas = tk.Canvas(level_frame, height=20, width=300,
                                           bg='black', highlightthickness=0)
        self.audio_level_canvas.pack(side='left', padx=(10, 0))
        
        # Audio info display
        info_frame = tk.Frame(monitor_frame, bg=self.colors['bg_secondary'])
        info_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        self.audio_info_text = tk.Text(info_frame, height=8, bg='black', fg='green',
                                      font=('Consolas', 10), wrap=tk.WORD)
        info_scroll = ttk.Scrollbar(info_frame, orient='vertical', command=self.audio_info_text.yview)
        self.audio_info_text.configure(yscrollcommand=info_scroll.set)
        
        self.audio_info_text.pack(side='left', fill='both', expand=True, padx=(0, 5))
        info_scroll.pack(side='right', fill='y')
        
        # Initialize with placeholder text
        self.audio_info_text.insert('1.0', "Audio monitoring will appear here...\n")
        
    def create_settings_tab(self):
        """Create application settings tab."""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        
        # General settings
        general_frame = tk.LabelFrame(self.settings_frame, text="General Settings",
                                     bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                     font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        general_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # System tray option
        tray_frame = tk.Frame(general_frame, bg=self.colors['bg_secondary'])
        tray_frame.pack(fill='x', pady=5)
        
        ttk.Checkbutton(tray_frame, text="Minimize to system tray",
                       variable=self.var_system_tray).pack(side='left')
        
        # Auto-start option
        autostart_frame = tk.Frame(general_frame, bg=self.colors['bg_secondary'])
        autostart_frame.pack(fill='x', pady=5)
        
        ttk.Checkbutton(autostart_frame, text="Start with Windows",
                       command=self.toggle_autostart).pack(side='left')
        
        # Audio settings
        audio_settings_frame = tk.LabelFrame(self.settings_frame, text="Audio Settings",
                                           bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                           font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        audio_settings_frame.pack(fill='x', padx=10, pady=5)
        
        # Sample rate setting
        sample_frame = tk.Frame(audio_settings_frame, bg=self.colors['bg_secondary'])
        sample_frame.pack(fill='x', pady=5)
        
        ttk.Label(sample_frame, text="Sample Rate:",
                 style='Header.TLabel').pack(side='left')
        
        sample_combo = ttk.Combobox(sample_frame, values=["44100 Hz", "48000 Hz", "96000 Hz"],
                                   state='readonly', width=15)
        sample_combo.set("44100 Hz")
        sample_combo.pack(side='left', padx=(10, 0))
        
        # Buffer size setting
        buffer_frame = tk.Frame(audio_settings_frame, bg=self.colors['bg_secondary'])
        buffer_frame.pack(fill='x', pady=5)
        
        ttk.Label(buffer_frame, text="Buffer Size:",
                 style='Header.TLabel').pack(side='left')
        
        buffer_combo = ttk.Combobox(buffer_frame, values=["128", "256", "512", "1024"],
                                   state='readonly', width=15)
        buffer_combo.set("512")
        buffer_combo.pack(side='left', padx=(10, 0))
        
        # Bluetooth settings
        bt_settings_frame = tk.LabelFrame(self.settings_frame, text="Bluetooth Settings",
                                         bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                         font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        bt_settings_frame.pack(fill='x', padx=10, pady=5)
        
        # Connection timeout setting
        timeout_frame = tk.Frame(bt_settings_frame, bg=self.colors['bg_secondary'])
        timeout_frame.pack(fill='x', pady=5)
        
        ttk.Label(timeout_frame, text="Connection Timeout:",
                 style='Header.TLabel').pack(side='left')
        
        timeout_spin = ttk.Spinbox(timeout_frame, from_=5, to=60, width=10)
        timeout_spin.set("30")
        timeout_spin.pack(side='left', padx=(10, 0))
        
        ttk.Label(timeout_frame, text="seconds",
                 style='Status.TLabel').pack(side='left', padx=(5, 0))
        
        # About section
        about_frame = tk.LabelFrame(self.settings_frame, text="About",
                                   bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                   font=('Segoe UI', 12, 'bold'), pady=10, padx=10)
        about_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        about_text = tk.Text(about_frame, height=6, bg=self.colors['bg_secondary'],
                            fg=self.colors['text_primary'], font=('Segoe UI', 10),
                            wrap=tk.WORD, relief='flat')
        about_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        about_content = """Music Host by Nadeemal v1.0

Universal Audio Streaming Application
Stream any Windows audio to multiple Bluetooth devices simultaneously.

• Capture system audio from any application (YouTube, Spotify, games, etc.)
• Connect to multiple Bluetooth speakers and headphones
• Real-time audio streaming with low latency
• Professional interface with modern design

© 2024 Nadeemal. All rights reserved."""
        
        about_text.insert('1.0', about_content)
        about_text.configure(state='disabled')
        
    def create_status_bar(self):
        """Create bottom status bar."""
        self.status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=30)
        self.status_frame.pack(side='bottom', fill='x')
        self.status_frame.pack_propagate(False)
        
        # Status text
        self.status_label = ttk.Label(self.status_frame, text="Ready - Start by discovering Bluetooth devices",
                                     style='Status.TLabel')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Connection indicator
        self.connection_indicator = tk.Label(self.status_frame, text="●", 
                                           fg=self.colors['warning'], bg=self.colors['bg_secondary'],
                                           font=('Arial', 12))
        self.connection_indicator.pack(side='right', padx=10, pady=5)
        
        ttk.Label(self.status_frame, text="Status", style='Status.TLabel').pack(side='right', pady=5)
        
    def setup_layout(self):
        """Setup the main layout."""
        self.header_frame.pack(side='top', fill='x')
        self.main_frame.pack(side='top', fill='both', expand=True)
        
    # Event handlers and methods
    def discover_devices(self):
        """Start Bluetooth device discovery."""
        self.update_status("Discovering Bluetooth devices...")
        self.btn_discover.configure(state='disabled', text="🔍 Discovering...")
        
        # Start discovery in background thread
        threading.Thread(target=self._discover_devices_worker, daemon=True).start()
        
    def _discover_devices_worker(self):
        """Background worker for device discovery."""
        # Simulate device discovery
        discovered_devices = [
            ("JBL Charge 4", "Speaker", "Available", "Strong"),
            ("Sony WH-1000XM4", "Headphones", "Available", "Medium"),
            ("Samsung Galaxy Buds", "Earbuds", "Available", "Weak"),
            ("Bose SoundLink", "Speaker", "Paired", "Strong"),
            ("AirPods Pro", "Earbuds", "Available", "Medium")
        ]
        
        # Clear existing items
        self.root.after(0, lambda: self.available_tree.delete(*self.available_tree.get_children()))
        
        # Add discovered devices with delay for realistic effect
        for i, (name, device_type, status, signal) in enumerate(discovered_devices):
            time.sleep(0.5)  # Simulate discovery time
            self.root.after(0, lambda n=name, t=device_type, s=status, sig=signal: 
                          self.available_tree.insert('', 'end', text=n, values=(t, s, sig)))
        
        # Re-enable button
        self.root.after(0, lambda: [
            self.btn_discover.configure(state='normal', text="🔍 Discover Devices"),
            self.update_status(f"Found {len(discovered_devices)} Bluetooth devices")
        ])
        
    def refresh_devices(self):
        """Refresh device list."""
        self.discover_devices()
        
    def connect_device(self):
        """Connect to selected device."""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to connect.")
            return
            
        device_name = self.available_tree.item(selection[0])['text']
        self.update_status(f"Connecting to {device_name}...")
        
        # Simulate connection process
        threading.Thread(target=self._connect_device_worker, args=(device_name,), daemon=True).start()
        
    def _connect_device_worker(self, device_name):
        """Background worker for device connection."""
        time.sleep(2)  # Simulate connection time
        
        # Add to connected devices
        if device_name not in self.connected_devices:
            self.connected_devices.append(device_name)
            
            # Update UI
            self.root.after(0, lambda: [
                self.update_connected_devices_display(),
                self.update_status(f"Connected to {device_name}"),
                self.update_connection_indicator()
            ])
        
    def disconnect_device(self):
        """Disconnect selected device."""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to disconnect.")
            return
            
        device_name = self.available_tree.item(selection[0])['text']
        if device_name in self.connected_devices:
            self.connected_devices.remove(device_name)
            self.update_connected_devices_display()
            self.update_status(f"Disconnected from {device_name}")
            self.update_connection_indicator()
        
    def test_device_audio(self):
        """Test audio on selected device."""
        selection = self.available_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to test.")
            return
            
        device_name = self.available_tree.item(selection[0])['text']
        self.update_status(f"Testing audio on {device_name}...")
        
        # Simulate audio test
        threading.Thread(target=self._test_audio_worker, args=(device_name,), daemon=True).start()
        
    def _test_audio_worker(self, device_name):
        """Background worker for audio testing."""
        time.sleep(1)
        self.root.after(0, lambda: self.update_status(f"Audio test completed on {device_name}"))
        
    def start_streaming(self):
        """Start audio streaming to connected devices."""
        if not self.connected_devices:
            messagebox.showwarning("No Devices", "Please connect at least one device before streaming.")
            return
            
        self.is_streaming = True
        self.var_streaming_status.set("● Streaming")
        self.btn_start_streaming.configure(state='disabled')
        self.btn_stop_streaming.configure(state='normal')
        self.update_connection_indicator()
        
        self.update_status(f"Streaming to {len(self.connected_devices)} devices")
        
        # Start streaming worker
        threading.Thread(target=self._streaming_worker, daemon=True).start()
        
    def _streaming_worker(self):
        """Background worker for audio streaming."""
        while self.is_streaming:
            # Simulate audio capture and streaming
            self.root.after(0, lambda: self.var_current_audio.set("YouTube - Example Song"))
            time.sleep(1)
            
    def stop_streaming(self):
        """Stop audio streaming."""
        self.is_streaming = False
        self.var_streaming_status.set("● Stopped")
        self.btn_start_streaming.configure(state='normal')
        self.btn_stop_streaming.configure(state='disabled')
        self.var_current_audio.set("No audio detected")
        self.update_connection_indicator()
        
        self.update_status("Streaming stopped")
        
    def refresh_audio_sources(self):
        """Refresh available audio sources."""
        self.update_status("Refreshing audio sources...")
        
    def on_volume_change(self, value):
        """Handle volume slider change."""
        volume = int(float(value))
        self.volume_label.configure(text=f"{volume}%")
        
    def toggle_autostart(self):
        """Toggle Windows startup."""
        messagebox.showinfo("Auto-start", "Auto-start setting will be implemented in the final version.")
        
    def update_connected_devices_display(self):
        """Update the connected devices display."""
        # Clear current display
        for widget in self.connected_frame_inner.winfo_children():
            widget.destroy()
            
        # Add connected device cards
        for i, device in enumerate(self.connected_devices):
            device_card = tk.Frame(self.connected_frame_inner, bg=self.colors['bg_accent'], 
                                  relief='raised', bd=1)
            device_card.pack(side='left', padx=5, pady=5, fill='y')
            
            # Device info
            tk.Label(device_card, text=device, bg=self.colors['bg_accent'], 
                    fg='white', font=('Segoe UI', 10, 'bold')).pack(padx=10, pady=(5, 0))
            
            tk.Label(device_card, text="● Connected", bg=self.colors['bg_accent'], 
                    fg='lightgreen', font=('Segoe UI', 8)).pack(padx=10, pady=(0, 5))
            
        # Update count
        self.var_connected_count.set(str(len(self.connected_devices)))
        
    def update_connection_indicator(self):
        """Update the connection status indicator."""
        if self.is_streaming:
            self.connection_indicator.configure(fg=self.colors['success'])  # Green
        elif self.connected_devices:
            self.connection_indicator.configure(fg=self.colors['warning'])  # Orange
        else:
            self.connection_indicator.configure(fg=self.colors['danger'])   # Red
            
    def update_status(self, message):
        """Update status bar message."""
        self.status_label.configure(text=message)
        
        # Also add to audio info if streaming related
        if any(word in message.lower() for word in ['streaming', 'audio', 'connected', 'device']):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.audio_info_text.insert('end', f"[{timestamp}] {message}\n")
            self.audio_info_text.see('end')
            
    def load_settings(self):
        """Load application settings."""
        try:
            settings_file = Path("settings.json")
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    
                # Apply settings
                self.var_volume_level.set(settings.get('volume', 75))
                self.var_auto_connect.set(settings.get('auto_connect', True))
                self.var_system_tray.set(settings.get('system_tray', False))
        except Exception as e:
            print(f"Could not load settings: {e}")
            
    def save_settings(self):
        """Save application settings."""
        try:
            settings = {
                'volume': self.var_volume_level.get(),
                'auto_connect': self.var_auto_connect.get(),
                'system_tray': self.var_system_tray.get()
            }
            
            with open("settings.json", 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
            
    def on_closing(self):
        """Handle application closing."""
        self.save_settings()
        
        if self.var_system_tray.get():
            # Minimize to tray instead of closing
            self.root.withdraw()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        app = MusicHostGUI()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    main()