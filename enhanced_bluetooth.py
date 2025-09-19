"""
Enhanced Bluetooth Manager for Windows
Manages Bluetooth device discovery, connection, and audio streaming
"""

import subprocess
import json
import threading
import time
import re
from typing import List, Dict, Optional, Callable
import os
import winreg

class WindowsBluetoothDevice:
    """Represents a Bluetooth device on Windows."""
    
    def __init__(self, name: str, address: str, device_type: str = "Unknown", is_connected: bool = False):
        self.name = name
        self.address = address
        self.device_type = device_type
        self.is_connected = is_connected
        self.is_audio_device = self._is_audio_device()
        self.signal_strength = "Unknown"
        self.last_seen = time.time()
        
    def _is_audio_device(self) -> bool:
        """Determine if this is an audio device based on name/type."""
        audio_keywords = [
            'speaker', 'headphone', 'headset', 'earphone', 'earbud', 'airpod',
            'beats', 'bose', 'sony', 'jbl', 'audio', 'sound', 'music'
        ]
        
        name_lower = self.name.lower()
        type_lower = self.device_type.lower()
        
        return any(keyword in name_lower or keyword in type_lower for keyword in audio_keywords)
        
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'address': self.address,
            'type': self.device_type,
            'is_connected': self.is_connected,
            'is_audio_device': self.is_audio_device,
            'signal_strength': self.signal_strength,
            'last_seen': self.last_seen
        }
        
    def __str__(self):
        return f"{self.name} ({self.address}) - {'Connected' if self.is_connected else 'Available'}"


