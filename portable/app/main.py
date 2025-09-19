"""
Bluetooth Multi-Device Music Player
A Windows application to stream music to multiple connected Bluetooth devices simultaneously.

Main Features:
- Discover and connect to multiple Bluetooth audio devices
- Play music files to all connected devices
- Synchronize audio playback across devices
- User-friendly GUI interface
- Volume control and playback controls

Author: Python Software Developer
Version: 1.0
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pygame
import time
from bluetooth_manager import BluetoothManager
from audio_engine import AudioEngine
from gui_components import MusicPlayerGUI

class BluetoothMusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bluetooth Multi-Device Music Player")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize components
        self.bluetooth_manager = BluetoothManager()
        self.audio_engine = AudioEngine()
        self.gui = MusicPlayerGUI(self.root, self)
        
        # Application state
        self.connected_devices = {}
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        
        # Setup window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def discover_devices(self):
        """Discover available Bluetooth audio devices."""
        try:
            self.gui.update_status("Discovering Bluetooth devices...")
            devices = self.bluetooth_manager.discover_audio_devices()
            self.gui.update_device_list(devices)
            self.gui.update_status(f"Found {len(devices)} Bluetooth audio devices")
            return devices
        except Exception as e:
            messagebox.showerror("Error", f"Failed to discover devices: {str(e)}")
            self.gui.update_status("Device discovery failed")
            return []
    
    def connect_device(self, device_address, device_name):
        """Connect to a specific Bluetooth device."""
        try:
            if device_address not in self.connected_devices:
                success = self.bluetooth_manager.connect_device(device_address)
                if success:
                    self.connected_devices[device_address] = {
                        'name': device_name,
                        'connected': True
                    }
                    self.gui.update_connected_devices(self.connected_devices)
                    self.gui.update_status(f"Connected to {device_name}")
                    return True
                else:
                    messagebox.showerror("Connection Error", f"Failed to connect to {device_name}")
                    return False
            else:
                messagebox.showinfo("Info", f"{device_name} is already connected")
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
            return False
    
    def disconnect_device(self, device_address):
        """Disconnect from a specific Bluetooth device."""
        try:
            if device_address in self.connected_devices:
                success = self.bluetooth_manager.disconnect_device(device_address)
                if success:
                    device_name = self.connected_devices[device_address]['name']
                    del self.connected_devices[device_address]
                    self.gui.update_connected_devices(self.connected_devices)
                    self.gui.update_status(f"Disconnected from {device_name}")
                    return True
                else:
                    messagebox.showerror("Error", "Failed to disconnect device")
                    return False
        except Exception as e:
            messagebox.showerror("Error", f"Disconnection failed: {str(e)}")
            return False
    
    def load_music_file(self):
        """Load a music file for playback."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Music File",
                filetypes=[
                    ("Audio Files", "*.mp3 *.wav *.ogg *.m4a"),
                    ("MP3 Files", "*.mp3"),
                    ("WAV Files", "*.wav"),
                    ("OGG Files", "*.ogg"),
                    ("All Files", "*.*")
                ]
            )
            
            if file_path:
                self.current_song = file_path
                song_name = os.path.basename(file_path)
                self.gui.update_current_song(song_name)
                self.audio_engine.load_file(file_path)
                self.gui.update_status(f"Loaded: {song_name}")
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load music file: {str(e)}")
            return False
    
    def play_music(self):
        """Start playing music to all connected devices."""
        try:
            if not self.current_song:
                messagebox.showwarning("Warning", "Please load a music file first")
                return
            
            if not self.connected_devices:
                messagebox.showwarning("Warning", "Please connect at least one Bluetooth device")
                return
            
            if self.is_paused:
                self.audio_engine.resume()
                self.is_paused = False
            else:
                self.audio_engine.play(list(self.connected_devices.keys()))
            
            self.is_playing = True
            self.gui.update_playback_controls(True)
            self.gui.update_status("Playing music to connected devices")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play music: {str(e)}")
    
    def pause_music(self):
        """Pause music playback."""
        try:
            self.audio_engine.pause()
            self.is_playing = False
            self.is_paused = True
            self.gui.update_playback_controls(False)
            self.gui.update_status("Music paused")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pause music: {str(e)}")
    
    def stop_music(self):
        """Stop music playback."""
        try:
            self.audio_engine.stop()
            self.is_playing = False
            self.is_paused = False
            self.gui.update_playback_controls(False)
            self.gui.update_status("Music stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop music: {str(e)}")
    
    def set_volume(self, volume):
        """Set playback volume (0-100)."""
        try:
            self.audio_engine.set_volume(volume / 100.0)
            self.gui.update_status(f"Volume set to {volume}%")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set volume: {str(e)}")
    
    def on_closing(self):
        """Handle application closing."""
        try:
            # Stop any playing music
            if self.is_playing:
                self.stop_music()
            
            # Disconnect all devices
            for device_address in list(self.connected_devices.keys()):
                self.disconnect_device(device_address)
            
            # Cleanup
            self.audio_engine.cleanup()
            self.bluetooth_manager.cleanup()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.root.destroy()
    
    def run(self):
        """Start the application."""
        try:
            # Initialize pygame mixer
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            
            # Start the GUI
            self.gui.update_status("Application started - Click 'Discover Devices' to begin")
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application: {str(e)}")
            sys.exit(1)

def main():
    """Main entry point."""
    try:
        app = BluetoothMusicPlayer()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()