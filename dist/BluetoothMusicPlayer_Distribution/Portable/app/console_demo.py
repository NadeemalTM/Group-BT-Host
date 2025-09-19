"""
Bluetooth Multi-Device Music Player - Console Version
A command-line version that works without GUI libraries.
"""

import os
import sys
import time
import threading

class ConsoleBluetoothMusicPlayer:
    """Console-based version that doesn't require Tkinter."""
    
    def __init__(self):
        self.mock_devices = [
            {"name": "Bluetooth Speaker 1", "address": "00:11:22:33:44:55", "has_audio": True},
            {"name": "Wireless Headphones", "address": "AA:BB:CC:DD:EE:FF", "has_audio": True},
            {"name": "Bluetooth Earbuds", "address": "11:22:33:44:55:66", "has_audio": True}
        ]
        self.connected_devices = {}
        self.current_file = None
        self.is_playing = False
        
    def display_menu(self):
        """Display the main menu."""
        print("\\n" + "="*50)
        print("🎵 BLUETOOTH MULTI-DEVICE MUSIC PLAYER")
        print("="*50)
        print("1. Discover Bluetooth Devices")
        print("2. Connect to Device")
        print("3. Disconnect Device")
        print("4. Show Connected Devices")
        print("5. Load Music File")
        print("6. Play Music")
        print("7. Pause Music")
        print("8. Stop Music")
        print("9. Show Current Song")
        print("0. Exit")
        print("="*50)
        
    def discover_devices(self):
        """Simulate device discovery."""
        print("\\n🔍 Discovering Bluetooth devices...")
        print("Please wait...")
        
        # Simulate discovery time
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(1)
        
        print("\\n\\n📱 Found Bluetooth Devices:")
        print("-" * 40)
        for i, device in enumerate(self.mock_devices, 1):
            status = "🔗 Connected" if device['address'] in self.connected_devices else "⚪ Available"
            print(f"{i}. {device['name']}")
            print(f"   Address: {device['address']}")
            print(f"   Status: {status}")
            print()
    
    def connect_device(self):
        """Connect to a selected device."""
        self.discover_devices()
        
        try:
            choice = input("\\nEnter device number to connect (1-3): ").strip()
            device_num = int(choice)
            
            if 1 <= device_num <= len(self.mock_devices):
                device = self.mock_devices[device_num - 1]
                
                if device['address'] not in self.connected_devices:
                    print(f"\\n🔗 Connecting to {device['name']}...")
                    time.sleep(2)  # Simulate connection time
                    
                    self.connected_devices[device['address']] = device
                    print(f"✅ Successfully connected to {device['name']}!")
                else:
                    print(f"\\n⚠️ {device['name']} is already connected")
            else:
                print("\\n❌ Invalid device number")
                
        except ValueError:
            print("\\n❌ Please enter a valid number")
    
    def disconnect_device(self):
        """Disconnect from a selected device."""
        if not self.connected_devices:
            print("\\n⚠️ No devices connected")
            return
        
        print("\\n📱 Connected Devices:")
        print("-" * 30)
        devices_list = list(self.connected_devices.values())
        for i, device in enumerate(devices_list, 1):
            print(f"{i}. {device['name']} ({device['address']})")
        
        try:
            choice = input("\\nEnter device number to disconnect: ").strip()
            device_num = int(choice)
            
            if 1 <= device_num <= len(devices_list):
                device = devices_list[device_num - 1]
                print(f"\\n🔌 Disconnecting from {device['name']}...")
                time.sleep(1)
                
                del self.connected_devices[device['address']]
                print(f"✅ Disconnected from {device['name']}")
            else:
                print("\\n❌ Invalid device number")
                
        except ValueError:
            print("\\n❌ Please enter a valid number")
    
    def show_connected_devices(self):
        """Show all connected devices."""
        if not self.connected_devices:
            print("\\n⚠️ No devices connected")
            print("Use option 2 to connect devices first")
        else:
            print("\\n🔗 Connected Devices:")
            print("-" * 30)
            for device in self.connected_devices.values():
                print(f"📱 {device['name']}")
                print(f"   Address: {device['address']}")
                print()
    
    def load_music_file(self):
        """Simulate loading a music file."""
        print("\\n🎵 Load Music File")
        print("(In the GUI version, this would open a file browser)")
        
        # Simulate file selection
        sample_files = [
            "My Favorite Song.mp3",
            "Party Mix 2024.wav",
            "Relaxing Music.ogg",
            "Dance Track.m4a"
        ]
        
        print("\\nSample music files:")
        for i, file in enumerate(sample_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = input("\\nSelect a file (1-4) or enter custom name: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(sample_files):
                self.current_file = sample_files[int(choice) - 1]
            else:
                self.current_file = choice if choice else "Custom Song.mp3"
            
            print(f"\\n✅ Loaded: {self.current_file}")
            
        except Exception as e:
            print(f"\\n❌ Error loading file: {e}")
    
    def play_music(self):
        """Simulate playing music."""
        if not self.current_file:
            print("\\n⚠️ No music file loaded")
            print("Use option 5 to load a music file first")
            return
        
        if not self.connected_devices:
            print("\\n⚠️ No devices connected")
            print("Use option 2 to connect devices first")
            return
        
        device_count = len(self.connected_devices)
        print(f"\\n🎵 Playing '{self.current_file}'")
        print(f"📡 Streaming to {device_count} connected device(s):")
        
        for device in self.connected_devices.values():
            print(f"   🔊 {device['name']}")
        
        self.is_playing = True
        print("\\n✅ Music is now playing on all connected devices!")
        print("🎶 Your friends can now hear the same music simultaneously!")
    
    def pause_music(self):
        """Simulate pausing music."""
        if self.is_playing:
            self.is_playing = False
            print("\\n⏸️ Music paused on all devices")
        else:
            print("\\n⚠️ No music is currently playing")
    
    def stop_music(self):
        """Simulate stopping music."""
        if self.is_playing:
            self.is_playing = False
            print("\\n⏹️ Music stopped on all devices")
        else:
            print("\\n⚠️ No music is currently playing")
    
    def show_current_song(self):
        """Show current song info."""
        if self.current_file:
            status = "🎵 Playing" if self.is_playing else "⏸️ Loaded"
            print(f"\\n{status}: {self.current_file}")
            
            if self.connected_devices:
                print(f"📡 Streaming to {len(self.connected_devices)} device(s)")
            else:
                print("⚠️ No devices connected")
        else:
            print("\\n📭 No music file loaded")
    
    def run(self):
        """Main application loop."""
        print("🎵 Welcome to Bluetooth Multi-Device Music Player!")
        print("This demo simulates connecting to multiple Bluetooth devices")
        print("and playing music to all of them simultaneously.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\\nEnter your choice (0-9): ").strip()
                
                if choice == "1":
                    self.discover_devices()
                elif choice == "2":
                    self.connect_device()
                elif choice == "3":
                    self.disconnect_device()
                elif choice == "4":
                    self.show_connected_devices()
                elif choice == "5":
                    self.load_music_file()
                elif choice == "6":
                    self.play_music()
                elif choice == "7":
                    self.pause_music()
                elif choice == "8":
                    self.stop_music()
                elif choice == "9":
                    self.show_current_song()
                elif choice == "0":
                    print("\\n👋 Thanks for using Bluetooth Music Player!")
                    print("🎶 Enjoy sharing music with your friends!")
                    break
                else:
                    print("\\n❌ Invalid choice. Please enter 0-9.")
                
                input("\\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\\n\\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\\n❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point."""
    try:
        app = ConsoleBluetoothMusicPlayer()
        app.run()
    except Exception as e:
        print(f"❌ Application error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()