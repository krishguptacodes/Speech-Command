# Command Protocol Documentation

## Overview

The voice command module uses a simple JSON-based protocol to communicate with ESP32. This document describes the protocol format and command mappings.

## Message Format

### Python to ESP32

Commands are sent as JSON objects with the following structure:

```json
{
  "command": "COMMAND_CODE",
  "timestamp": 1234567890
}
```

**Fields:**
- `command` (string): Action code for the ESP32 to execute
- `timestamp` (integer): Unix timestamp in milliseconds when command was issued

### ESP32 to Python (Optional)

ESP32 can send acknowledgments as simple text:
```
ACK
```

Or as JSON for more detailed responses:
```json
{
  "status": "OK",
  "command": "MOVE_UP",
  "timestamp": 1234567890
}
```

## Command Mappings

Voice commands are mapped to action codes as follows:

| Voice Command | Action Code | Description |
|--------------|-------------|-------------|
| grab | GRAB | Close the gripper |
| release | RELEASE | Open the gripper |
| stop | STOP | Stop all movement |
| move up / up | MOVE_UP | Move arm upward |
| move down / down | MOVE_DOWN | Move arm downward |
| move left / left | MOVE_LEFT | Rotate arm left |
| move right / right | MOVE_RIGHT | Rotate arm right |

## Communication Methods

### Serial/UART

**Python Side:**
```python
from esp32_serial_interface import ESP32SerialInterface

esp32 = ESP32SerialInterface(port="/dev/ttyUSB0", baudrate=115200)
esp32.connect()
esp32.send_command("grab")
```

**ESP32 Side:**
- Listens on serial port (115200 baud default)
- Receives JSON-formatted commands via UART
- Parses and executes commands
- Optionally sends "ACK" response

**Message Termination:** Newline character (`\n`)

### WiFi - HTTP

**Python Side:**
```python
from esp32_wifi_interface import ESP32WiFiInterface

esp32 = ESP32WiFiInterface(esp32_ip="192.168.1.100", port=80, protocol="http")
esp32.send_command("move up")
```

**ESP32 Side:**
- Runs HTTP server on port 80
- Endpoint: `POST /command`
- Content-Type: `application/json`
- Response: Plain text "OK" or error message

**Example HTTP Request:**
```http
POST /command HTTP/1.1
Host: 192.168.1.100
Content-Type: application/json

{"command": "MOVE_UP", "timestamp": 1234567890}
```

### WiFi - UDP

**Python Side:**
```python
from esp32_wifi_interface import ESP32WiFiInterface

esp32 = ESP32WiFiInterface(esp32_ip="192.168.1.100", port=8888, protocol="udp")
esp32.send_command("release")
```

**ESP32 Side:**
- Listens on UDP port (8888 default)
- Receives JSON-formatted commands as UDP datagrams
- Optionally sends UDP acknowledgment

**Advantages:**
- Lower latency than HTTP
- No connection overhead
- Suitable for real-time control

## Error Handling

### Python Side

The interface methods return boolean values:
- `True`: Command sent successfully
- `False`: Communication error occurred

Example:
```python
if not esp32.send_command("grab"):
    print("Failed to send command")
```

### ESP32 Side

- Invalid JSON: Log error, ignore message
- Unknown command: Log warning, send error response
- Command execution failure: Log error, continue listening

## Adding Custom Commands

### 1. Update Python Side

In `voice_command.py`:
```python
COMMANDS = {
    'grab', 'release', 'stop',
    'move up', 'move down', 'move left', 'move right',
    'rotate', 'extend'  # Add your commands
}
```

In `esp32_serial_interface.py` and `esp32_wifi_interface.py`:
```python
COMMAND_MAP = {
    'grab': 'GRAB',
    # ... existing mappings ...
    'rotate': 'ROTATE',
    'extend': 'EXTEND'
}
```

### 2. Update ESP32 Side

In Arduino sketch:
```cpp
#define CMD_ROTATE "ROTATE"
#define CMD_EXTEND "EXTEND"

void executeCommand(const char* command) {
    // ... existing code ...
    else if (strcmp(command, CMD_ROTATE) == 0) {
        // Your rotation code
    }
    else if (strcmp(command, CMD_EXTEND) == 0) {
        // Your extension code
    }
}
```

## Security Considerations

1. **Serial**: Physical access required, inherently secure
2. **WiFi HTTP**: 
   - Use WPA2/WPA3 encryption
   - Consider adding API key authentication
   - Implement rate limiting
3. **WiFi UDP**:
   - No built-in security
   - Add encryption layer if needed
   - Validate sender IP address

## Performance Characteristics

| Method | Latency | Reliability | Setup Complexity |
|--------|---------|-------------|------------------|
| Serial | 10-50ms | High | Low |
| HTTP | 50-200ms | High | Medium |
| UDP | 20-100ms | Medium | Medium |

## Troubleshooting

### Serial Issues
- **No response**: Check baud rate matches on both sides
- **Garbled data**: Verify serial port settings (8N1)
- **Permission denied**: Add user to dialout group (Linux)

### WiFi Issues
- **Connection timeout**: Verify IP address and firewall
- **Commands not executing**: Check ESP32 serial monitor for errors
- **Packet loss (UDP)**: Switch to TCP/HTTP or add retry logic

## Example Flow

```
User speaks: "Hey Helper"
    ↓
Voice Command Module detects wake word
    ↓
Audio Feedback: "Yes, I'm listening"
    ↓
User speaks: "grab"
    ↓
Command recognized: "grab"
    ↓
Audio Feedback: "Executing grab"
    ↓
Python sends: {"command": "GRAB", "timestamp": 1640000000}
    ↓
ESP32 receives and parses JSON
    ↓
ESP32 executes: Close gripper
    ↓
ESP32 responds: "ACK"
    ↓
Command complete
```

## API Reference

### Python Classes

#### VoiceCommandModule
```python
VoiceCommandModule(
    model_path: str,
    sample_rate: int = 16000,
    command_callback: Callable[[str], None] = None
)
```

#### ESP32SerialInterface
```python
ESP32SerialInterface(
    port: str,
    baudrate: int = 115200,
    timeout: float = 1.0
)
```

#### ESP32WiFiInterface
```python
ESP32WiFiInterface(
    esp32_ip: str,
    port: int = 80,
    protocol: str = 'http',
    timeout: float = 2.0
)
```

## Version History

- v1.0: Initial release with Vosk support, serial and WiFi interfaces
