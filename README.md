# Voice Command Module for Assistive Robotic Arm

A Python-based voice command system for controlling robotic arms with low-latency offline speech recognition. Features wake word detection, command recognition, audio feedback, and multiple communication interfaces for ESP32 integration.

## Features

✅ **Wake Word Detection** - "Hey Helper" activation phrase
✅ **Command Recognition** - Supports grab, release, stop, and directional movement commands
✅ **Audio Feedback** - Text-to-speech confirmation for all actions
✅ **Low-Latency Processing** - Optimized for real-time control
✅ **Offline Speech Recognition** - Uses Vosk for privacy and reliability
✅ **Multiple Communication Interfaces** - Serial (UART) and WiFi (HTTP/UDP) support
✅ **ESP32 Integration** - Complete example code for robotic arm control

## System Requirements

- Python 3.7 or higher
- Microphone (built-in or USB)
- Operating System: Linux, macOS, or Windows
- ESP32 development board (for robot control)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/krishguptacodes/Speech-Command.git
cd Speech-Command
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio espeak
```

#### macOS
```bash
brew install portaudio espeak
```

#### Windows
- PortAudio is included with sounddevice
- Install eSpeak from: http://espeak.sourceforge.net/download.html

### 4. Download Vosk Speech Recognition Model

Download a Vosk model from https://alphacephei.com/vosk/models

**Recommended models:**
- **vosk-model-small-en-us-0.15** (40 MB) - Fast, good for real-time control
- **vosk-model-en-us-0.22** (1.8 GB) - More accurate, slower

Example download:
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

## Quick Start

### Basic Voice Command Testing

Test the voice command module without hardware:

```bash
python voice_command.py ./vosk-model-small-en-us-0.15
```

Say: "Hey Helper" followed by a command like "move up" or "grab"

### With Serial Connection to ESP32

```bash
python example_serial_integration.py ./vosk-model-small-en-us-0.15 /dev/ttyUSB0
```

Windows users: Replace `/dev/ttyUSB0` with `COM3` (or appropriate COM port)

### With WiFi Connection to ESP32

```bash
python example_wifi_integration.py ./vosk-model-small-en-us-0.15 192.168.1.100
```

Replace `192.168.1.100` with your ESP32's IP address.

For UDP instead of HTTP:
```bash
python example_wifi_integration.py ./vosk-model-small-en-us-0.15 192.168.1.100 udp 8888
```

## Available Commands

Once the wake word "Hey Helper" is detected, you can say:

- **grab** - Close the gripper
- **release** - Open the gripper
- **stop** - Stop all movement
- **move up** / **up** - Move arm upward
- **move down** / **down** - Move arm downward
- **move left** / **left** - Rotate arm left
- **move right** / **right** - Rotate arm right

## ESP32 Setup

### Hardware Connection Options

#### Option 1: Serial/UART Connection
1. Connect ESP32 to computer via USB
2. Note the serial port (e.g., `/dev/ttyUSB0` on Linux, `COM3` on Windows)
3. Upload `esp32_examples/serial_receiver.ino` to ESP32
4. Run the Python serial integration script

#### Option 2: WiFi Connection
1. Update WiFi credentials in `esp32_examples/wifi_receiver.ino`
2. Upload sketch to ESP32
3. Note the IP address shown in Serial Monitor
4. Run the Python WiFi integration script

See [esp32_examples/README.md](esp32_examples/README.md) for detailed ESP32 setup instructions.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Voice Command Module                  │
│                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │  Microphone  │───▶│  Vosk Model  │───▶│  Command  │ │
│  │   (Audio)    │    │   (Speech    │    │  Parser   │ │
│  └──────────────┘    │  Recognition)│    └───────────┘ │
│                      └──────────────┘          │        │
│                                                 ▼        │
│                      ┌──────────────┐    ┌───────────┐ │
│                      │  Text-to-    │◀───│  Command  │ │
│                      │   Speech     │    │  Handler  │ │
│                      └──────────────┘    └───────────┘ │
│                                                 │        │
└─────────────────────────────────────────────────┼────────┘
                                                  ▼
                         ┌────────────────────────────────┐
                         │   Communication Interface      │
                         │  ┌──────────┐  ┌────────────┐ │
                         │  │  Serial  │  │    WiFi    │ │
                         │  │  (UART)  │  │ (HTTP/UDP) │ │
                         │  └──────────┘  └────────────┘ │
                         └────────────────────────────────┘
                                        ▼
                              ┌──────────────────┐
                              │      ESP32       │
                              │  Robotic Arm     │
                              │    Controller    │
                              └──────────────────┘
```

## Project Structure

```
Speech-Command/
├── voice_command.py                    # Core voice command module
├── esp32_serial_interface.py          # Serial communication interface
├── esp32_wifi_interface.py            # WiFi communication interface
├── example_serial_integration.py      # Complete serial example
├── example_wifi_integration.py        # Complete WiFi example
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── esp32_examples/                    # ESP32 Arduino code
    ├── serial_receiver.ino            # ESP32 serial receiver
    ├── wifi_receiver.ino              # ESP32 WiFi receiver
    └── README.md                      # ESP32 setup guide
```

## Usage Examples

### Example 1: Custom Command Handler