class EnhancedBluetoothManager:
    """Enhanced Bluetooth manager for Windows with audio focus."""
    
    def __init__(self):
        self.devices: List[WindowsBluetoothDevice] = []
        self.connected_devices: List[WindowsBluetoothDevice] = []
        self.is_discovering = False
        self.discovery_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self.device_found_callback: Optional[Callable] = None
        self.device_connected_callback: Optional[Callable] = None
        self.device_disconnected_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        
        self._check_bluetooth_support()
        
    def _check_bluetooth_support(self):
        """Check if Bluetooth is available on the system."""
        try:
            # Check if Bluetooth service is running
            result = subprocess.run(['sc', 'query', 'bthserv'], 
                                  capture_output=True, text=True, timeout=5)
            self.bluetooth_available = 'RUNNING' in result.stdout
        except Exception:
            self.bluetooth_available = False
            
        if not self.bluetooth_available:
            self._log("Warning: Bluetooth service not detected. Using simulation mode.")
            
    def set_device_found_callback(self, callback: Callable):
        """Set callback for when a device is found."""
        self.device_found_callback = callback
        
    def set_device_connected_callback(self, callback: Callable):
        """Set callback for when a device connects."""
        self.device_connected_callback = callback
        
    def set_device_disconnected_callback(self, callback: Callable):
        """Set callback for when a device disconnects."""
        self.device_disconnected_callback = callback
        
    def set_status_callback(self, callback: Callable):
        """Set callback for status updates."""
        self.status_callback = callback
        
    def _log(self, message: str):
        """Log message and call status callback if available."""
        print(f"[BluetoothManager] {message}")
        if self.status_callback:
            self.status_callback(message)
            
    def discover_devices(self, duration: int = 10) -> List[WindowsBluetoothDevice]:
        """Start discovering Bluetooth devices."""
        if self.is_discovering:
            self._log("Discovery already in progress")
            return self.devices
            
        self.is_discovering = True
        self.devices.clear()
        
        self._log("Starting Bluetooth device discovery...")
        
        if self.bluetooth_available:
            self.discovery_thread = threading.Thread(
                target=self._real_discovery_worker, 
                args=(duration,), 
                daemon=True
            )
        else:
            self.discovery_thread = threading.Thread(
                target=self._simulated_discovery_worker, 
                args=(duration,), 
                daemon=True
            )
            
        self.discovery_thread.start()
        return self.devices
        
    def _real_discovery_worker(self, duration: int):
        """Real Bluetooth discovery using Windows commands."""
        try:
            # Use PowerShell to discover Bluetooth devices
            ps_script = """
            Add-Type -AssemblyName System.Runtime.WindowsRuntime
            $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
            Function Await($WinRtTask, $ResultType) {
                $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                $netTask = $asTask.Invoke($null, @($WinRtTask))
                $netTask.Wait(-1) | Out-Null
                $netTask.Result
            }
            
            [Windows.Devices.Bluetooth.BluetoothAdapter,Windows.Devices.Bluetooth,ContentType=WindowsRuntime] | Out-Null
            [Windows.Devices.Bluetooth.BluetoothDevice,Windows.Devices.Bluetooth,ContentType=WindowsRuntime] | Out-Null
            [Windows.Devices.Enumeration.DeviceInformation,Windows.Devices.Enumeration,ContentType=WindowsRuntime] | Out-Null
            
            $adapter = Await ([Windows.Devices.Bluetooth.BluetoothAdapter]::GetDefaultAsync()) ([Windows.Devices.Bluetooth.BluetoothAdapter])
            if ($adapter) {
                $devices = Await ($adapter.GetDevicesAsync()) ([Windows.Devices.Enumeration.DeviceInformationCollection])
                foreach ($device in $devices) {
                    Write-Output "$($device.Name)|$($device.Id)|Unknown|false"
                }
            }
            """
            
            # Run PowerShell script
            result = subprocess.run(['powershell', '-Command', ps_script], 
                                  capture_output=True, text=True, timeout=duration)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            name = parts[0].strip()
                            device_id = parts[1].strip()
                            device_type = parts[2].strip()
                            is_connected = parts[3].strip().lower() == 'true'
                            
                            if name and name != "None":
                                device = WindowsBluetoothDevice(name, device_id, device_type, is_connected)
                                self.devices.append(device)
                                
                                if self.device_found_callback:
                                    self.device_found_callback(device)
                                    
            else:
                # Fall back to simulated discovery
                self._log("PowerShell discovery failed, using simulation")
                self._simulated_discovery_devices()
                
        except Exception as e:
            self._log(f"Real discovery failed: {e}, using simulation")
            self._simulated_discovery_devices()
            
        self.is_discovering = False
        self._log(f"Discovery completed. Found {len(self.devices)} devices")
        
    def _simulated_discovery_worker(self, duration: int):
        """Simulated discovery for testing when Bluetooth isn't available."""
        self._log("Using simulated Bluetooth discovery")
        
        # Simulate discovery time
        total_steps = 8
        step_time = duration / total_steps
        
        simulated_devices = [
            ("JBL Charge 4", "XX:XX:XX:XX:XX:01", "Speaker", False),
            ("Sony WH-1000XM4", "XX:XX:XX:XX:XX:02", "Headphones", False),
            ("Samsung Galaxy Buds", "XX:XX:XX:XX:XX:03", "Earbuds", False),
            ("Bose SoundLink Mini", "XX:XX:XX:XX:XX:04", "Speaker", False),
            ("AirPods Pro", "XX:XX:XX:XX:XX:05", "Earbuds", True),
            ("Beats Studio3", "XX:XX:XX:XX:XX:06", "Headphones", False),
            ("JBL Flip 5", "XX:XX:XX:XX:XX:07", "Speaker", False),
            ("Anker Soundcore", "XX:XX:XX:XX:XX:08", "Speaker", False)
        ]
        
        for i, (name, address, device_type, is_connected) in enumerate(simulated_devices):
            if not self.is_discovering:
                break
                
            device = WindowsBluetoothDevice(name, address, device_type, is_connected)
            device.signal_strength = ["Weak", "Medium", "Strong"][i % 3]
            
            self.devices.append(device)
            
            if is_connected:
                self.connected_devices.append(device)
                
            self._log(f"Discovered: {name}")
            
            if self.device_found_callback:
                self.device_found_callback(device)
                
            time.sleep(step_time)
            
        self.is_discovering = False
        self._log(f"Simulated discovery completed. Found {len(self.devices)} devices")
        
    def _simulated_discovery_devices(self):
        """Add simulated devices immediately."""
        simulated_devices = [
            ("JBL Charge 4", "XX:XX:XX:XX:XX:01", "Speaker", False),
            ("Sony WH-1000XM4", "XX:XX:XX:XX:XX:02", "Headphones", False),
            ("Samsung Galaxy Buds", "XX:XX:XX:XX:XX:03", "Earbuds", False),
        ]
        
        for name, address, device_type, is_connected in simulated_devices:
            device = WindowsBluetoothDevice(name, address, device_type, is_connected)
            self.devices.append(device)
            
            if self.device_found_callback:
                self.device_found_callback(device)
                
    def connect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Connect to a Bluetooth device."""
        if device.is_connected:
            self._log(f"{device.name} is already connected")
            return True
            
        self._log(f"Connecting to {device.name}...")
        
        # Start connection in background thread
        threading.Thread(target=self._connect_worker, args=(device,), daemon=True).start()
        return True
        
    def _connect_worker(self, device: WindowsBluetoothDevice):
        """Background worker for device connection."""
        try:
            if self.bluetooth_available:
                success = self._real_connect_device(device)
            else:
                success = self._simulated_connect_device(device)
                
            if success:
                device.is_connected = True
                if device not in self.connected_devices:
                    self.connected_devices.append(device)
                    
                self._log(f"Successfully connected to {device.name}")
                
                if self.device_connected_callback:
                    self.device_connected_callback(device)
            else:
                self._log(f"Failed to connect to {device.name}")
                
        except Exception as e:
            self._log(f"Connection error for {device.name}: {e}")
            
    def _real_connect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Real device connection using Windows Bluetooth stack."""
        try:
            # Use Windows Bluetooth commands to connect
            # This is a simplified approach - real implementation would be more complex
            
            if device.is_audio_device:
                # For audio devices, try to connect using audio profile
                cmd = ['bluetoothctl', 'connect', device.address]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                return result.returncode == 0
            else:
                # For other devices, use general connection
                return False  # Not implemented for non-audio devices
                
        except Exception as e:
            self._log(f"Real connection failed: {e}")
            return False
            
    def _simulated_connect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Simulate device connection."""
        # Simulate connection delay
        time.sleep(2)
        
        # Simulate 90% success rate for audio devices, 50% for others
        import random
        success_rate = 0.9 if device.is_audio_device else 0.5
        return random.random() < success_rate
        
    def disconnect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Disconnect from a Bluetooth device."""
        if not device.is_connected:
            self._log(f"{device.name} is not connected")
            return True
            
        self._log(f"Disconnecting from {device.name}...")
        
        # Start disconnection in background thread
        threading.Thread(target=self._disconnect_worker, args=(device,), daemon=True).start()
        return True
        
    def _disconnect_worker(self, device: WindowsBluetoothDevice):
        """Background worker for device disconnection."""
        try:
            if self.bluetooth_available:
                success = self._real_disconnect_device(device)
            else:
                success = self._simulated_disconnect_device(device)
                
            if success:
                device.is_connected = False
                if device in self.connected_devices:
                    self.connected_devices.remove(device)
                    
                self._log(f"Successfully disconnected from {device.name}")
                
                if self.device_disconnected_callback:
                    self.device_disconnected_callback(device)
            else:
                self._log(f"Failed to disconnect from {device.name}")
                
        except Exception as e:
            self._log(f"Disconnection error for {device.name}: {e}")
            
    def _real_disconnect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Real device disconnection."""
        try:
            cmd = ['bluetoothctl', 'disconnect', device.address]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False
            
    def _simulated_disconnect_device(self, device: WindowsBluetoothDevice) -> bool:
        """Simulate device disconnection."""
        time.sleep(1)
        return True  # Disconnection usually succeeds
        
    def get_connected_devices(self) -> List[WindowsBluetoothDevice]:
        """Get list of connected devices."""
        return self.connected_devices.copy()
        
    def get_audio_devices(self) -> List[WindowsBluetoothDevice]:
        """Get list of audio-capable devices."""
        return [device for device in self.devices if device.is_audio_device]
        
    def get_connected_audio_devices(self) -> List[WindowsBluetoothDevice]:
        """Get list of connected audio devices."""
        return [device for device in self.connected_devices if device.is_audio_device]
        
    def stop_discovery(self):
        """Stop device discovery."""
        self.is_discovering = False
        self._log("Discovery stopped")
        
    def refresh_device_status(self):
        """Refresh the connection status of all devices."""
        self._log("Refreshing device status...")
        
        for device in self.devices:
            # In real implementation, this would check actual connection status
            # For simulation, we'll keep current status
            pass
            
    def send_audio_to_device(self, device: WindowsBluetoothDevice, audio_data: bytes) -> bool:
        """Send audio data to a specific device."""
        if not device.is_connected or not device.is_audio_device:
            return False
            
        # In real implementation, this would send audio via Bluetooth A2DP
        # For simulation, just return success
        return True
        
    def send_audio_to_all(self, audio_data: bytes) -> int:
        """Send audio data to all connected audio devices."""
        success_count = 0
        
        for device in self.get_connected_audio_devices():
            if self.send_audio_to_device(device, audio_data):
                success_count += 1
                
        return success_count
        
    def get_device_by_address(self, address: str) -> Optional[WindowsBluetoothDevice]:
        """Find device by Bluetooth address."""
        for device in self.devices:
            if device.address == address:
                return device
        return None
        
    def get_device_by_name(self, name: str) -> Optional[WindowsBluetoothDevice]:
        """Find device by name."""
        for device in self.devices:
            if device.name == name:
                return device
        return None
        
    def save_known_devices(self, filename: str = "known_devices.json"):
        """Save known devices to file."""
        try:
            devices_data = [device.to_dict() for device in self.devices]
            with open(filename, 'w') as f:
                json.dump(devices_data, f, indent=2)
            self._log(f"Saved {len(devices_data)} devices to {filename}")
        except Exception as e:
            self._log(f"Failed to save devices: {e}")
            
    def load_known_devices(self, filename: str = "known_devices.json") -> bool:
        """Load known devices from file."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    devices_data = json.load(f)
                    
                self.devices.clear()
                for data in devices_data:
                    device = WindowsBluetoothDevice(
                        data['name'], 
                        data['address'], 
                        data['type'], 
                        data.get('is_connected', False)
                    )
                    device.signal_strength = data.get('signal_strength', 'Unknown')
                    device.last_seen = data.get('last_seen', time.time())
                    self.devices.append(device)
                    
                self._log(f"Loaded {len(self.devices)} devices from {filename}")
                return True
        except Exception as e:
            self._log(f"Failed to load devices: {e}")
            
        return False


