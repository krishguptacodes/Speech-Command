# Quick Start Guide

Get your voice-controlled robotic arm up and running in minutes!

## Prerequisites

- Python 3.7+
- Microphone
- ESP32 (optional, for hardware integration)

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Speech Model

```bash
# Download small English model (~40 MB)
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### 3. Test Voice Commands (No Hardware)

```bash
python voice_command.py ./vosk-model-small-en-us-0.15
```

**Try saying:**
1. "Hey Helper"
2. "move up"
3. "Hey Helper"
4. "grab"

## Hardware Integration

### Option A: Serial Connection (Easiest)

1. Connect ESP32 via USB
2. Upload `esp32_examples/serial_receiver.ino`
3. Find your serial port:
   - Linux: `ls /dev/ttyUSB*`
   - Windows: Check Device Manager
4. Run:
   ```bash
   python example_serial_integration.py ./vosk-model-small-en-us-0.15 /dev/ttyUSB0
   ```

### Option B: WiFi Connection

1. Update WiFi credentials in `esp32_examples/wifi_receiver.ino`
2. Upload to ESP32
3. Note the IP address from Serial Monitor
4. Run:
   ```bash
   python example_wifi_integration.py ./vosk-model-small-en-us-0.15 192.168.1.100
   ```

## Command Cheat Sheet

| Say This | Robot Does |
|----------|------------|
| Hey Helper | Activate listening |
| grab | Close gripper |
| release | Open gripper |
| move up | Arm moves up |
| move down | Arm moves down |
| move left | Rotate left |
| move right | Rotate right |
| stop | Stop all motors |

## Troubleshooting

### "PortAudio not found"
- **Linux**: `sudo apt-get install portaudio19-dev`
- **macOS**: `brew install portaudio`
- **Windows**: Usually works out of the box

### Wake word not detected
- Speak clearly: "Hey Helper"
- Check microphone volume
- Reduce background noise

### ESP32 not responding
- Verify correct serial port
- Check baud rate (115200)
- Look at Serial Monitor for errors

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Review [PROTOCOL.md](PROTOCOL.md) for command protocol
- Check [esp32_examples/README.md](esp32_examples/README.md) for ESP32 setup
- Run `python test_voice_command.py` to verify installation

## Support

Having issues? 
1. Check [README.md](README.md) Troubleshooting section
2. Review ESP32 Serial Monitor for debug output
3. Open an issue on GitHub

---

**Happy building! 🤖🎤**