```python
from voice_command import VoiceCommandModule

def my_command_handler(command: str):
    print(f"Received command: {command}")
    # Add your custom logic here
    if command == "grab":
        # Control your robot
        pass

vcm = VoiceCommandModule(
    model_path="./vosk-model-small-en-us-0.15",
    command_callback=my_command_handler
)

vcm.start_listening()
```

### Example 2: Serial Communication

```python
from esp32_serial_interface import ESP32SerialInterface

esp32 = ESP32SerialInterface(port="/dev/ttyUSB0", baudrate=115200)
if esp32.connect():
    esp32.send_command("move up")
    esp32.send_command("grab")
    esp32.disconnect()
```

### Example 3: WiFi Communication

```python
from esp32_wifi_interface import ESP32WiFiInterface

esp32 = ESP32WiFiInterface(
    esp32_ip="192.168.1.100",
    port=80,
    protocol="http"
)

esp32.send_command("move left")
esp32.send_command("release")
esp32.close()
```

## Performance Considerations

### Low-Latency Tips

1. **Use Small Model** - vosk-model-small-en-us-0.15 provides the best latency
2. **Sample Rate** - 16000 Hz is optimal for Vosk and reduces processing overhead
3. **Hardware** - Use a decent microphone and avoid noisy environments
4. **Communication** - UDP is faster than HTTP for WiFi connections

### Typical Latency Breakdown

- Speech Recognition: 200-500ms
- Command Processing: 10-50ms
- Audio Feedback: 500-1000ms
- Communication (Serial): 10-50ms
- Communication (WiFi): 50-200ms

**Total typical latency: 770ms - 1800ms** from speech to robot action

### Known Limitations

1. **Text-to-Speech Blocking**: Audio feedback currently blocks command processing (500-1000ms). This is acceptable for most use cases but could be improved with threaded TTS for higher responsiveness.

2. **Single Command Processing**: Only one command can be processed at a time. Multiple rapid commands require waiting for previous command completion.

3. **Wake Word Accuracy**: Wake word detection depends on clear pronunciation and low background noise. Consider using a physical button as an alternative activation method in noisy environments.

## Troubleshooting

### Microphone Not Working

```bash
# List audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"
```

If your microphone isn't the default, modify the code to specify device:
```python
with sd.RawInputStream(samplerate=16000, device=YOUR_DEVICE_ID, ...):
```

### Wake Word Not Detected

- Speak clearly and at a moderate pace
- Ensure "Hey Helper" is pronounced distinctly
- Reduce background noise
- Check microphone volume/gain settings

### Commands Not Recognized

- Say the full command (e.g., "move up" not just "up" initially)
- Wait for audio feedback before next command
- The model may need clearer pronunciation

### ESP32 Connection Issues

**Serial:**
- Check USB cable connection
- Verify correct port (use Arduino IDE to find port)
- Ensure no other program is using the port
- Try different baud rate if issues persist

**WiFi:**
- Verify ESP32 and computer are on same network
- Check firewall settings
- Ping the ESP32 IP address to verify connectivity
- Check ESP32 Serial Monitor for error messages

### Text-to-Speech Not Working

**Linux:**
```bash
sudo apt-get install espeak
```

**macOS:**
```bash
brew install espeak
```

**Windows:**
- Install eSpeak: http://espeak.sourceforge.net/download.html

## Advanced Configuration

### Adjusting Speech Recognition Sensitivity

In `voice_command.py`, modify the recognizer settings:

```python
self.recognizer = KaldiRecognizer(self.model, sample_rate)
self.recognizer.SetWords(True)
self.recognizer.SetMaxAlternatives(0)  # Increase for more alternatives
```

### Adding Custom Commands

Edit the `COMMANDS` set in `voice_command.py`:

```python
COMMANDS = {
    'grab', 'release', 'stop',
    'move up', 'move down', 'move left', 'move right',
    'rotate', 'extend', 'retract',  # Add your commands
}
```

Update the command map in ESP32 interfaces accordingly.

### Changing Wake Word

To use a different wake word, edit `voice_command.py`:

```python
WAKE_WORD = "robot activate"  # Change this
```

Note: Vosk uses phonetic matching, so similar-sounding phrases work best.

## Security Considerations

- **Offline Processing** - All speech recognition happens locally, no data sent to cloud
- **Network Security** - Use WiFi with WPA2/WPA3 encryption
- **Physical Access** - Implement emergency stop mechanisms on the robot
- **Command Validation** - Add authentication if needed for critical operations
- **WiFi Authentication** - The example ESP32 code does not implement authentication. For production use:
  - Add API key verification
  - Implement IP address whitelisting
  - Use HTTPS instead of HTTP
  - Consider VPN or secure tunneling for remote access
- **Buffer Overflow Protection** - ESP32 examples include input validation to prevent buffer overflows

**Note**: The provided ESP32 examples are for demonstration purposes. Production deployments should implement proper security measures appropriate to your use case.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source. Please check the repository for license details.

## Credits

- **Vosk** - Offline speech recognition engine
- **Pyttsx3** - Text-to-speech library
- **SoundDevice** - Audio capture library

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review ESP32 examples README for hardware-specific help

## Future Enhancements

- [ ] Multiple wake word support
- [ ] Custom command training
- [ ] Multi-language support
- [ ] Gesture-based control integration
- [ ] Mobile app control interface
- [ ] Voice command macros/sequences
- [ ] Non-blocking text-to-speech for improved responsiveness
- [ ] Authentication system for WiFi connections
- [ ] Custom wake word training