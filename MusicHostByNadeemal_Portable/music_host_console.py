"""
Music Host by Nadeemal - Console Version
Professional console application for streaming audio to multiple Bluetooth devices
Works without GUI dependencies
"""

import os
import sys
import time
import threading
import json
from datetime import datetime

# Import our backend modules
try:
    from audio_capture import WindowsAudioCapture, AudioStreamProcessor
    from enhanced_bluetooth import EnhancedBluetoothManager, WindowsBluetoothDevice
except ImportError as e:
    print(f"Import error: {e}")
    print("Some modules not found, using simulation mode")
    
    # Create stub classes for missing modules
    class WindowsAudioCapture:
        def __init__(self): pass
        def set_audio_callback(self, cb): pass
        def set_volume_callback(self, cb): pass
        def start_capture(self): return True
        def stop_capture(self): pass
        def cleanup(self): pass
        def get_current_level(self): return 0.5
        
    class AudioStreamProcessor:
        def __init__(self): pass
        def add_device(self, device): pass
        def remove_device(self, device): pass
        def start_streaming(self): pass
        def stop_streaming(self): pass
        def clear_devices(self): pass
        
    class WindowsBluetoothDevice:
        def __init__(self, name, addr, dev_type="Speaker", connected=False):
            self.name = name
            self.address = addr
            self.device_type = dev_type
            self.is_connected = connected
            self.is_audio_device = True
            
        def to_dict(self):
            return {"name": self.name, "address": self.address}
            
    class EnhancedBluetoothManager:
        def __init__(self): 
            self.devices = []
            self.connected_devices = []
            
        def set_device_found_callback(self, cb): self.device_found_cb = cb
        def set_device_connected_callback(self, cb): self.device_connected_cb = cb
        def set_device_disconnected_callback(self, cb): self.device_disconnected_cb = cb
        def set_status_callback(self, cb): self.status_cb = cb
        
        def discover_devices(self, duration=5):
            self.devices = [
                WindowsBluetoothDevice("JBL Charge 4", "XX:XX:XX:XX:XX:01"),
                WindowsBluetoothDevice("Sony WH-1000XM4", "XX:XX:XX:XX:XX:02"),
                WindowsBluetoothDevice("Samsung Galaxy Buds", "XX:XX:XX:XX:XX:03"),
                WindowsBluetoothDevice("AirPods Pro", "XX:XX:XX:XX:XX:04"),
            ]
            return self.devices
            
        def get_device_by_name(self, name):
            for device in self.devices:
                if device.name == name:
                    return device
            return None
            
        def connect_device(self, device):
            if device not in self.connected_devices:
                self.connected_devices.append(device)
                device.is_connected = True
            return True
            
        def disconnect_device(self, device):
            if device in self.connected_devices:
                self.connected_devices.remove(device)
                device.is_connected = False
            return True
            
        def get_connected_devices(self):
            return self.connected_devices
            
        def get_connected_audio_devices(self):
            return [d for d in self.connected_devices if d.is_audio_device]


