# ESP32 Examples for Voice Command Module

This directory contains Arduino/PlatformIO sketches for ESP32 to receive voice commands from the Python voice command module.

## Files

- **serial_receiver.ino** - Receives commands via serial/UART connection
- **wifi_receiver.ino** - Receives commands via WiFi (HTTP or UDP)

## Hardware Requirements

- ESP32 development board
- Servo motors or stepper motors for robotic arm
- Appropriate power supply for motors
- (Optional) Motor driver board if using high-power motors

## Setup Instructions

### Using Arduino IDE

1. Install Arduino IDE from https://www.arduino.cc/en/software
2. Install ESP32 board support:
   - Open Arduino IDE
   - Go to File → Preferences
   - Add this URL to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Board Manager
   - Search for "esp32" and install "esp32 by Espressif Systems"

3. Install required libraries:
   - Go to Tools → Manage Libraries
   - Install "ArduinoJson" by Benoit Blanchon

4. Select your ESP32 board:
   - Go to Tools → Board → ESP32 Arduino
   - Select your specific ESP32 board (e.g., "ESP32 Dev Module")

5. Upload the sketch:
   - Open the desired .ino file
   - Update WiFi credentials (for wifi_receiver.ino)
   - Click Upload

### Using PlatformIO

1. Install PlatformIO from https://platformio.org/
2. Create a new project with ESP32 board
3. Add to `platformio.ini`:
   ```ini
   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   lib_deps = 
       bblanchon/ArduinoJson@^6.21.0
   ```
4. Copy the .ino file content to `src/main.cpp`
5. Build and upload

## Configuration

### Serial Receiver
- Default baud rate: 115200
- No configuration needed, just upload and connect

### WiFi Receiver
Before uploading, update these lines in `wifi_receiver.ino`:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
```

## Pin Configuration

Default pins (modify as needed):
```cpp
#define LED_PIN 2
#define SERVO_BASE_PIN 13
#define SERVO_SHOULDER_PIN 12
#define SERVO_ELBOW_PIN 14
#define SERVO_GRIPPER_PIN 27
```

## Command Protocol

Commands are sent as JSON:
```json
{
  "command": "MOVE_UP",
  "timestamp": 1234567890
}
```

Supported commands:
- GRAB
- RELEASE
- STOP
- MOVE_UP
- MOVE_DOWN
- MOVE_LEFT
- MOVE_RIGHT

## Testing

After uploading:

1. **Serial**: Open Serial Monitor (115200 baud) to see debug output
2. **WiFi**: 
   - Check Serial Monitor for ESP32's IP address
   - Visit the IP in a web browser to see status page
   - Use Python scripts to send commands

## Troubleshooting

- **ESP32 not connecting**: Check USB cable and drivers
- **WiFi not working**: Verify SSID/password, check signal strength
- **Commands not executing**: Check Serial Monitor for error messages
- **Motor issues**: Verify power supply and pin connections
