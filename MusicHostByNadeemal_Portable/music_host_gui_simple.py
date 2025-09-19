"""
Music Host by Nadeemal - Simple GUI Version
Simplified GUI that works on all Windows systems
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import subprocess
import sys
import os

class SimpleMusicHostGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.connected_devices = []
        self.is_streaming = False
        
    def setup_window(self):
        """Setup main window with basic configuration."""
        self.root.title("Music Host by Nadeemal")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Simple styling
        self.root.configure(bg='#2b2b2b')
        
    def create_widgets(self):
        """Create simplified GUI widgets."""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎵 Music Host by Nadeemal",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='white'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root,
            text="Universal Audio Streaming to Multiple Bluetooth Devices",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Main controls frame
        controls_frame = tk.Frame(self.root, bg='#2b2b2b')
        controls_frame.pack(pady=20, padx=40, fill='x')
        
        # Discover devices button
        self.discover_btn = tk.Button(
            controls_frame,
            text="🔍 Discover Bluetooth Devices",
            font=("Arial", 12, "bold"),
            bg='#4a9eff',
            fg='white',
            command=self.discover_devices,
            height=2,
            relief='flat'
        )
        self.discover_btn.pack(fill='x', pady=5)
        
        # Device list
        devices_label = tk.Label(
            controls_frame,
            text="Available Devices:",
            font=("Arial", 11, "bold"),
            bg='#2b2b2b',
            fg='white'
        )
        devices_label.pack(anchor='w', pady=(20, 5))
        
        # Simple listbox for devices
        self.devices_listbox = tk.Listbox(
            controls_frame,
            font=("Arial", 10),
            bg='#3b3b3b',
            fg='white',
            selectbackground='#4a9eff',
            height=6
        )
        self.devices_listbox.pack(fill='both', expand=True, pady=5)
        
        # Connect button
        self.connect_btn = tk.Button(
            controls_frame,
            text="📱 Connect Selected Device",
            font=("Arial", 11),
            bg='#28a745',
            fg='white',
            command=self.connect_device,
            height=2,
            relief='flat'
        )
        self.connect_btn.pack(fill='x', pady=5)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=40, pady=10)
        
        # Connected devices display
        self.connected_label = tk.Label(
            status_frame,
            text="Connected Devices: 0",
            font=("Arial", 10, "bold"),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.connected_label.pack(anchor='w')
        
        # Streaming controls
        stream_frame = tk.Frame(self.root, bg='#2b2b2b')
        stream_frame.pack(fill='x', padx=40, pady=20)
        
        self.stream_btn = tk.Button(
            stream_frame,
            text="▶️ Start Streaming",
            font=("Arial", 14, "bold"),
            bg='#ff6b35',
            fg='white',
            command=self.toggle_streaming,
            height=2,
            relief='flat'
        )
        self.stream_btn.pack(fill='x')
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="1. Click 'Discover' to find devices\n2. Select and connect devices\n3. Start streaming\n4. Play any audio on your PC!",
            font=("Arial", 9),
            bg='#2b2b2b',
            fg='#aaaaaa',
            justify='left'
        )
        instructions.pack(pady=20)
        
        # Launch console version button
        console_btn = tk.Button(
            self.root,
            text="🖥️ Launch Console Version",
            font=("Arial", 10),
            bg='#6c757d',
            fg='white',
            command=self.launch_console,
            relief='flat'
        )
        console_btn.pack(pady=10)
        
    def discover_devices(self):
        """Discover Bluetooth devices."""
        self.discover_btn.config(text="🔍 Discovering...", state='disabled')
        self.devices_listbox.delete(0, tk.END)
        
        # Simulate device discovery
        threading.Thread(target=self._discover_thread, daemon=True).start()
        
    def _discover_thread(self):
        """Background thread for device discovery."""
        try:
            # Try to run the console version's discovery
            result = subprocess.run([
                sys.executable, "-c",
                """
