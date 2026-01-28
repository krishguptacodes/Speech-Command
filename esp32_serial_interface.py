"""
Serial Communication Interface for ESP32
Sends voice commands to ESP32 via serial port
"""

import serial
import json
import time
from typing import Optional


class ESP32SerialInterface:
    """
    Serial communication interface for sending commands to ESP32.
    """
    
    # Command protocol - maps voice commands to ESP32 action codes
    COMMAND_MAP = {
        'grab': 'GRAB',
        'release': 'RELEASE',
        'stop': 'STOP',
        'move up': 'MOVE_UP',
        'move down': 'MOVE_DOWN',
        'move left': 'MOVE_LEFT',
        'move right': 'MOVE_RIGHT',
        'up': 'MOVE_UP',
        'down': 'MOVE_DOWN',
        'left': 'MOVE_LEFT',
        'right': 'MOVE_RIGHT'
    }
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1.0):
        """
        Initialize serial connection to ESP32.
        
        Args:
            port: Serial port (e.g., '/dev/ttyUSB0', 'COM3')
            baudrate: Communication speed (default: 115200)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn: Optional[serial.Serial] = None
        
    def connect(self):
        """Establish serial connection to ESP32."""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout
            )
            time.sleep(2)  # Wait for ESP32 to reset
            print(f"✓ Connected to ESP32 on {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect to ESP32: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("✓ Disconnected from ESP32")
    
    def send_command(self, voice_command: str) -> bool:
        """
        Send a voice command to ESP32.
        
        Args:
            voice_command: Voice command string
            
        Returns:
            True if command was sent successfully, False otherwise
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            print("✗ Serial connection not open")
            return False
        
        # Map voice command to ESP32 action code
        action_code = self.COMMAND_MAP.get(voice_command.lower())
        
        if not action_code:
            print(f"✗ Unknown command: {voice_command}")
            return False
        
        try:
            # Create command message as JSON
            message = {
                'command': action_code,
                'timestamp': int(time.time() * 1000)
            }
            
            # Send as JSON string with newline terminator
            json_str = json.dumps(message) + '\n'
            self.serial_conn.write(json_str.encode('utf-8'))
            self.serial_conn.flush()
            
            print(f"✓ Sent command: {action_code}")
            
            # Read acknowledgment if available
            if self.serial_conn.in_waiting > 0:
                response = self.serial_conn.readline().decode('utf-8').strip()
                print(f"  ESP32 response: {response}")
            
            return True
            
        except serial.SerialException as e:
            print(f"✗ Failed to send command: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if serial connection is active."""
        return self.serial_conn is not None and self.serial_conn.is_open


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python esp32_serial_interface.py <serial_port>")
        print("\nExample (Linux/Mac): python esp32_serial_interface.py /dev/ttyUSB0")
        print("Example (Windows): python esp32_serial_interface.py COM3")
        sys.exit(1)
    
    port = sys.argv[1]
    
    # Test the serial interface
    interface = ESP32SerialInterface(port)
    
    if interface.connect():
        print("\nTesting commands...")
        test_commands = ['grab', 'move up', 'move left', 'release', 'stop']
        
        for cmd in test_commands:
            print(f"\nSending: {cmd}")
            interface.send_command(cmd)
            time.sleep(1)
        
        interface.disconnect()
    else:
        print("Failed to connect to ESP32")
        sys.exit(1)
