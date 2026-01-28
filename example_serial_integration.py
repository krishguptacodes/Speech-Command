"""
Example Integration: Voice Command Module with ESP32 Serial Interface
Demonstrates complete integration for assistive robotic arm control
"""

import sys
import os
from voice_command import VoiceCommandModule
from esp32_serial_interface import ESP32SerialInterface


def main():
    """Main integration example."""
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Voice Command Module - ESP32 Serial Integration")
        print("=" * 60)
        print("\nUsage: python example_serial_integration.py <vosk_model_path> <serial_port>")
        print("\nArguments:")
        print("  vosk_model_path : Path to Vosk speech recognition model")
        print("  serial_port     : Serial port for ESP32 (e.g., /dev/ttyUSB0 or COM3)")
        print("\nExample (Linux/Mac):")
        print("  python example_serial_integration.py ./vosk-model-small-en-us-0.15 /dev/ttyUSB0")
        print("\nExample (Windows):")
        print("  python example_serial_integration.py ./vosk-model-small-en-us-0.15 COM3")
        print("\nDownload Vosk models from: https://alphacephei.com/vosk/models")
        print("Recommended: vosk-model-small-en-us-0.15 (40 MB, fast)")
        sys.exit(1)
    
    model_path = sys.argv[1]
    serial_port = sys.argv[2]
    
    # Validate model path
    if not os.path.exists(model_path):
        print(f"✗ Error: Model path does not exist: {model_path}")
        print("Please download a Vosk model from: https://alphacephei.com/vosk/models")
        sys.exit(1)
    
    # Initialize ESP32 serial interface
    print("Initializing ESP32 Serial Interface...")
    esp32 = ESP32SerialInterface(serial_port, baudrate=115200)
    
    if not esp32.connect():
        print("✗ Failed to connect to ESP32. Please check:")
        print("  - ESP32 is powered on")
        print("  - Correct serial port is specified")
        print("  - No other program is using the serial port")
        sys.exit(1)
    
    # Define command handler that sends commands to ESP32
    def command_handler(command: str):
        """Handle recognized voice commands by sending to ESP32."""
        print(f"[HANDLER] Processing command: {command}")
        esp32.send_command(command)
    
    # Initialize voice command module
    print("\nInitializing Voice Command Module...")
    vcm = VoiceCommandModule(
        model_path=model_path,
        sample_rate=16000,
        command_callback=command_handler
    )
    
    print("\n" + "=" * 60)
    print("SYSTEM READY - Voice-Controlled Robotic Arm")
    print("=" * 60)
    print("Say 'Hey Helper' followed by a command")
    print("Available commands:")
    print("  - grab / release")
    print("  - move up / move down")
    print("  - move left / move right")
    print("  - stop")
    print("\nPress Ctrl+C to exit")
    print("=" * 60 + "\n")
    
    try:
        # Start listening (blocking call)
        vcm.start_listening()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        # Clean up
        vcm.stop_listening()
        esp32.disconnect()
        print("System stopped.")


if __name__ == "__main__":
    main()