class ConsoleMusicHost:
    """Console-based Music Host application."""
    
    def __init__(self):
        self.running = True
        self.is_streaming = False
        self.current_volume = 75
        
        # Initialize backend systems
        self.audio_capture = WindowsAudioCapture()
        self.bluetooth_manager = EnhancedBluetoothManager()
        self.stream_processor = AudioStreamProcessor()
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Statistics
        self.stats = {
            'start_time': datetime.now(),
            'devices_discovered': 0,
            'devices_connected': 0,
            'streaming_time': 0,
            'audio_level': 0.0
        }
        
    def setup_callbacks(self):
        """Setup callbacks for backend systems."""
        self.bluetooth_manager.set_device_found_callback(self.on_device_found)
        self.bluetooth_manager.set_device_connected_callback(self.on_device_connected)
        self.bluetooth_manager.set_device_disconnected_callback(self.on_device_disconnected)
        self.bluetooth_manager.set_status_callback(self.on_status_update)
        
    def clear_screen(self):
        """Clear console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        """Print application header."""
        print("=" * 80)
        print("🎵 MUSIC HOST BY NADEEMAL - UNIVERSAL AUDIO STREAMING")
        print("=" * 80)
        print("Stream any Windows audio to multiple Bluetooth devices simultaneously")
        print(f"Started: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Current status
        status = "🔴 Stopped"
        if self.is_streaming:
            status = "🟢 Streaming"
            
        connected_count = len(self.bluetooth_manager.get_connected_devices())
        print(f"Status: {status} | Connected Devices: {connected_count} | Volume: {self.current_volume}%")
        print("=" * 80)
        
    def print_menu(self):
        """Print main menu."""
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1. 🔍 Discover Bluetooth Devices")
        print("2. 📱 Show Available Devices") 
        print("3. 🔗 Connect to Device")
        print("4. ❌ Disconnect Device")
        print("5. 📋 Show Connected Devices")
        print("6. ▶️  Start Audio Streaming")
        print("7. ⏹️  Stop Audio Streaming")
        print("8. 🔊 Adjust Volume")
        print("9. 📊 Show Statistics")
        print("10. ⚙️ Settings")
        print("0. 🚪 Exit")
        print("-" * 40)
        
    def discover_devices(self):
        """Discover Bluetooth devices."""
        print("\n🔍 DISCOVERING BLUETOOTH DEVICES")
        print("-" * 40)
        print("Scanning for nearby Bluetooth audio devices...")
        
        # Start discovery
        devices = self.bluetooth_manager.discover_devices(duration=3)
        
        # Simulate discovery progress
        for i in range(3):
            print(f"Scanning... {i+1}/3")
            time.sleep(1)
            
        self.stats['devices_discovered'] = len(devices)
        
        print(f"\n✅ Discovery completed! Found {len(devices)} devices:")
        for i, device in enumerate(devices, 1):
            status = "🟢 Connected" if device.is_connected else "⚪ Available"
            audio_icon = "🎵" if device.is_audio_device else "📱"
            print(f"  {i}. {audio_icon} {device.name} ({device.device_type}) - {status}")
            
        input("\nPress Enter to continue...")
        
    def show_available_devices(self):
        """Show available devices."""
        print("\n📱 AVAILABLE BLUETOOTH DEVICES")
        print("-" * 40)
        
        devices = self.bluetooth_manager.devices
        if not devices:
            print("No devices found. Please discover devices first.")
        else:
            for i, device in enumerate(devices, 1):
                status = "🟢 Connected" if device.is_connected else "⚪ Available"
                audio_icon = "🎵" if device.is_audio_device else "📱"
                print(f"  {i}. {audio_icon} {device.name}")
                print(f"     Type: {device.device_type}")
                print(f"     Status: {status}")
                print(f"     Address: {device.address}")
                print()
                
        input("Press Enter to continue...")
        
    def connect_device(self):
        """Connect to a device."""
        print("\n🔗 CONNECT TO DEVICE")
        print("-" * 40)
        
        devices = [d for d in self.bluetooth_manager.devices if not d.is_connected]
        if not devices:
            print("No available devices to connect. Please discover devices first.")
            input("Press Enter to continue...")
            return
            
        print("Available devices:")
        for i, device in enumerate(devices, 1):
            audio_icon = "🎵" if device.is_audio_device else "📱"
            print(f"  {i}. {audio_icon} {device.name} ({device.device_type})")
            
        try:
            choice = input("\nEnter device number to connect (or Enter to cancel): ").strip()
            if not choice:
                return
                
            device_index = int(choice) - 1
            if 0 <= device_index < len(devices):
                device = devices[device_index]
                print(f"\n🔄 Connecting to {device.name}...")
                
                # Simulate connection time
                for i in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)
                    
                success = self.bluetooth_manager.connect_device(device)
                if success:
                    print(f"\n✅ Successfully connected to {device.name}!")
                    self.stats['devices_connected'] += 1
                else:
                    print(f"\n❌ Failed to connect to {device.name}")
            else:
                print("Invalid device number.")
                
        except (ValueError, IndexError):
            print("Invalid input.")
            
        input("\nPress Enter to continue...")
        
    def disconnect_device(self):
        """Disconnect from a device."""
        print("\n❌ DISCONNECT DEVICE")
        print("-" * 40)
        
        connected_devices = self.bluetooth_manager.get_connected_devices()
        if not connected_devices:
            print("No connected devices.")
            input("Press Enter to continue...")
            return
            
        print("Connected devices:")
        for i, device in enumerate(connected_devices, 1):
            audio_icon = "🎵" if device.is_audio_device else "📱"
            print(f"  {i}. {audio_icon} {device.name} ({device.device_type})")
            
        try:
            choice = input("\nEnter device number to disconnect (or Enter to cancel): ").strip()
            if not choice:
                return
                
            device_index = int(choice) - 1
            if 0 <= device_index < len(connected_devices):
                device = connected_devices[device_index]
                print(f"\n🔄 Disconnecting from {device.name}...")
                time.sleep(1)
                
                success = self.bluetooth_manager.disconnect_device(device)
                if success:
                    print(f"✅ Successfully disconnected from {device.name}")
                else:
                    print(f"❌ Failed to disconnect from {device.name}")
            else:
                print("Invalid device number.")
                
        except (ValueError, IndexError):
            print("Invalid input.")
            
        input("\nPress Enter to continue...")
        
    def show_connected_devices(self):
        """Show connected devices."""
        print("\n📋 CONNECTED DEVICES")
        print("-" * 40)
        
        connected_devices = self.bluetooth_manager.get_connected_devices()
        audio_devices = self.bluetooth_manager.get_connected_audio_devices()
        
        if not connected_devices:
            print("No devices are currently connected.")
        else:
            print(f"Total connected: {len(connected_devices)}")
            print(f"Audio devices: {len(audio_devices)}")
            print()
            
            for i, device in enumerate(connected_devices, 1):
                audio_icon = "🎵" if device.is_audio_device else "📱"
                streaming_status = "🔊 Streaming" if self.is_streaming and device.is_audio_device else "⚪ Ready"
                print(f"  {i}. {audio_icon} {device.name}")
                print(f"     Type: {device.device_type}")
                print(f"     Status: {streaming_status}")
                print()
                
        input("Press Enter to continue...")
        
    def start_streaming(self):
        """Start audio streaming."""
        print("\n▶️ START AUDIO STREAMING")
        print("-" * 40)
        
        audio_devices = self.bluetooth_manager.get_connected_audio_devices()
        if not audio_devices:
            print("❌ No audio devices connected!")
            print("Please connect at least one Bluetooth audio device before streaming.")
            input("\nPress Enter to continue...")
            return
            
        if self.is_streaming:
            print("⚠️ Streaming is already active.")
            input("Press Enter to continue...")
            return
            
        print(f"🎯 Target devices ({len(audio_devices)}):")
        for device in audio_devices:
            print(f"  🎵 {device.name}")
            
        print(f"\n🔊 Volume level: {self.current_volume}%")
        print("🎶 Audio source: System Audio (all Windows applications)")
        
        confirm = input("\nStart streaming? (Y/n): ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            print("\n🚀 Starting audio streaming...")
            
            # Start streaming
            self.is_streaming = True
            self.audio_capture.start_capture()
            self.stream_processor.start_streaming()
            
            # Add devices to stream processor
            for device in audio_devices:
                self.stream_processor.add_device(device.to_dict())
                
            print("✅ Streaming started successfully!")
            print("\n🎵 Now playing audio from any Windows application will be")
            print("   streamed to all connected Bluetooth devices simultaneously.")
            print("\n📱 Applications that will be captured:")
            print("   • YouTube in web browsers")
            print("   • Spotify, iTunes, Windows Media Player")
            print("   • Games with audio")
            print("   • Video calls (Zoom, Teams, etc.)")
            print("   • Any other audio-playing application")
            
            self.streaming_start_time = time.time()
            
        input("\nPress Enter to continue...")
        
    def stop_streaming(self):
        """Stop audio streaming."""
        print("\n⏹️ STOP AUDIO STREAMING")
        print("-" * 40)
        
        if not self.is_streaming:
            print("⚠️ Streaming is not currently active.")
            input("Press Enter to continue...")
            return
            
        print("🛑 Stopping audio streaming...")
        
        # Stop streaming
        self.is_streaming = False
        self.audio_capture.stop_capture()
        self.stream_processor.stop_streaming()
        self.stream_processor.clear_devices()
        
        if hasattr(self, 'streaming_start_time'):
            duration = time.time() - self.streaming_start_time
            self.stats['streaming_time'] += duration
            print(f"📊 Streaming duration: {duration:.1f} seconds")
            
        print("✅ Streaming stopped successfully.")
        input("\nPress Enter to continue...")
        
    def adjust_volume(self):
        """Adjust volume."""
        print("\n🔊 ADJUST VOLUME")
        print("-" * 40)
        print(f"Current volume: {self.current_volume}%")
        
        try:
            new_volume = input("Enter new volume (0-100) or Enter to cancel: ").strip()
            if not new_volume:
                return
                
            volume = int(new_volume)
            if 0 <= volume <= 100:
                self.current_volume = volume
                print(f"✅ Volume set to {self.current_volume}%")
            else:
                print("❌ Volume must be between 0 and 100")
                
        except ValueError:
            print("❌ Invalid volume value")
            
        input("\nPress Enter to continue...")
        
    def show_statistics(self):
        """Show application statistics."""
        print("\n📊 STATISTICS")
        print("-" * 40)
        
        uptime = datetime.now() - self.stats['start_time']
        
        print(f"⏰ Uptime: {uptime}")
        print(f"🔍 Devices discovered: {self.stats['devices_discovered']}")
        print(f"🔗 Devices connected: {self.stats['devices_connected']}")
        print(f"🎵 Total streaming time: {self.stats['streaming_time']:.1f} seconds")
        print(f"📊 Current audio level: {self.audio_capture.get_current_level():.2f}")
        print(f"🔊 Current volume: {self.current_volume}%")
        print(f"📱 Connected devices: {len(self.bluetooth_manager.get_connected_devices())}")
        print(f"🎵 Audio devices: {len(self.bluetooth_manager.get_connected_audio_devices())}")
        print(f"▶️ Streaming status: {'Active' if self.is_streaming else 'Stopped'}")
        
        if self.is_streaming:
            print("\n🎶 Currently streaming to:")
            for device in self.bluetooth_manager.get_connected_audio_devices():
                print(f"   • {device.name}")
                
        input("\nPress Enter to continue...")
        
    def show_settings(self):
        """Show settings menu."""
        print("\n⚙️ SETTINGS")
        print("-" * 40)
        print("1. 🔊 Audio Source: System Audio")
        print("2. 📡 Bluetooth: Enabled")
        print("3. 🎵 Audio Quality: High (44.1kHz)")
        print("4. 🔄 Auto-reconnect: Enabled")
        print("5. 📝 Save Device List")
        print("6. 📁 Load Device List")
        print("0. ← Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "5":
            try:
                devices_data = [device.to_dict() for device in self.bluetooth_manager.devices]
                with open("music_host_devices.json", 'w') as f:
                    json.dump(devices_data, f, indent=2)
                print("✅ Device list saved successfully!")
            except Exception as e:
                print(f"❌ Failed to save device list: {e}")
                
        elif choice == "6":
            try:
                if os.path.exists("music_host_devices.json"):
                    with open("music_host_devices.json", 'r') as f:
                        devices_data = json.load(f)
                    print(f"✅ Loaded {len(devices_data)} devices from file")
                else:
                    print("❌ No saved device list found")
            except Exception as e:
                print(f"❌ Failed to load device list: {e}")
                
        input("\nPress Enter to continue...")
        
    # Callback handlers
    def on_device_found(self, device):
        """Handle device found."""
        pass
        
    def on_device_connected(self, device):
        """Handle device connected."""
        pass
        
    def on_device_disconnected(self, device):
        """Handle device disconnected.""" 
        pass
        
    def on_status_update(self, message):
        """Handle status updates."""
        pass
        
    def run(self):
        """Main application loop."""
        try:
            while self.running:
                self.clear_screen()
                self.print_header()
                self.print_menu()
                
                choice = input("\nEnter your choice (0-10): ").strip()
                
                if choice == "0":
                    self.running = False
                elif choice == "1":
                    self.discover_devices()
                elif choice == "2":
                    self.show_available_devices()
                elif choice == "3":
                    self.connect_device()
                elif choice == "4":
                    self.disconnect_device()
                elif choice == "5":
                    self.show_connected_devices()
                elif choice == "6":
                    self.start_streaming()
                elif choice == "7":
                    self.stop_streaming()
                elif choice == "8":
                    self.adjust_volume()
                elif choice == "9":
                    self.show_statistics()
                elif choice == "10":
                    self.show_settings()
                else:
                    print("\n❌ Invalid choice. Please try again.")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Application interrupted by user")
            
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Cleanup on exit."""
        if self.is_streaming:
            print("\n🛑 Stopping streaming...")
            self.stop_streaming()
            
        print("\n👋 Thank you for using Music Host by Nadeemal!")
        print("🎶 Enjoy sharing your music with friends!")
        self.audio_capture.cleanup()


def main():
    """Main entry point."""
    try:
        app = ConsoleMusicHost()
        app.run()
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        print("Please check that all required files are present and try again.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()