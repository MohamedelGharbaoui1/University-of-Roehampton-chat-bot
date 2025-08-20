# audio_manager.py - Audio response generation and text-to-speech

import base64
import re
import time
import logging
from pathlib import Path
from typing import Optional
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class AudioManager:
    """Manages audio response generation and text-to-speech functionality"""
    
    def __init__(self):
        self.client = None
        if Config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self._ensure_audio_folder()
    
    def _ensure_audio_folder(self):
        """Create audio folder if it doesn't exist"""
        audio_path = Path(Config.AUDIO_FOLDER)
        audio_path.mkdir(exist_ok=True)
        temp_audio_path = Path(Config.TEMP_AUDIO_FOLDER)
        temp_audio_path.mkdir(exist_ok=True)
    
    def is_available(self) -> bool:
        """Check if audio generation is available"""
        return self.client is not None
    
    def generate_audio_response(self, text: str, voice: str = None) -> Optional[bytes]:
        """
        Generate audio response using OpenAI TTS
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (defaults to Config.TTS_VOICE)
        
        Returns:
            Audio bytes or None if failed
        """
        if not self.client:
            logger.error("OpenAI client not initialized")
            return None
        
        if not text or not text.strip():
            logger.error("No text provided for audio generation")
            return None
        
        # Clean text for TTS (remove markdown and excessive formatting)
        clean_text = self.clean_text_for_tts(text)
        
        # Use provided voice or default
        selected_voice = voice or Config.TTS_VOICE
        
        try:
            # Generate audio using OpenAI TTS
            response = self.client.audio.speech.create(
                model=Config.TTS_MODEL,
                voice=selected_voice,
                input=clean_text,
                response_format="mp3"
            )
            
            # Return audio bytes
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return None
    
    def clean_text_for_tts(self, text: str) -> str:
        """
        Clean text for text-to-speech by removing markdown and formatting
        
        Args:
            text: Raw text with potential markdown
            
        Returns:
            Cleaned text suitable for TTS
        """
        if not text:
            return ""
        
        # Remove markdown formatting
        # Remove bold/italic markers
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # *italic*
        text = re.sub(r'_(.*?)_', r'\1', text)        # _italic_
        
        # Remove headers
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove special characters and emojis for better TTS
        text = re.sub(r'[🔑📄📚⚠️❌✅🤖🙋📊💾⏱️🔧🗑️🔄🔍🚨📁🎓📋🆔🔐]', '', text)
        
        # Clean up multiple spaces and line breaks
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Ensure proper sentence ending
        text = text.strip()
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def create_audio_player(self, audio_bytes: bytes, key: str = None) -> str:
        """
        Create an HTML audio player with the audio data
        
        Args:
            audio_bytes: Audio data in bytes
            key: Unique key for the audio player
            
        Returns:
            HTML string for the audio player
        """
        if not audio_bytes:
            return ""
        
        # Encode audio as base64
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Create unique key if not provided
        if not key:
            key = f"audio_{int(time.time() * 1000)}"
        
        # HTML audio player with custom styling
        audio_html = f"""
        <div class="audio-player-container" style="margin: 10px 0;">
            <div class="audio-controls" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 25px;
                padding: 10px 20px;
                display: flex;
                align-items: center;
                gap: 15px;
                box-shadow: 0 4px 15px rgba(102,126,234,0.3);
            ">
                <div style="color: white; font-weight: 500; display: flex; align-items: center; gap: 8px;">
                    🔊 <span style="font-size: 14px;">Audio Response</span>
                </div>
                <audio controls style="
                    height: 35px;
                    border-radius: 17px;
                    outline: none;
                    flex: 1;
                    min-width: 200px;
                ">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
                    Your browser does not support audio playback.
                </audio>
            </div>
        </div>
        """
        
        return audio_html
    
    def test_voice(self, voice: str) -> Optional[bytes]:
        """Test a voice with a sample text"""
        test_text = "Hello! This is how I will sound when reading responses to you."
        return self.generate_audio_response(test_text, voice)