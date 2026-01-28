/*
 * ESP32 Example Code - Serial Interface for Voice Command Module
 * 
 * This example demonstrates receiving voice commands via serial (UART)
 * and controlling a robotic arm accordingly.
 * 
 * Hardware Requirements:
 * - ESP32 development board
 * - Servo motors or stepper motors for robotic arm
 * - Power supply appropriate for your motors
 * 
 * Connections:
 * - Serial: USB or pins 16 (RX), 17 (TX) for Serial2
 * - Servos: Connect to PWM-capable GPIO pins
 */

#include <Arduino.h>
#include <ArduinoJson.h>

// Serial configuration
#define SERIAL_BAUD 115200

// Command definitions (matching Python interface)
#define CMD_GRAB "GRAB"
#define CMD_RELEASE "RELEASE"
#define CMD_STOP "STOP"
#define CMD_MOVE_UP "MOVE_UP"
#define CMD_MOVE_DOWN "MOVE_DOWN"
#define CMD_MOVE_LEFT "MOVE_LEFT"
#define CMD_MOVE_RIGHT "MOVE_RIGHT"

// Pin definitions (adjust for your hardware)
#define LED_PIN 2
#define SERVO_BASE_PIN 13
#define SERVO_SHOULDER_PIN 12
#define SERVO_ELBOW_PIN 14
#define SERVO_GRIPPER_PIN 27

// Global state
bool isMoving = false;
unsigned long lastCommandTime = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD);
  while (!Serial) {
    delay(10);
  }
  
  // Initialize LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Initialize servo pins (or stepper motor pins)
  // Add your motor initialization here
  // Example:
  // pinMode(SERVO_BASE_PIN, OUTPUT);
  // ledcSetup(0, 50, 16);  // 50 Hz PWM for servos
  // ledcAttachPin(SERVO_BASE_PIN, 0);
  
  Serial.println("ESP32 Voice Command Receiver - Ready");
  Serial.println("Waiting for commands...");
}

void executeCommand(const char* command) {
  Serial.print("Executing: ");
  Serial.println(command);
  
  // Blink LED to indicate command received
  digitalWrite(LED_PIN, HIGH);
  
  // Execute the appropriate action
  if (strcmp(command, CMD_GRAB) == 0) {
    // Close gripper
    Serial.println("Action: Closing gripper");
    // Add your gripper close code here
    // Example: moveServo(SERVO_GRIPPER_PIN, 90);
    
  } else if (strcmp(command, CMD_RELEASE) == 0) {
    // Open gripper
    Serial.println("Action: Opening gripper");
    // Add your gripper open code here
    // Example: moveServo(SERVO_GRIPPER_PIN, 0);
    
  } else if (strcmp(command, CMD_STOP) == 0) {
    // Stop all movement
    Serial.println("Action: STOP - Halting all motors");
    isMoving = false;
    // Add your motor stop code here
    
  } else if (strcmp(command, CMD_MOVE_UP) == 0) {
    // Move arm up
    Serial.println("Action: Moving UP");
    // Add your upward movement code here
    // Example: moveServo(SERVO_SHOULDER_PIN, currentAngle + 10);
    
  } else if (strcmp(command, CMD_MOVE_DOWN) == 0) {
    // Move arm down
    Serial.println("Action: Moving DOWN");
    // Add your downward movement code here
    
  } else if (strcmp(command, CMD_MOVE_LEFT) == 0) {
    // Rotate arm left
    Serial.println("Action: Moving LEFT");
    // Add your left rotation code here
    // Example: moveServo(SERVO_BASE_PIN, currentAngle - 10);
    
  } else if (strcmp(command, CMD_MOVE_RIGHT) == 0) {
    // Rotate arm right
    Serial.println("Action: Moving RIGHT");
    // Add your right rotation code here
    
  } else {
    Serial.print("Unknown command: ");
    Serial.println(command);
  }
  
  // Turn off LED
  delay(100);
  digitalWrite(LED_PIN, LOW);
  
  // Send acknowledgment back to PC
  Serial.println("ACK");
}

void processSerialCommand() {
  if (Serial.available() > 0) {
    String jsonString = Serial.readStringUntil('\n');
    jsonString.trim();
    
    if (jsonString.length() == 0) {
      return;
    }
    
    // Parse JSON command
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, jsonString);
    
    if (error) {
      Serial.print("JSON parse error: ");
      Serial.println(error.c_str());
      return;
    }
    
    // Extract command
    const char* command = doc["command"];
    unsigned long timestamp = doc["timestamp"];
    
    if (command != nullptr) {
      lastCommandTime = timestamp;
      executeCommand(command);
    }
  }
}

void loop() {
  // Process incoming serial commands
  processSerialCommand();
  
  // Add any continuous control logic here
  // For example, checking limit switches, safety monitors, etc.
  
  delay(10);  // Small delay for stability
}
