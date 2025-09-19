# Bluetooth Multi-Device Music Player

A Windows application that allows you to play music simultaneously to multiple connected Bluetooth devices. Perfect for creating a synchronized audio experience with friends using multiple Bluetooth speakers or headphones.

## Features

- **Multi-Device Audio Streaming**: Play music to multiple Bluetooth devices simultaneously
- **Device Discovery**: Automatically discover nearby Bluetooth audio devices
- **Easy Connection Management**: Connect/disconnect devices with simple clicks
- **Music Player Controls**: Play, pause, stop, and volume control
- **Synchronization**: Attempt to synchronize audio across all connected devices
- **User-Friendly GUI**: Clean, intuitive interface built with Tkinter
- **File Format Support**: MP3, WAV, OGG, and M4A audio files

## System Requirements

- **Operating System**: Windows 10/11 (64-bit recommended)
- **Python**: Version 3.7 or higher
- **Bluetooth**: Built-in or USB Bluetooth adapter
- **Memory**: 512 MB RAM minimum
- **Storage**: 100 MB free space

## Installation

### Quick Setup

1. **Download or Clone the Project**
   ```bash
   git clone <repository-url>
   cd bluetooth-music-player
   ```

2. **Run the Setup Script**
   ```bash
   python setup.py
   ```
   This will automatically install all required dependencies.

3. **Launch the Application**
   ```bash
   python main.py
   ```

### Manual Installation

If the automatic setup doesn't work, install dependencies manually:

```bash
pip install pygame==2.5.2
pip install pybluez==0.23
pip install pyaudio==0.2.11
pip install mutagen==1.47.0
pip install pillow==10.0.1
pip install numpy==1.24.3
pip install pycaw==20220416
```

## Usage Guide

### Getting Started

1. **Launch the Application**
   - Run `python main.py` or use the desktop shortcut
   - The main window will open with the music player interface

2. **Discover Bluetooth Devices**
   - Click "Discover Devices" to scan for nearby Bluetooth audio devices
   - Wait for the scan to complete (usually 10-15 seconds)
   - Available devices will appear in the device list

3. **Connect to Devices**
   - Select one or more devices from the discovered list
   - Click "Connect" for each device you want to use
   - Connected devices will appear in the "Connected Devices" section

4. **Load Music**
   - Click "Load Music File" to select an audio file
   - Supported formats: MP3, WAV, OGG, M4A
   - The current song name will be displayed

5. **Play Music**
   - Click "▶ Play" to start playback to all connected devices
   - Use "⏸ Pause" and "⏹ Stop" to control playback
   - Adjust volume using the volume slider

### Advanced Features

#### Synchronization Settings
- Adjust "Sync Delay" to compensate for different device latencies
- Default is 150ms, but you may need to adjust based on your devices
- Higher values add more delay to account for slower devices

#### Auto-Connect
- Enable "Auto-connect to known devices" to automatically connect to previously paired devices

#### Multiple File Playback
- Load different music files during playback
- The new file will start playing to all connected devices

## Troubleshooting

### Common Issues

**1. "No Bluetooth devices found"**
- Ensure Bluetooth is enabled on your computer
- Make sure target devices are in pairing/discoverable mode
- Try refreshing the device list
- Restart the Bluetooth service: `net stop bthserv && net start bthserv`

**2. "Failed to connect to device"**
- Ensure the device is not connected to another source
- Try forgetting and re-pairing the device in Windows Settings
- Check if the device supports A2DP audio profile
- Some devices may need to be connected through Windows Settings first

**3. "Audio not playing to Bluetooth devices"**
- Check Windows Sound settings - ensure Bluetooth devices are enabled
- Try disconnecting and reconnecting the devices
- Verify that the devices support stereo audio (A2DP)
- Check if Windows has set the device as "Hands-free" instead of "Stereo Audio"

**4. "Audio is out of sync between devices"**
- Adjust the "Sync Delay" setting in the application
- Different Bluetooth devices have different latencies
- Start with 150ms and adjust up or down based on your experience

**5. "Application crashes on startup"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that your Python version is 3.7 or higher
- Try running as administrator if permission issues occur

### Audio Quality Issues

**Poor Audio Quality:**
- Check Bluetooth codec settings in Windows
- Ensure devices are within good range (< 10 meters)
- Close other applications using Bluetooth or audio
- Try adjusting the sample rate in settings

**Audio Dropouts:**
- Reduce the number of connected devices
- Move closer to Bluetooth devices
- Close bandwidth-intensive applications
- Check for interference from other wireless devices

### Windows-Specific Solutions

**1. Reset Bluetooth Stack**
```powershell
# Run as Administrator
Get-Service -Name "bthserv" | Restart-Service
```

**2. Check Bluetooth Drivers**
- Open Device Manager
- Expand "Bluetooth" section
- Update drivers for your Bluetooth adapter

**3. Audio Service Issues**
```powershell
# Restart Windows Audio service
net stop audiosrv
net start audiosrv
```

## Technical Information

### How It Works

The application uses several components to achieve multi-device audio streaming:

1. **Bluetooth Discovery**: Uses Windows Bluetooth APIs to discover nearby devices
2. **Audio Engine**: Pygame mixer handles audio file loading and playback
3. **Device Management**: Maintains connections to multiple Bluetooth devices
4. **Synchronization**: Attempts to compensate for varying device latencies

### Limitations

- **Windows Only**: Currently designed for Windows 10/11
- **A2DP Profile**: Devices must support Advanced Audio Distribution Profile
- **Latency**: Bluetooth inherently has latency; perfect synchronization is difficult
- **Device Limits**: Windows typically supports 5-7 simultaneous Bluetooth audio connections
- **Codec Dependency**: Audio quality depends on supported Bluetooth codecs

### File Structure

```
bluetooth-music-player/
├── main.py                 # Main application entry point
├── bluetooth_manager.py    # Bluetooth device management
├── audio_engine.py        # Audio playback and streaming
├── gui_components.py      # User interface components
├── setup.py              # Installation script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with multiple Bluetooth devices
5. Submit a pull request

### Building from Source

```bash
# Clone repository
git clone <repository-url>
cd bluetooth-music-player

# Set up development environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Future Enhancements

- Linux and macOS support
- Advanced audio effects and equalizer
- Playlist management
- Network streaming capabilities
- Mobile device integration
- Audio visualization

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and bug reports:
1. Check this README for common solutions
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

Include the following information when reporting issues:
- Windows version
- Python version
- Bluetooth adapter model
- Connected device models
- Error messages or logs

## Acknowledgments

- Built with Python and Tkinter
- Uses pygame for audio handling
- Windows Bluetooth API integration
- Community feedback and testing

---

**Note**: This application is designed for personal use and may not work perfectly with all Bluetooth device combinations. Bluetooth audio streaming to multiple devices simultaneously is technically challenging and results may vary based on your hardware and device compatibility.