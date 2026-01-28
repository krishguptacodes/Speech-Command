/*
 * ESP32 Example Code - WiFi Interface for Voice Command Module
 * 
 * This example demonstrates receiving voice commands via WiFi (HTTP or UDP)
 * and controlling a robotic arm accordingly.
 * 
 * SECURITY WARNING: This example code does not implement authentication.
 * For production use, add API key authentication, IP whitelisting, or
 * other security measures to prevent unauthorized access to your robot.
 * 
 * Hardware Requirements:
 * - ESP32 development board with WiFi
 * - Servo motors or stepper motors for robotic arm
 * - Power supply appropriate for your motors
 * 
 * IMPORTANT: Update WiFi credentials below before uploading!
 * NEVER commit real WiFi credentials to version control!
 */

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

// WiFi credentials - UPDATE THESE!
// For production: Use a separate config file or secure storage
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server configuration
WebServer server(80);        // HTTP server on port 80
WiFiUDP udp;                // UDP server
const int udpPort = 8888;   // UDP port

// Command definitions
#define CMD_GRAB "GRAB"
#define CMD_RELEASE "RELEASE"
#define CMD_STOP "STOP"
#define CMD_MOVE_UP "MOVE_UP"
#define CMD_MOVE_DOWN "MOVE_DOWN"
#define CMD_MOVE_LEFT "MOVE_LEFT"
#define CMD_MOVE_RIGHT "MOVE_RIGHT"

// Pin definitions
#define LED_PIN 2

void executeCommand(const char* command) {
  Serial.print("Executing: ");
  Serial.println(command);
  
  digitalWrite(LED_PIN, HIGH);
  
  if (strcmp(command, CMD_GRAB) == 0) {
    Serial.println("Action: Closing gripper");
    // Add your gripper close code
    
  } else if (strcmp(command, CMD_RELEASE) == 0) {
    Serial.println("Action: Opening gripper");
    // Add your gripper open code
    
  } else if (strcmp(command, CMD_STOP) == 0) {
    Serial.println("Action: STOP");
    // Add your motor stop code
    
  } else if (strcmp(command, CMD_MOVE_UP) == 0) {
    Serial.println("Action: Moving UP");
    // Add your upward movement code
    
  } else if (strcmp(command, CMD_MOVE_DOWN) == 0) {
    Serial.println("Action: Moving DOWN");
    // Add your downward movement code
    
  } else if (strcmp(command, CMD_MOVE_LEFT) == 0) {
    Serial.println("Action: Moving LEFT");
    // Add your left rotation code
    
  } else if (strcmp(command, CMD_MOVE_RIGHT) == 0) {
    Serial.println("Action: Moving RIGHT");
    // Add your right rotation code
  }
  
  delay(100);
  digitalWrite(LED_PIN, LOW);
}

// HTTP POST handler for /command endpoint
void handleCommand() {
  if (server.hasArg("plain")) {
    String body = server.arg("plain");
    
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, body);
    
    if (error) {
      server.send(400, "text/plain", "Invalid JSON");
      return;
    }
    
    const char* command = doc["command"];
    if (command != nullptr) {
      executeCommand(command);
      server.send(200, "text/plain", "OK");
    } else {
      server.send(400, "text/plain", "Missing command");
    }
  } else {
    server.send(400, "text/plain", "No body");
  }
}

// Root page handler
void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Voice Command Receiver</h1>";
  html += "<p>Status: Ready</p>";
  html += "<p>IP: " + WiFi.localIP().toString() + "</p>";
  html += "<p>Listening for commands...</p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void processUDP() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Prevent buffer overflow - max buffer size is 255
    if (packetSize > 254) {
      Serial.printf("UDP packet too large (%d bytes), ignoring\n", packetSize);
      udp.flush();  // Discard oversized packet
      return;
    }
    
    char incomingPacket[255];
    int len = udp.read(incomingPacket, 254);  // Read max 254 bytes
    if (len > 0) {
      incomingPacket[len] = 0;  // Null terminate
    }
    
    Serial.printf("UDP packet received: %s\n", incomingPacket);
    
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, incomingPacket);
    
    if (!error) {
      const char* command = doc["command"];
      if (command != nullptr) {
        executeCommand(command);
        
        // Send acknowledgment
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.print("OK");
        udp.endPacket();
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  
  // Connect to WiFi
  Serial.println("\nConnecting to WiFi...");
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  // Start HTTP server
  server.on("/", handleRoot);
  server.on("/command", HTTP_POST, handleCommand);
  server.begin();
  Serial.println("HTTP server started on port 80");
  
  // Start UDP server
  udp.begin(udpPort);
  Serial.printf("UDP server started on port %d\n", udpPort);
  
  Serial.println("\nESP32 Voice Command Receiver - Ready");
}

void loop() {
  server.handleClient();  // Handle HTTP requests
  processUDP();           // Handle UDP packets
  delay(10);
}
