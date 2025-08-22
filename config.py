# config.py - Complete configuration settings for the University Chatbot

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class for the University Chatbot"""
    
    # App Information
    PROJECT_NAME = "Roehampton University Chatbot"
    COMPANY_NAME = "University of Roehampton"
    PAGE_ICON = "🎓"
    
    # Folder Structure
    DATA_FOLDER = "data"
    AUDIO_FOLDER = "audio_responses"
    TEMP_AUDIO_FOLDER = "temp_audio"
    ETHICS_FOLDER = "ethics_documents"
    ASSETS_FOLDER = "assets"
    
    # File Paths
    LOGO_PATH = "logo.png"
    STUDENT_DATA_FILE = "student_modules_with_pdfs.xlsx"
    ETHICS_PDF_FILE = "reforming_modernity.pdf"
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    
    # Text-to-Speech Settings
    TTS_MODEL = "tts-1"
    TTS_VOICE = "alloy"
    SUPPORTED_VOICES = {
        'alloy': 'Alloy (Neutral)',
        'echo': 'Echo (Male)', 
        'fable': 'Fable (British Male)',
        'onyx': 'Onyx (Deep Male)',
        'nova': 'Nova (Female)',
        'shimmer': 'Shimmer (Soft Female)'
    }
    
    # Document Processing
    MAX_CONTENT_LENGTH = 15000
    PREVIEW_LENGTH = 800
    SUPPORTED_EXTENSIONS = ['.pdf', '.docx']
    
    # UI Settings
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    @classmethod
    def validate_setup(cls) -> tuple[bool, list[str]]:
        """Validate that all required configurations are properly set"""
        errors = []
        
        # Check API key
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not found in environment variables")
        
        # Check required folders
        for folder in [cls.DATA_FOLDER]:
            if not Path(folder).exists():
                errors.append(f"Required folder not found: {folder}")
        
        # Check student data file
        student_file = Path(cls.STUDENT_DATA_FILE)
        if not student_file.exists():
            errors.append(f"Student data file not found: {cls.STUDENT_DATA_FILE}")
        
        # Optional folders (create if missing)
        for folder in [cls.ASSETS_FOLDER, cls.AUDIO_FOLDER, cls.TEMP_AUDIO_FOLDER]:
            folder_path = Path(folder)
            if not folder_path.exists():
                try:
                    folder_path.mkdir(exist_ok=True)
                except Exception as e:
                    errors.append(f"Could not create folder {folder}: {str(e)}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def get_env_file_template(cls) -> str:
        """Get a template for the .env file"""
        return """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model Configuration (defaults provided)
# MODEL=gpt-3.5-turbo
# MAX_TOKENS=1500
# TEMPERATURE=0.3
"""
    
    @classmethod
    def create_required_folders(cls) -> list[str]:
        """Create all required folders and return status"""
        folders = [
            cls.DATA_FOLDER,
            cls.ASSETS_FOLDER, 
            cls.AUDIO_FOLDER,
            cls.TEMP_AUDIO_FOLDER
        ]
        
        created = []
        for folder in folders:
            folder_path = Path(folder)
            if not folder_path.exists():
                try:
                    folder_path.mkdir(exist_ok=True)
                    created.append(f"Created folder: {folder}")
                except Exception as e:
                    created.append(f"Failed to create {folder}: {str(e)}")
            else:
                created.append(f"Folder exists: {folder}")
        
        return created
