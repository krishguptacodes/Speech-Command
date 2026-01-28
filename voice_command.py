"""
Voice Command Module for Assistive Robotic Arm
Uses Vosk for offline speech recognition with low-latency processing
"""

import json
import queue
import sys
import time
from typing import Callable, Optional
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3


class VoiceCommandModule:
    """
    Main voice command module for assistive robotic arm control.
    Supports wake word detection and command recognition.
    """
    
    # Define valid commands
    COMMANDS = {
        'grab', 'release', 'stop',
        'move up', 'move down', 'move left', 'move right',
        'up', 'down', 'left', 'right'
    }
    
    WAKE_WORD = "hey helper"
    
    def __init__(self, model_path: str, sample_rate: int = 16000, 
                 command_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the voice command module.
        
        Args:
            model_path: Path to the Vosk model directory
            sample_rate: Audio sample rate (default: 16000 Hz)
            command_callback: Callback function to handle recognized commands
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.command_callback = command_callback
        
        # Initialize Vosk model
        print(f"Loading speech recognition model from {model_path}...")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.recognizer.SetWords(True)
        
        # Initialize text-to-speech for audio feedback
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)
        
        # State management
        self.is_awake = False
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        print("Voice Command Module initialized successfully!")
    
    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream processing."""
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        self.audio_queue.put(bytes(indata))
    
    def speak(self, text: str):
        """
        Provide audio feedback using text-to-speech.
        
        Args:
            text: Text to speak
        """
        print(f"Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def process_text(self, text: str):
        """
        Process recognized text for wake word and commands.
        
        Args:
            text: Recognized text from speech recognition
        """
        text_lower = text.lower().strip()
        
        # Check for wake word
        if not self.is_awake:
            if self.WAKE_WORD in text_lower:
                self.is_awake = True
                print(f"✓ Wake word detected: '{self.WAKE_WORD}'")
                self.speak("Yes, I'm listening")
                return
        else:
            # Check for commands
            command_found = None
            
            # Check exact matches first
            if text_lower in self.COMMANDS:
                command_found = text_lower
            else:
                # Check for commands within the text
                # Sort by length (descending) to match longer commands first
                sorted_commands = sorted(self.COMMANDS, key=len, reverse=True)
                for cmd in sorted_commands:
                    if cmd in text_lower:
                        command_found = cmd
                        break
            
            if command_found:
                print(f"✓ Command recognized: '{command_found}'")
                self.speak(f"Executing {command_found}")
                
                # Execute command callback
                if self.command_callback:
                    self.command_callback(command_found)
                
                # Reset awake state after command
                self.is_awake = False
            elif 'stop' in text_lower or 'cancel' in text_lower:
                print("✓ Stop/Cancel command")
                self.speak("Cancelled")
                self.is_awake = False
                if self.command_callback:
                    self.command_callback('stop')
            else:
                print(f"✗ Unrecognized command: '{text_lower}'")
                self.speak("Command not recognized. Please try again.")
                self.is_awake = False
    
    def start_listening(self):
        """
        Start listening for voice commands.
        This is a blocking call that continuously processes audio.
        """
        self.is_listening = True
        
        print("\n" + "="*60)
        print("Voice Command Module - Active")
        print("="*60)
        print(f"Wake word: '{self.WAKE_WORD}'")
        print(f"Available commands: {', '.join(sorted(self.COMMANDS))}")
        print("="*60 + "\n")
        
        try:
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000,
                                  dtype='int16', channels=1,
                                  callback=self.audio_callback):
                print("Listening for wake word...")
                
                while self.is_listening:
                    try:
                        data = self.audio_queue.get(timeout=1)
                    except queue.Empty:
                        continue
                    
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        if result.get('text'):
                            text = result['text']
                            print(f"Heard: '{text}'")
                            self.process_text(text)
                    else:
                        # Partial result for low-latency feedback
                        partial = json.loads(self.recognizer.PartialResult())
                        if partial.get('partial'):
                            # Could be used for real-time feedback if needed
                            pass
                            
        except KeyboardInterrupt:
            print("\nStopping voice command module...")
        except Exception as e:
            print(f"Error in audio processing: {e}")
            raise
        finally:
            self.is_listening = False
            print("Voice Command Module stopped.")
    
    def stop_listening(self):
        """Stop listening for voice commands."""
        self.is_listening = False


if __name__ == "__main__":
    # Example usage
    def example_command_handler(command: str):
        """Example command handler that prints the command."""
        print(f"[HANDLER] Received command: {command}")
        # Here you would integrate with ESP32 communication
    
    # Check if model path is provided
    if len(sys.argv) < 2:
        print("Usage: python voice_command.py <path_to_vosk_model>")
        print("\nExample: python voice_command.py ./vosk-model-small-en-us-0.15")
        print("\nDownload models from: https://alphacephei.com/vosk/models")
        sys.exit(1)
    
    model_path = sys.argv[1]
    
    # Initialize and start the voice command module
    vcm = VoiceCommandModule(
        model_path=model_path,
        command_callback=example_command_handler
    )
    
    vcm.start_listening()
