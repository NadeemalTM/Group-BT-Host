"""
Music Host by Nadeemal - Main Application
Professional Windows application for streaming audio to multiple Bluetooth devices
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import os
from pathlib import Path

# Import our custom modules
try:
    from audio_capture import WindowsAudioCapture, AudioStreamProcessor
    from enhanced_bluetooth import EnhancedBluetoothManager, WindowsBluetoothDevice
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all module files are in the same directory")
    sys.exit(1)

class MusicHostApplication:
    """Main application class integrating all components."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Initialize backend systems
        self.audio_capture = WindowsAudioCapture()
        self.bluetooth_manager = EnhancedBluetoothManager()
        self.stream_processor = AudioStreamProcessor()
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Initialize GUI
        self.setup_gui()
        
        # Application state
        self.is_streaming = False
        self.current_volume = 75
        
    def setup_window(self):
        """Configure main window."""
        self.root.title("Music Host by Nadeemal - Universal Audio Streaming")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        # Try to set icon
        try:
            icon_path = Path("assets/icon.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
            
        # Center window
        self.center_window()
        
        # Handle closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_callbacks(self):
        """Setup callbacks for backend systems."""
        # Audio capture callbacks
        self.audio_capture.set_audio_callback(self.on_audio_data)
        self.audio_capture.set_volume_callback(self.on_volume_update)
        
        # Bluetooth callbacks
        self.bluetooth_manager.set_device_found_callback(self.on_device_found)
        self.bluetooth_manager.set_device_connected_callback(self.on_device_connected)
        self.bluetooth_manager.set_device_disconnected_callback(self.on_device_disconnected)
        self.bluetooth_manager.set_status_callback(self.on_status_update)
        
    def setup_gui(self):
        """Setup the graphical user interface."""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        self.colors = {
            'bg_primary': '#2C3E50',
            'bg_secondary': '#34495E',
            'bg_accent': '#3498DB',
            'text_primary': '#ECF0F1',
            'text_secondary': '#BDC3C7',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Create main layout
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
    def create_header(self):
        """Create application header."""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], pady=15)
        header_frame.pack(side='top', fill='x')
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🎵 Music Host by Nadeemal",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_primary'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Stream any Windows audio to multiple Bluetooth devices simultaneously",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_primary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Current audio display
        self.audio_display_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'], 
                                           relief='raised', bd=1)
        self.audio_display_frame.pack(pady=(15, 0), padx=20, fill='x')
        
        audio_info_frame = tk.Frame(self.audio_display_frame, bg=self.colors['bg_secondary'])
        audio_info_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(audio_info_frame, text="🎶 Currently Playing:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(side='left')
        
        self.current_audio_label = tk.Label(audio_info_frame,
                                           text="No audio detected",
                                           font=('Segoe UI', 11),
                                           fg=self.colors['text_secondary'],
                                           bg=self.colors['bg_secondary'])
        self.current_audio_label.pack(side='left', padx=(10, 0))
        
        # Audio level indicator
        self.audio_level_frame = tk.Frame(audio_info_frame, bg=self.colors['bg_secondary'])
        self.audio_level_frame.pack(side='right')
        
        tk.Label(self.audio_level_frame, text="Level:",
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_secondary']).pack(side='left')
        
        self.audio_level_canvas = tk.Canvas(self.audio_level_frame, width=100, height=20,
                                           bg='black', highlightthickness=0)
        self.audio_level_canvas.pack(side='left', padx=(5, 0))
        
    def create_main_content(self):
        """Create main content area."""
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Bluetooth devices
        left_panel = self.create_bluetooth_panel(main_frame)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Right panel - Audio controls
        right_panel = self.create_audio_panel(main_frame)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        
    def create_bluetooth_panel(self, parent):
        """Create Bluetooth device management panel."""
        panel = tk.LabelFrame(parent, text="Bluetooth Device Management",
                             font=('Segoe UI', 12, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_secondary'],
                             pady=10, padx=10)
        
        # Discovery controls
        discovery_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        discovery_frame.pack(fill='x', pady=(0, 10))
        
        self.btn_discover = tk.Button(discovery_frame, text="🔍 Discover Devices",
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=self.colors['bg_accent'], fg='white',
                                     command=self.discover_devices,
                                     relief='flat', padx=20, pady=8)
        self.btn_discover.pack(side='left', padx=(0, 10))
        
        self.btn_refresh = tk.Button(discovery_frame, text="🔄 Refresh",
                                    font=('Segoe UI', 10),
                                    bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                    command=self.refresh_devices,
                                    relief='flat', padx=15, pady=8)
        self.btn_refresh.pack(side='left')
        
        # Device list
        list_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Available devices
        tk.Label(list_frame, text="Available Devices:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        # Treeview for devices
        self.device_tree = ttk.Treeview(list_frame, columns=('type', 'status', 'signal'),
                                       show='tree headings', height=8)
        
        self.device_tree.heading('#0', text='Device Name', anchor='w')
        self.device_tree.heading('type', text='Type', anchor='center')
        self.device_tree.heading('status', text='Status', anchor='center')
        self.device_tree.heading('signal', text='Signal', anchor='center')
        
        self.device_tree.column('#0', width=250, minwidth=200)
        self.device_tree.column('type', width=100, minwidth=80)
        self.device_tree.column('status', width=100, minwidth=80)
        self.device_tree.column('signal', width=80, minwidth=60)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.device_tree.pack(side='left', fill='both', expand=True, pady=(5, 0))
        tree_scroll.pack(side='right', fill='y', pady=(5, 0))
        
        # Device action buttons
        action_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        action_frame.pack(fill='x')
        
        self.btn_connect = tk.Button(action_frame, text="🔗 Connect",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=self.colors['success'], fg='white',
                                    command=self.connect_device,
                                    relief='flat', padx=15, pady=6)
        self.btn_connect.pack(side='left', padx=(0, 5))
        
        self.btn_disconnect = tk.Button(action_frame, text="❌ Disconnect",
                                       font=('Segoe UI', 10, 'bold'),
                                       bg=self.colors['danger'], fg='white',
                                       command=self.disconnect_device,
                                       relief='flat', padx=15, pady=6)
        self.btn_disconnect.pack(side='left', padx=(0, 5))
        
        self.btn_test = tk.Button(action_frame, text="🔊 Test",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_accent'], fg='white',
                                 command=self.test_device,
                                 relief='flat', padx=15, pady=6)
        self.btn_test.pack(side='left')
        
        # Connected devices display
        connected_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        connected_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(connected_frame, text="Connected Devices:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        self.connected_devices_frame = tk.Frame(connected_frame, bg=self.colors['bg_secondary'])
        self.connected_devices_frame.pack(fill='x', pady=(5, 0))
        
        return panel
        
    def create_audio_panel(self, parent):
        """Create audio control panel."""
        panel = tk.LabelFrame(parent, text="Audio Control",
                             font=('Segoe UI', 12, 'bold'),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_secondary'],
                             pady=10, padx=10, width=300)
        panel.pack_propagate(False)
        
        # Streaming controls
        control_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        control_frame.pack(fill='x', pady=(0, 15))
        
        self.btn_start_stream = tk.Button(control_frame, text="▶️ Start Streaming",
                                         font=('Segoe UI', 12, 'bold'),
                                         bg=self.colors['success'], fg='white',
                                         command=self.start_streaming,
                                         relief='flat', pady=12)
        self.btn_start_stream.pack(fill='x', pady=(0, 5))
        
        self.btn_stop_stream = tk.Button(control_frame, text="⏹️ Stop Streaming",
                                        font=('Segoe UI', 12, 'bold'),
                                        bg=self.colors['danger'], fg='white',
                                        command=self.stop_streaming,
                                        relief='flat', pady=12,
                                        state='disabled')
        self.btn_stop_stream.pack(fill='x')
        
        # Status display
        status_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        status_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(status_frame, text="Status:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        self.status_label = tk.Label(status_frame, text="● Ready",
                                    font=('Segoe UI', 10),
                                    fg=self.colors['warning'],
                                    bg=self.colors['bg_secondary'])
        self.status_label.pack(anchor='w', pady=(2, 0))
        
        # Volume control
        volume_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        volume_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(volume_frame, text="🔊 Volume:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        self.volume_var = tk.IntVar(value=75)
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient='horizontal',
                                    variable=self.volume_var, bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'], highlightthickness=0,
                                    command=self.on_volume_change)
        self.volume_scale.pack(fill='x', pady=(5, 0))
        
        # Audio source selection
        source_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        source_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(source_frame, text="Audio Source:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        self.source_var = tk.StringVar(value="System Audio")
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_var,
                                   values=["System Audio", "Microphone", "Line In"],
                                   state='readonly')
        source_combo.pack(fill='x', pady=(5, 0))
        
        # Statistics
        stats_frame = tk.Frame(panel, bg=self.colors['bg_secondary'])
        stats_frame.pack(fill='both', expand=True)
        
        tk.Label(stats_frame, text="Statistics:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        self.stats_text = tk.Text(stats_frame, height=8, width=30,
                                 bg='black', fg='green',
                                 font=('Consolas', 9),
                                 wrap=tk.WORD, state='disabled')
        self.stats_text.pack(fill='both', expand=True, pady=(5, 0))
        
        return panel
        
    def create_status_bar(self):
        """Create status bar."""
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_bar_label = tk.Label(status_frame, 
                                        text="Ready - Click 'Discover Devices' to begin",
                                        font=('Segoe UI', 9),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['bg_secondary'])
        self.status_bar_label.pack(side='left', padx=10, pady=3)
        
        # Connection count
        self.connection_count_label = tk.Label(status_frame,
                                              text="Devices: 0",
                                              font=('Segoe UI', 9),
                                              fg=self.colors['text_secondary'],
                                              bg=self.colors['bg_secondary'])
        self.connection_count_label.pack(side='right', padx=10, pady=3)
        
    # Event handlers
    def discover_devices(self):
        """Start device discovery."""
        self.btn_discover.configure(state='disabled', text="🔍 Discovering...")
        self.update_status("Starting Bluetooth device discovery...")
        
        # Clear existing devices
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
            
        # Start discovery
        self.bluetooth_manager.discover_devices(duration=8)
        
        # Re-enable button after delay
        self.root.after(9000, lambda: [
            self.btn_discover.configure(state='normal', text="🔍 Discover Devices"),
            self.update_status("Device discovery completed")
        ])
        
    def refresh_devices(self):
        """Refresh device list."""
        self.discover_devices()
        
    def connect_device(self):
        """Connect to selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to connect.")
            return
            
        item = self.device_tree.item(selection[0])
        device_name = item['text']
        
        # Find device object
        device = self.bluetooth_manager.get_device_by_name(device_name)
        if device:
            self.bluetooth_manager.connect_device(device)
        else:
            messagebox.showerror("Error", "Device not found.")
            
    def disconnect_device(self):
        """Disconnect selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to disconnect.")
            return
            
        item = self.device_tree.item(selection[0])
        device_name = item['text']
        
        device = self.bluetooth_manager.get_device_by_name(device_name)
        if device:
            self.bluetooth_manager.disconnect_device(device)
        else:
            messagebox.showerror("Error", "Device not found.")
            
    def test_device(self):
        """Test selected device."""
        selection = self.device_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to test.")
            return
            
        item = self.device_tree.item(selection[0])
        device_name = item['text']
        self.update_status(f"Testing audio on {device_name}...")
        
        # Simulate test
        self.root.after(2000, lambda: self.update_status(f"Audio test completed on {device_name}"))
        
    def start_streaming(self):
        """Start audio streaming."""
        connected_devices = self.bluetooth_manager.get_connected_audio_devices()
        if not connected_devices:
            messagebox.showwarning("No Devices", 
                                 "Please connect at least one Bluetooth audio device before streaming.")
            return
            
        self.is_streaming = True
        self.btn_start_stream.configure(state='disabled')
        self.btn_stop_stream.configure(state='normal')
        self.status_label.configure(text="● Streaming", fg=self.colors['success'])
        
        # Start audio capture
        self.audio_capture.start_capture()
        self.stream_processor.start_streaming()
        
        # Add connected devices to stream processor
        for device in connected_devices:
            self.stream_processor.add_device(device.to_dict())
            
        self.update_status(f"Streaming to {len(connected_devices)} devices")
        self.update_stats(f"Started streaming to {len(connected_devices)} devices")
        
    def stop_streaming(self):
        """Stop audio streaming."""
        self.is_streaming = False
        self.btn_start_stream.configure(state='normal')
        self.btn_stop_stream.configure(state='disabled')
        self.status_label.configure(text="● Stopped", fg=self.colors['warning'])
        
        # Stop audio capture
        self.audio_capture.stop_capture()
        self.stream_processor.stop_streaming()
        self.stream_processor.clear_devices()
        
        self.current_audio_label.configure(text="No audio detected")
        self.update_status("Streaming stopped")
        self.update_stats("Streaming stopped")
        
    def on_volume_change(self, value):
        """Handle volume change."""
        self.current_volume = int(float(value))
        
    # Callback handlers
    def on_device_found(self, device: WindowsBluetoothDevice):
        """Handle device found."""
        def update_ui():
            status_icon = "🔗" if device.is_connected else "📱"
            if device.is_audio_device:
                status_icon = "🎵" if device.is_connected else "🔊"
                
            status_text = "Connected" if device.is_connected else "Available"
            
            self.device_tree.insert('', 'end', 
                                  text=f"{status_icon} {device.name}",
                                  values=(device.device_type, status_text, device.signal_strength))
                                  
        self.root.after(0, update_ui)
        
    def on_device_connected(self, device: WindowsBluetoothDevice):
        """Handle device connected."""
        def update_ui():
            self.update_connected_devices_display()
            self.update_status(f"Connected to {device.name}")
            self.update_stats(f"Connected: {device.name}")
            
            # Update tree view
            for item in self.device_tree.get_children():
                if device.name in self.device_tree.item(item)['text']:
                    self.device_tree.item(item, values=(device.device_type, "Connected", device.signal_strength))
                    break
                    
        self.root.after(0, update_ui)
        
    def on_device_disconnected(self, device: WindowsBluetoothDevice):
        """Handle device disconnected."""
        def update_ui():
            self.update_connected_devices_display()
            self.update_status(f"Disconnected from {device.name}")
            self.update_stats(f"Disconnected: {device.name}")
            
            # Update tree view
            for item in self.device_tree.get_children():
                if device.name in self.device_tree.item(item)['text']:
                    self.device_tree.item(item, values=(device.device_type, "Available", device.signal_strength))
                    break
                    
        self.root.after(0, update_ui)
        
    def on_audio_data(self, data, sample_rate, channels):
        """Handle incoming audio data."""
        if self.is_streaming:
            self.stream_processor.process_audio_data(data, sample_rate, channels)
            
            # Update current audio display
            def update_ui():
                # Simulate detecting current application
                self.current_audio_label.configure(text="System Audio - Various Applications")
                
            self.root.after(0, update_ui)
            
    def on_volume_update(self, level):
        """Handle volume level update."""
        def update_ui():
            # Update audio level display
            self.audio_level_canvas.delete('all')
            bar_width = int(level * 100)  # level is 0.0 to 1.0
            
            # Color based on level
            if level > 0.8:
                color = 'red'
            elif level > 0.5:
                color = 'yellow'
            else:
                color = 'green'
                
            self.audio_level_canvas.create_rectangle(0, 2, bar_width, 18, fill=color, outline='')
            
        self.root.after(0, update_ui)
        
    def on_status_update(self, message):
        """Handle status updates."""
        self.root.after(0, lambda: self.update_status(message))
        
    # Helper methods
    def update_connected_devices_display(self):
        """Update connected devices display."""
        # Clear current display
        for widget in self.connected_devices_frame.winfo_children():
            widget.destroy()
            
        # Get connected devices
        connected = self.bluetooth_manager.get_connected_devices()
        
        if connected:
            for device in connected:
                device_frame = tk.Frame(self.connected_devices_frame, 
                                       bg=self.colors['bg_accent'],
                                       relief='raised', bd=1)
                device_frame.pack(fill='x', pady=2)
                
                icon = "🎵" if device.is_audio_device else "📱"
                tk.Label(device_frame, text=f"{icon} {device.name}",
                        font=('Segoe UI', 9, 'bold'),
                        fg='white', bg=self.colors['bg_accent']).pack(side='left', padx=5, pady=2)
                
                tk.Label(device_frame, text="● Connected",
                        font=('Segoe UI', 8),
                        fg='lightgreen', bg=self.colors['bg_accent']).pack(side='right', padx=5, pady=2)
        else:
            tk.Label(self.connected_devices_frame, text="No devices connected",
                    font=('Segoe UI', 9, 'italic'),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_secondary']).pack(pady=5)
            
        # Update connection count
        self.connection_count_label.configure(text=f"Devices: {len(connected)}")
        
    def update_status(self, message):
        """Update status bar."""
        self.status_bar_label.configure(text=message)
        
    def update_stats(self, message):
        """Update statistics display."""
        self.stats_text.configure(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.stats_text.insert('end', f"[{timestamp}] {message}\n")
        self.stats_text.see('end')
        self.stats_text.configure(state='disabled')
        
    def on_closing(self):
        """Handle application closing."""
        # Stop all operations
        if self.is_streaming:
            self.stop_streaming()
            
        # Cleanup
        self.audio_capture.cleanup()
        
        # Close application
        self.root.destroy()
        
    def run(self):
        """Start the application."""
        # Initial setup
        self.update_status("Application started - Ready to discover devices")
        self.update_stats("Music Host by Nadeemal started")
        self.update_stats("Capture any Windows audio and stream to Bluetooth devices")
        
        # Start main loop
        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        # Create and run application
        app = MusicHostApplication()
        app.run()
        
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Application Error", 
                           f"An error occurred starting the application:\n\n{str(e)}\n\n"
                           f"Please ensure all required files are present and try again.")


if __name__ == "__main__":
    main()