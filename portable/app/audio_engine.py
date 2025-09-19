"""
Audio Engine Module
Handles audio file loading, playback, and streaming to multiple Bluetooth devices.
"""

import pygame
import threading
import time
import os
from typing import List, Optional
import wave
import struct
import numpy as np
from mutagen import File
import io

class AudioEngine:
    def __init__(self):
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        self.playback_thread = None
        self.stop_event = threading.Event()
        
        # Audio properties
        self.sample_rate = 44100
        self.channels = 2
        self.bit_depth = 16
        
        # Synchronization
        self.sync_delay = 0.0  # Compensation for Bluetooth latency
        
    def load_file(self, file_path: str) -> bool:
        """Load an audio file for playback."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")
            
            self.current_file = file_path
            
            # Get audio file metadata
            audio_info = self._get_audio_info(file_path)
            print(f"Loaded audio file: {os.path.basename(file_path)}")
            print(f"Duration: {audio_info.get('duration', 'Unknown')}")
            print(f"Bitrate: {audio_info.get('bitrate', 'Unknown')}")
            
            # Load the file into pygame mixer
            pygame.mixer.music.load(file_path)
            
            return True
            
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False
    
    def _get_audio_info(self, file_path: str) -> dict:
        """Get metadata information from audio file."""
        try:
            audio_file = File(file_path)
            if audio_file is not None:
                return {
                    'duration': f"{int(audio_file.info.length // 60)}:{int(audio_file.info.length % 60):02d}",
                    'bitrate': f"{getattr(audio_file.info, 'bitrate', 'Unknown')} kbps",
                    'sample_rate': getattr(audio_file.info, 'sample_rate', 'Unknown'),
                    'channels': getattr(audio_file.info, 'channels', 'Unknown')
                }
        except:
            pass
        return {'duration': 'Unknown', 'bitrate': 'Unknown'}
    
    def play(self, device_addresses: List[str]) -> bool:
        """Start playing audio to specified Bluetooth devices."""
        try:
            if not self.current_file:
                raise ValueError("No audio file loaded")
            
            if self.is_playing:
                self.stop()
            
            self.stop_event.clear()
            self.is_playing = True
            self.is_paused = False
            
            # Start playback thread
            self.playback_thread = threading.Thread(
                target=self._playback_worker,
                args=(device_addresses,),
                daemon=True
            )
            self.playback_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting playback: {e}")
            return False
    
    def _playback_worker(self, device_addresses: List[str]):
        """Worker thread for audio playback."""
        try:
            # Apply synchronization delay for Bluetooth devices
            if self.sync_delay > 0:
                time.sleep(self.sync_delay)
            
            # Start pygame mixer playback
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            # Monitor playback
            while self.is_playing and not self.stop_event.is_set():
                if not pygame.mixer.music.get_busy() and not self.is_paused:
                    # Music finished playing
                    self.is_playing = False
                    break
                
                time.sleep(0.1)
            
            # Stream audio data to Bluetooth devices
            self._stream_to_bluetooth_devices(device_addresses)
            
        except Exception as e:
            print(f"Error in playback worker: {e}")
            self.is_playing = False
    
    def _stream_to_bluetooth_devices(self, device_addresses: List[str]):
        """Stream audio data to multiple Bluetooth devices simultaneously."""
        try:
            # This is where we would implement actual Bluetooth audio streaming
            # For now, we'll simulate the process
            
            print(f"Streaming audio to {len(device_addresses)} Bluetooth devices")
            
            # In a real implementation, this would:
            # 1. Read audio data from the current file
            # 2. Convert to appropriate format for Bluetooth A2DP
            # 3. Send data packets to each connected device
            # 4. Handle synchronization and buffering
            
            for device_address in device_addresses:
                print(f"Streaming to device: {device_address}")
                # Simulate audio streaming
                threading.Thread(
                    target=self._device_stream_worker,
                    args=(device_address,),
                    daemon=True
                ).start()
                
        except Exception as e:
            print(f"Error streaming to Bluetooth devices: {e}")
    
    def _device_stream_worker(self, device_address: str):
        """Worker thread for streaming to a specific device."""
        try:
            # Simulate audio streaming to individual device
            while self.is_playing and not self.stop_event.is_set():
                if self.is_paused:
                    time.sleep(0.1)
                    continue
                
                # In real implementation:
                # - Read audio chunk from current file
                # - Apply any device-specific audio processing
                # - Send via Bluetooth A2DP protocol
                # - Handle latency compensation
                
                time.sleep(0.1)  # Simulate processing time
                
        except Exception as e:
            print(f"Error in device stream worker for {device_address}: {e}")
    
    def pause(self):
        """Pause audio playback."""
        try:
            if self.is_playing and not self.is_paused:
                pygame.mixer.music.pause()
                self.is_paused = True
                print("Audio playback paused")
                
        except Exception as e:
            print(f"Error pausing playback: {e}")
    
    def resume(self):
        """Resume audio playback."""
        try:
            if self.is_playing and self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                print("Audio playback resumed")
                
        except Exception as e:
            print(f"Error resuming playback: {e}")
    
    def stop(self):
        """Stop audio playback."""
        try:
            self.is_playing = False
            self.is_paused = False
            self.stop_event.set()
            
            pygame.mixer.music.stop()
            
            if self.playback_thread and self.playback_thread.is_alive():
                self.playback_thread.join(timeout=2)
            
            print("Audio playback stopped")
            
        except Exception as e:
            print(f"Error stopping playback: {e}")
    
    def set_volume(self, volume: float):
        """Set playback volume (0.0 to 1.0)."""
        try:
            self.volume = max(0.0, min(1.0, volume))
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(self.volume)
            print(f"Volume set to {self.volume:.2f}")
            
        except Exception as e:
            print(f"Error setting volume: {e}")
    
    def get_volume(self) -> float:
        """Get current volume level."""
        return self.volume
    
    def get_position(self) -> float:
        """Get current playback position in seconds."""
        try:
            if self.is_playing:
                # pygame doesn't provide position directly
                # This would need to be tracked manually
                return 0.0
            return 0.0
        except:
            return 0.0
    
    def set_position(self, position: float):
        """Set playback position in seconds."""
        try:
            # pygame.mixer doesn't support seeking directly
            # Would need to implement with a different audio library
            # or reload file at specific position
            print(f"Seek to position: {position:.2f}s")
            
        except Exception as e:
            print(f"Error setting position: {e}")
    
    def set_sync_delay(self, delay: float):
        """Set synchronization delay for Bluetooth devices."""
        self.sync_delay = max(0.0, delay)
        print(f"Sync delay set to {self.sync_delay:.3f}s")
    
    def get_audio_format_info(self) -> dict:
        """Get current audio format information."""
        try:
            if pygame.mixer.get_init():
                freq, format_bits, channels = pygame.mixer.get_init()
                return {
                    'sample_rate': freq,
                    'bit_depth': abs(format_bits),
                    'channels': channels,
                    'signed': format_bits < 0
                }
            return {}
        except:
            return {}
    
    def is_file_loaded(self) -> bool:
        """Check if an audio file is currently loaded."""
        return self.current_file is not None
    
    def get_current_file(self) -> Optional[str]:
        """Get the path of the currently loaded file."""
        return self.current_file
    
    def cleanup(self):
        """Clean up audio resources."""
        try:
            self.stop()
            if pygame.mixer.get_init():
                pygame.mixer.quit()
            print("Audio engine cleaned up")
            
        except Exception as e:
            print(f"Error during audio cleanup: {e}")

class AudioEffects:
    """Audio effects and processing utilities."""
    
    @staticmethod
    def apply_echo(audio_data: np.ndarray, delay: float, decay: float) -> np.ndarray:
        """Apply echo effect to audio data."""
        try:
            delay_samples = int(delay * 44100)
            echo = np.zeros_like(audio_data)
            
            if len(audio_data) > delay_samples:
                echo[delay_samples:] = audio_data[:-delay_samples] * decay
                return audio_data + echo
            
            return audio_data
        except:
            return audio_data
    
    @staticmethod
    def apply_volume_fade(audio_data: np.ndarray, fade_in: float, fade_out: float) -> np.ndarray:
        """Apply fade in/out effects."""
        try:
            length = len(audio_data)
            fade_in_samples = int(fade_in * 44100)
            fade_out_samples = int(fade_out * 44100)
            
            # Fade in
            if fade_in_samples > 0:
                fade_in_curve = np.linspace(0, 1, min(fade_in_samples, length))
                audio_data[:len(fade_in_curve)] *= fade_in_curve
            
            # Fade out
            if fade_out_samples > 0:
                fade_out_curve = np.linspace(1, 0, min(fade_out_samples, length))
                start_idx = max(0, length - fade_out_samples)
                audio_data[start_idx:start_idx + len(fade_out_curve)] *= fade_out_curve
            
            return audio_data
        except:
            return audio_data

class AudioSynchronizer:
    """Handles audio synchronization across multiple Bluetooth devices."""
    
    def __init__(self):
        self.device_delays = {}
        self.master_clock = time.time
        
    def calibrate_device_delay(self, device_address: str, ping_time: float):
        """Calibrate delay for a specific device based on ping time."""
        # Estimate Bluetooth audio latency (typically 100-300ms)
        estimated_latency = ping_time + 0.15  # Add 150ms for typical Bluetooth audio delay
        self.device_delays[device_address] = estimated_latency
        print(f"Device {device_address} delay calibrated: {estimated_latency:.3f}s")
    
    def get_sync_delays(self, device_addresses: List[str]) -> dict:
        """Get synchronization delays for all devices."""
        if not self.device_delays:
            # Default delays if not calibrated
            return {addr: 0.15 for addr in device_addresses}
        
        max_delay = max(self.device_delays.get(addr, 0.15) for addr in device_addresses)
        return {addr: max_delay - self.device_delays.get(addr, 0.15) 
                for addr in device_addresses}