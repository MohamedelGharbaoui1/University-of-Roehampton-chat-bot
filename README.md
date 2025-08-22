# University of Roehampton Chatbot - Refactored

A modular, intelligent academic assistant for University of Roehampton students, providing coursework support and ethics guidance through a guided conversation interface.

## 🏗️ Architecture Overview

The application has been refactored into modular components for better maintainability and understanding:

```
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── session_manager.py     # Session state management
├── database_manager.py    # Student database operations 
├── document_processor.py  # Document reading and processing
├── ai_assistant.py        # AI response generation
├── audio_manager.py       # Text-to-speech functionality
├── ui_components.py       # UI components and styling
├── conversation_flows.py  # Conversation flow management
├── localization.py        # Multi-language support
├── ethics_handler.py      # Ethics-specific functionality
└── requirements.txt       # Python dependencies
```

## 📦 Module Descriptions

### Core Modules

#### `ai_assistant.py`

- OpenAI API integration
- Coursework response generation
- Ethics guidance responses
- System prompt management

#### `audio_manager.py`

- Text-to-speech functionality
- Audio response generation
- Voice selection and testing
- Audio player HTML generation

#### `ui_components.py`

- UI component rendering
- CSS styling and theming
- Logo handling
- Welcome screen and sidebar

#### `conversation_flows.py`

- Screen rendering logic
- User input handling
- Navigation between steps
- Chat interface management

#### `localization.py`

- Multi-language support
- Translation management
- RTL language handling
- Language-specific prompts

#### `ethics_handler.py`

- Ethics document processing
- Ethics-specific chat interface
- Reforming Modernity integration
- Ethics response generation

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd university-chatbot

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Directory Structure

Create the following directories:

```
project-root/
├── data/                           # Student documents
│   ├── reforming_modernity.pdf    # Ethics document
│   └── [student-pdfs]             # Coursework documents
├── assets/                        # Static assets
│   └── logo.png                   # University logo
├── translations/                  # Language files (auto-generated)
└── audio_responses/              # Audio cache (auto-generated)
```

### 4. Student Database

Create `student_modules_with_pdfs.xlsx` with columns:

- Student ID
- Code
- Programme
- Module
- PDF File

Example:
| Student ID | Code | Programme | Module | PDF File |
|------------|------|-----------|--------|----------|
| A00034131 | 1234 | Computer Science | Machine Learning | ml_coursework1.pdf |
| A00034131 | 1234 | Computer Science | Machine Learning | ml_coursework2.pdf |

### 5. Run the Application

```bash
streamlit run main.py
```

## 🔧 Configuration Options

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_key_here

# Optional (defaults provided)
MODEL=gpt-3.5-turbo
MAX_TOKENS=1500
TEMPERATURE=0.3
```

### Config Class Settings

Modify `config.py` to customize:

- File paths and folders
- OpenAI model settings
- UI configuration
- Supported file types
- Audio voices

## 🌟 Features

### Student Authentication

- Secure student ID and code validation
- Module access control
- Programme-specific content

### Multi-Document Support

- PDF and DOCX processing
- Multiple documents per module
- Combined document analysis

### Ethics Guidance

- Reforming Modernity document integration
- Ethics-specific responses
- University policy guidance

### Audio Accessibility

- Multiple voice options
- Text-to-speech responses
- Audio player integration

### Multi-Language Support

- English, Arabic, French, Spanish
- RTL language support
- Localized interface

### Responsive Design

- Mobile-friendly interface
- Modern Roehampton branding
- Accessible components

## 🛠️ Development

### Adding New Languages

1. Update `localization.py`:

```python
def _get_new_language_translations(self) -> Dict[str, str]:
    return {
        'app_title': 'Translation here',
        # ... more translations
    }
```

2. Add to language options:

```python
def get_language_options(self) -> Dict[str, str]:
    return {
        'new_lang': '🇫🇷 New Language Name',
        # ... existing languages
    }
```

### Adding New Conversation Flows

1. Create new methods in `conversation_flows.py`
2. Add step to session manager
3. Update main application router

### Customizing AI Responses

Modify prompt templates in `ai_assistant.py`:

- `_create_coursework_system_prompt()`
- `_create_ethics_system_prompt()`

### Adding New Document Types

1. Extend `document_processor.py`
2. Add to `SUPPORTED_EXTENSIONS` in config
3. Implement new reading methods

## 📱 Usage Guide

### For Students

1. **Select Path**: Choose between Ethics or Coursework assistance
2. **Authentication**: Enter Student ID and access code
3. **Module Selection**: Choose your module and documents
4. **Coursework Type**: Select type of help needed
5. **Chat**: Ask questions about your materials

### For Administrators

1. **Student Data**: Maintain Excel file with student information
2. **Documents**: Add PDF/DOCX files to data folder
3. **Ethics**: Ensure reforming_modernity.pdf is available
4. **Monitoring**: Check logs for usage and errors

## 🔍 Troubleshooting

### Common Issues

**Database not loading:**

- Check Excel file format and column names
- Verify file permissions
- Check for special characters in data

**Documents not found:**

- Ensure files are in `data/` folder
- Check file names in Excel match actual files
- Verify file permissions

**Audio not working:**

- Check OpenAI API key
- Verify internet connection
- Try different voice options

**Styling issues:**

- Clear browser cache
- Check CSS conflicts
- Verify Streamlit version

### Debug Mode

Enable detailed logging by setting in `config.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

View session state information in sidebar debug panel.

## 📋 API Reference

### Key Classes

#### `SessionManager`

```python
SessionManager.initialize_session_state()
SessionManager.reset_conversation()
SessionManager.is_authenticated() -> bool
```

#### `DatabaseManager`

```python
DatabaseManager.load_student_database() -> Tuple[Dict, str]
DatabaseManager.validate_student_credentials(id, code) -> Tuple[bool, Dict, str]
```

#### `AIAssistant`

```python
ai_assistant.generate_coursework_response(question, content, module_info) -> str
ai_assistant.generate_ethics_response(question, content, student_info) -> str
```

#### `AudioManager`

```python
audio_manager.generate_audio_response(text, voice) -> Optional[bytes]
audio_manager.create_audio_player(audio_bytes, key) -> str
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the modular architecture
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For technical support:

- Check the troubleshooting section
- Review application logs
- Contact system administrator

For feature requests:

- Create an issue in the repository
- Provide detailed requirements
- Include use case examplesconfig.py`
- Centralized configuration management
- Environment variable handling
- Validation functions
- Constants and settings

#### `session_manager.py`

- Streamlit session state initialization
- State management utilities
- Conversation flow tracking
- Session reset functionality

#### `database_manager.py`

- Student database loading from Excel
- Credential validation
- Module and coursework data access
- Database statistics

#### `document_processor.py`

- PDF and DOCX document reading
- Content extraction and metadata
- Multi-document handling
- Document preview generation

#### `
