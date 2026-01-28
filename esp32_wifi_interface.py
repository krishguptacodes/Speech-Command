"""
WiFi/Network Communication Interface for ESP32
Sends voice commands to ESP32 via HTTP or UDP
"""

import json
import time
import socket
import requests
from typing import Optional


class ESP32WiFiInterface:
    """
    WiFi communication interface for sending commands to ESP32.
    Supports both HTTP REST API and UDP protocols.
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
    
    def __init__(self, esp32_ip: str, port: int = 80, protocol: str = 'http', timeout: float = 2.0):
        """
        Initialize WiFi connection to ESP32.
        
        Args:
            esp32_ip: IP address of ESP32
            port: Port number (default: 80 for HTTP, 8888 for UDP)
            protocol: Communication protocol ('http' or 'udp')
            timeout: Connection timeout in seconds
        """
        self.esp32_ip = esp32_ip
        self.port = port
        self.protocol = protocol.lower()
        self.timeout = timeout
        self.udp_socket: Optional[socket.socket] = None
        
        if self.protocol == 'udp':
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.settimeout(timeout)
        
        print(f"✓ ESP32 WiFi Interface initialized ({protocol.upper()} mode)")
        print(f"  Target: {esp32_ip}:{port}")
    
    def send_command_http(self, action_code: str) -> bool:
        """
        Send command via HTTP POST request.
        
        Args:
            action_code: ESP32 action code
            
        Returns:
            True if successful, False otherwise
        """
        url = f"http://{self.esp32_ip}:{self.port}/command"
        
        payload = {
            'command': action_code,
            'timestamp': int(time.time() * 1000)
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                print(f"✓ Command sent via HTTP: {action_code}")
                print(f"  Response: {response.text}")
                return True
            else:
                print(f"✗ HTTP error {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to send HTTP command: {e}")
            return False
    
    def send_command_udp(self, action_code: str) -> bool:
        """
        Send command via UDP datagram.
        
        Args:
            action_code: ESP32 action code
            
        Returns:
            True if successful, False otherwise
        """
        if not self.udp_socket:
            print("✗ UDP socket not initialized")
            return False
        
        message = {
            'command': action_code,
            'timestamp': int(time.time() * 1000)
        }
        
        try:
            json_str = json.dumps(message)
            self.udp_socket.sendto(
                json_str.encode('utf-8'),
                (self.esp32_ip, self.port)
            )
            
            print(f"✓ Command sent via UDP: {action_code}")
            
            # Try to receive acknowledgment (optional)
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                response = data.decode('utf-8')
                print(f"  Response from {addr}: {response}")
            except socket.timeout:
                # No response expected for UDP in some implementations
                pass
            
            return True
            
        except socket.error as e:
            print(f"✗ Failed to send UDP command: {e}")
            return False
    
    def send_command(self, voice_command: str) -> bool:
        """
        Send a voice command to ESP32.
        
        Args:
            voice_command: Voice command string
            
        Returns:
            True if command was sent successfully, False otherwise
        """
        # Map voice command to ESP32 action code
        action_code = self.COMMAND_MAP.get(voice_command.lower())
        
        if not action_code:
            print(f"✗ Unknown command: {voice_command}")
            return False
        
        # Send via appropriate protocol
        if self.protocol == 'http':
            return self.send_command_http(action_code)
        elif self.protocol == 'udp':
            return self.send_command_udp(action_code)
        else:
            print(f"✗ Unsupported protocol: {self.protocol}")
            return False
    
    def close(self):
        """Close network connections."""
        if self.udp_socket:
            self.udp_socket.close()
            print("✓ UDP socket closed")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python esp32_wifi_interface.py <esp32_ip> [protocol] [port]")
        print("\nExamples:")
        print("  python esp32_wifi_interface.py 192.168.1.100")
        print("  python esp32_wifi_interface.py 192.168.1.100 udp 8888")
        print("  python esp32_wifi_interface.py 192.168.1.100 http 80")
        sys.exit(1)
    
    esp32_ip = sys.argv[1]
    protocol = sys.argv[2] if len(sys.argv) > 2 else 'http'
    port = int(sys.argv[3]) if len(sys.argv) > 3 else (80 if protocol == 'http' else 8888)
    
    # Test the WiFi interface
    interface = ESP32WiFiInterface(esp32_ip, port=port, protocol=protocol)
    
    print("\nTesting commands...")
    test_commands = ['grab', 'move up', 'move left', 'release', 'stop']
    
    for cmd in test_commands:
        print(f"\nSending: {cmd}")
        interface.send_command(cmd)
        time.sleep(1)
    
    interface.close()
