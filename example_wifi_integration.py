"""
Example Integration: Voice Command Module with ESP32 WiFi Interface
Demonstrates complete integration for assistive robotic arm control via WiFi
"""

import sys
import os
from voice_command import VoiceCommandModule
from esp32_wifi_interface import ESP32WiFiInterface


def main():
    """Main integration example."""
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Voice Command Module - ESP32 WiFi Integration")
        print("=" * 60)
        print("\nUsage: python example_wifi_integration.py <vosk_model_path> <esp32_ip> [protocol] [port]")
        print("\nArguments:")
        print("  vosk_model_path : Path to Vosk speech recognition model")
        print("  esp32_ip        : IP address of ESP32 (e.g., 192.168.1.100)")
        print("  protocol        : Communication protocol - 'http' or 'udp' (default: http)")
        print("  port            : Port number (default: 80 for HTTP, 8888 for UDP)")
        print("\nExamples:")
        print("  python example_wifi_integration.py ./vosk-model-small-en-us-0.15 192.168.1.100")
        print("  python example_wifi_integration.py ./vosk-model-small-en-us-0.15 192.168.1.100 udp 8888")
        print("\nDownload Vosk models from: https://alphacephei.com/vosk/models")
        print("Recommended: vosk-model-small-en-us-0.15 (40 MB, fast)")
        sys.exit(1)
    
    model_path = sys.argv[1]
    esp32_ip = sys.argv[2]
    protocol = sys.argv[3] if len(sys.argv) > 3 else 'http'
    port = int(sys.argv[4]) if len(sys.argv) > 4 else (80 if protocol == 'http' else 8888)
    
    # Validate model path
    if not os.path.exists(model_path):
        print(f"✗ Error: Model path does not exist: {model_path}")
        print("Please download a Vosk model from: https://alphacephei.com/vosk/models")
        sys.exit(1)
    
    # Initialize ESP32 WiFi interface
    print(f"Initializing ESP32 WiFi Interface ({protocol.upper()})...")
    esp32 = ESP32WiFiInterface(esp32_ip, port=port, protocol=protocol)
    
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
    print("SYSTEM READY - Voice-Controlled Robotic Arm (WiFi)")
    print("=" * 60)
    print(f"ESP32 Address: {esp32_ip}:{port} ({protocol.upper()})")
    print("\nSay 'Hey Helper' followed by a command")
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
        esp32.close()
        print("System stopped.")


if __name__ == "__main__":
    main()