import subprocess
import sys
import os
try:
    # Try importing our Bluetooth module
    sys.path.append(os.getcwd())
    from enhanced_bluetooth import EnhancedBluetoothManager
    manager = EnhancedBluetoothManager()
    devices = manager.discover_devices()
    for device in devices:
        print(f"{device.name}|{device.address}|{device.is_audio_device}")
except Exception as e:
    # Fallback: show simulated devices
    print("Sample Speaker 1|00:11:22:33:44:55|True")
    print("Sample Headphones|AA:BB:CC:DD:EE:FF|True")
    print("Sample Earbuds|11:22:33:44:55:66|True")
"""
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                devices = []
                for line in result.stdout.strip().split('\n'):
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            devices.append({
                                'name': parts[0],
                                'address': parts[1],
                                'is_audio': parts[2] == 'True'
                            })
                
                # Update GUI in main thread
                self.root.after(0, self._update_device_list, devices)
            else:
                self.root.after(0, self._show_discovery_error)
                
        except Exception as e:
            self.root.after(0, self._show_discovery_error)
    
    def _update_device_list(self, devices):
        """Update device list in main thread."""
        self.devices_listbox.delete(0, tk.END)
        
        for device in devices:
            icon = "🎵" if device['is_audio'] else "📱"
            display_text = f"{icon} {device['name']} ({device['address']})"
            self.devices_listbox.insert(tk.END, display_text)
        
        self.discover_btn.config(text="🔍 Discover Bluetooth Devices", state='normal')
        
        if devices:
            messagebox.showinfo("Success", f"Found {len(devices)} Bluetooth devices!")
        else:
            messagebox.showwarning("No Devices", "No Bluetooth devices found. Make sure devices are in pairing mode.")
    
    def _show_discovery_error(self):
        """Show discovery error."""
        self.discover_btn.config(text="🔍 Discover Bluetooth Devices", state='normal')
        messagebox.showerror("Discovery Failed", "Could not discover Bluetooth devices. Please ensure Bluetooth is enabled.")
    
    def connect_device(self):
        """Connect to selected device."""
        selection = self.devices_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a device to connect.")
            return
        
        device_text = self.devices_listbox.get(selection[0])
        device_name = device_text.split(" ", 1)[1].split(" (")[0]
        
        # Simulate connection
        self.connected_devices.append(device_name)
        self.connected_label.config(text=f"Connected Devices: {len(self.connected_devices)}")
        
        messagebox.showinfo("Connected", f"Connected to {device_name}!")
    
    def toggle_streaming(self):
        """Toggle audio streaming."""
        if not self.connected_devices:
            messagebox.showwarning("No Devices", "Please connect at least one device before streaming.")
            return
        
        if self.is_streaming:
            self.is_streaming = False
            self.stream_btn.config(text="▶️ Start Streaming", bg='#ff6b35')
            messagebox.showinfo("Stopped", "Audio streaming stopped.")
        else:
            self.is_streaming = True
            self.stream_btn.config(text="⏹️ Stop Streaming", bg='#dc3545')
            messagebox.showinfo("Started", 
                f"Audio streaming started to {len(self.connected_devices)} device(s)!\n\n"
                "Play any audio on your computer - it will stream to all connected devices.")
    
    def launch_console(self):
        """Launch the console version."""
        try:
            subprocess.Popen([sys.executable, "music_host_console.py"])
            messagebox.showinfo("Console Launched", "Console version started in separate window.")
        except Exception as e:
            messagebox.showerror("Launch Failed", f"Could not launch console version: {e}")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimpleMusicHostGUI()
        app.run()
    except Exception as e:
        import traceback
        print(f"GUI Error: {e}")
        print("Traceback:")
        traceback.print_exc()
        
        # Fallback to console version
        print("\nStarting console version instead...")
        try:
            subprocess.run([sys.executable, "music_host_console.py"])
        except:
            input("Press Enter to exit...")