# Test the Bluetooth manager
if __name__ == "__main__":
    def on_device_found(device):
        print(f"Found: {device}")
        
    def on_device_connected(device):
        print(f"Connected: {device}")
        
    def on_device_disconnected(device):
        print(f"Disconnected: {device}")
        
    def on_status(message):
        print(f"Status: {message}")
        
    # Test the manager
    manager = EnhancedBluetoothManager()
    manager.set_device_found_callback(on_device_found)
    manager.set_device_connected_callback(on_device_connected)
    manager.set_device_disconnected_callback(on_device_disconnected)
    manager.set_status_callback(on_status)
    
    print("Starting discovery...")
    manager.discover_devices(duration=5)
    
    # Wait for discovery to complete
    time.sleep(6)
    
    print(f"\nFound {len(manager.devices)} devices:")
    for device in manager.devices:
        print(f"  {device}")
        
    # Test connecting to first audio device
    audio_devices = manager.get_audio_devices()
    if audio_devices:
        print(f"\nConnecting to {audio_devices[0].name}...")
        manager.connect_device(audio_devices[0])
        time.sleep(3)
        
    print(f"\nConnected devices: {len(manager.get_connected_devices())}")
    for device in manager.get_connected_devices():
        print(f"  {device}")
        
    # Save devices
    manager.save_known_devices()