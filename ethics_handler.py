# ethics_handler.py - Direct access ethics interface with multi-language support

import streamlit as st
import os
import time
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from openai import OpenAI
import traceback

# Import from your existing modules
from localization import t, language_manager

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

class EthicsConfig:
    """Configuration for ethics document handling"""
    ETHICS_PDF_FILE = "reforming_modernity.pdf"
    DATA_FOLDER = "data"
    MAX_TOKENS = 1500
    TEMPERATURE = 0.3
    MODEL = "gpt-3.5-turbo"
    MAX_CONTENT_LENGTH = 15000

def get_language_name(lang_code: str) -> str:
    """Get full language name for the AI prompt"""
    language_names = {
        'en': 'English',
        'ar': 'Arabic',
        'fr': 'French',
        'es': 'Spanish'
    }
    return language_names.get(lang_code, 'English')

def get_language_specific_instructions(language_code: str, language_name: str) -> str:
    """Get language-specific instructions for the ethics AI"""
    if language_code == 'en':
        return "LANGUAGE: Respond in English."
    
    elif language_code == 'ar':
        return f"""LANGUAGE REQUIREMENTS:
- RESPOND ENTIRELY IN ARABIC ({language_name})
- Use proper Arabic grammar and formal academic language
- Write from right to left as appropriate for Arabic
- Use Arabic academic and ethical terminology when available
- Maintain respectful and formal tone appropriate for Arabic academic context
- When discussing ethical concepts, use traditional Arabic ethical terminology where appropriate
- If you need to reference English terms or names, you may include them in parentheses after the Arabic translation"""
    
    elif language_code == 'fr':
        return f"""LANGUAGE REQUIREMENTS:
- RESPOND ENTIRELY IN FRENCH ({language_name})
- Use proper French grammar and academic language
- Use formal "vous" form when addressing the student
- Use French ethical and philosophical terminology when available
- Maintain professional and supportive tone appropriate for French academic context
- Use proper French accents and punctuation"""
    
    elif language_code == 'es':
        return f"""LANGUAGE REQUIREMENTS:
- RESPOND ENTIRELY IN SPANISH ({language_name})
- Use proper Spanish grammar and academic language
- Use formal "usted" form when addressing the student
- Use Spanish ethical and philosophical terminology when available
- Maintain professional and supportive tone appropriate for Spanish academic context
- Use proper Spanish accents and punctuation"""
    
    else:
        return f"LANGUAGE: Respond in {language_name}."

def load_ethics_document() -> Tuple[Optional[str], Dict[str, Any], str]:
    """Load the ethics document (reforming_modernity.pdf) with better error handling"""
    try:
        pdf_path = Path(EthicsConfig.DATA_FOLDER) / EthicsConfig.ETHICS_PDF_FILE
        
        logger.info(f"Attempting to load ethics document from: {pdf_path}")
        
        if not pdf_path.exists():
            error_msg = f"Ethics document not found: {pdf_path}"
            logger.error(error_msg)
            return None, {}, error_msg
        
        # Check if the file is readable
        if not os.access(pdf_path, os.R_OK):
            error_msg = f"Cannot read ethics document: {pdf_path} (permission denied)"
            logger.error(error_msg)
            return None, {}, error_msg
        
        # Import the document reading functions from your main app
        try:
            from document_processor import DocumentProcessor
            logger.info("Successfully imported DocumentProcessor")
        except ImportError as e:
            error_msg = f"Cannot import DocumentProcessor: {e}"
            logger.error(error_msg)
            return None, {}, error_msg
        
        logger.info(f"Reading document: {pdf_path}")
        content, metadata = DocumentProcessor.read_document(pdf_path)
        
        if content and content.strip():
            logger.info(f"Successfully loaded ethics document: {EthicsConfig.ETHICS_PDF_FILE}")
            logger.info(f"Content length: {len(content)} characters")
            return content, metadata, f"Loaded {EthicsConfig.ETHICS_PDF_FILE} successfully"
        else:
            error_msg = f"Failed to extract content from {EthicsConfig.ETHICS_PDF_FILE}"
            logger.error(error_msg)
            return None, metadata or {}, error_msg
            
    except Exception as e:
        error_msg = f"Error loading ethics document: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return None, {}, error_msg

def generate_ethics_response(question: str, document_content: str) -> str:
    """Generate AI response for ethics-related questions with multi-language support"""
    try:
        logger.info("Starting ethics response generation")
        
        if not client:
            return t('api_key_missing')
        
        if not document_content or not document_content.strip():
            return t('no_docs_error')
        
        if not question or not question.strip():
            return t('enter_ethics_question')
        
        # Get current language
        current_language = getattr(st.session_state, 'language', 'en')
        language_name = get_language_name(current_language)
        
        logger.info(f"Language: {current_language}")
        
        # Truncate content if too long
        truncated_content = document_content[:EthicsConfig.MAX_CONTENT_LENGTH]
        
        # Language-specific instructions
        language_instructions = get_language_specific_instructions(current_language, language_name)
        
        system_prompt = f"""You are an expert ethics advisor providing guidance based on the "Reforming Modernity" document. You help anyone seeking ethical guidance and understanding.

ETHICS DOCUMENT CONTENT:
{truncated_content}

INSTRUCTIONS:
- Answer ethics questions based ONLY on the provided "Reforming Modernity" document content
- Provide thoughtful, well-reasoned ethical guidance based on what's actually in the document
- Reference specific sections, concepts, or examples from the document when relevant
- If the document discusses specific ethical frameworks, theories, or principles, use those
- Help users understand and apply the ethical concepts presented in this document
- Encourage critical thinking about ethical issues as presented in the material
- Be supportive and educational in your approach
- If a question cannot be answered from the document content, clearly state this and suggest what topics the document does cover
- Always maintain academic integrity and professional ethics standards

CONTEXT:
- Document: Reforming Modernity (University Ethics Material)
- Purpose: Ethics guidance based on this specific document
- Audience: Anyone seeking ethical understanding

{language_instructions}

Remember: Base your responses strictly on the actual content of the "Reforming Modernity" document. If the document focuses on specific ethical themes, theories, or applications, emphasize those in your responses."""

        # Add language instruction to user question if not English
        if current_language != 'en':
            language_instruction = f"Please respond in {language_name}. "
            question = language_instruction + question

        logger.info("Making OpenAI API call")
        response = client.chat.completions.create(
            model=EthicsConfig.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=EthicsConfig.MAX_TOKENS,
            temperature=EthicsConfig.TEMPERATURE,
        )
        
        if response and response.choices and len(response.choices) > 0:
            result = response.choices[0].message.content.strip()
            logger.info("Successfully generated ethics response")
            return result
        else:
            return t('no_response_generated', default="No response generated from OpenAI")
        
    except Exception as e:
        error_msg = t('response_error', error=str(e), default=f"Error generating response: {str(e)}")
        logger.error(f"Error in generate_ethics_response: {str(e)}")
        return error_msg

def render_ethics_chat_interface():
    """Render the direct access ethics chat interface with multi-language support"""
    try:
        logger.info("Starting direct access ethics chat interface")
        
        # Load ethics document if not already loaded
        if 'ethics_document' not in st.session_state or st.session_state.ethics_document is None:
            logger.info("Loading ethics document for the first time")
            loading_msg = t('loading_materials', default="Loading ethics guidance materials...")
            with st.spinner(loading_msg):
                content, metadata, message = load_ethics_document()
                
                if content and content.strip():
                    st.session_state.ethics_document = {
                        'content': content,
                        'metadata': metadata,
                        'filename': EthicsConfig.ETHICS_PDF_FILE
                    }
                    st.success(message)
                    logger.info("Ethics document loaded successfully")
                else:
                    st.error(f"❌ **{message}**")
                    st.info("Please ensure 'reforming_modernity.pdf' is in your data folder and is readable.")
                    logger.error(f"Failed to load ethics document: {message}")
                    
                    # Debug information
                    with st.expander("🔧 Debug Information", expanded=False):
                        st.code(f"""
                        Expected file path: {Path(EthicsConfig.DATA_FOLDER) / EthicsConfig.ETHICS_PDF_FILE}
                        File exists: {Path(EthicsConfig.DATA_FOLDER / EthicsConfig.ETHICS_PDF_FILE).exists()}
                        Data folder exists: {Path(EthicsConfig.DATA_FOLDER).exists()}
                        Content received: {content is not None}
                        Content length: {len(content) if content else 0}
                        Metadata: {metadata}
                        """)
                    
                    if st.button(t('back_to_welcome')):
                        st.session_state.conversation_step = 'welcome'
                        st.rerun()
                    return
        
        # Header for ethics assistance with translation support
        current_language = getattr(st.session_state, 'language', 'en')
        lang_attr = f'lang="{current_language}"' if current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 📋 {t('ethics_guidance')}")
        st.markdown(f"**{t('ethics_document')}:** Reforming Modernity")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show document info
        with st.expander(t('about_ethics_document'), expanded=False):
            metadata = st.session_state.ethics_document.get('metadata', {})
            st.markdown(f"""
            **Document:** {EthicsConfig.ETHICS_PDF_FILE}
            **Pages:** {metadata.get('total_pages', 'Unknown')}
            **Words:** {metadata.get('word_count', 'Unknown')}
            **File Size:** {metadata.get('file_size', 'Unknown')} bytes
            
            This AI assistant will help you understand and apply the ethical concepts and guidance contained in this document.
            """)
        
        # General example questions with translations
        with st.expander(t('ethics_assistant_usage'), expanded=False):
            st.markdown(f"**{t('ethics_examples')}**")
            st.markdown(f"- \"{t('ethics_example_1')}\"")
            st.markdown(f"- \"{t('ethics_example_2')}\"")
            st.markdown(f"- \"{t('ethics_example_3')}\"")
            st.markdown(f"- \"{t('ethics_example_4')}\"")
            
            st.markdown(f"**{t('ethics_tips')}**")
            st.markdown(f"- {t('ethics_tip_1')}")
            st.markdown(f"- {t('ethics_tip_2')}")
            st.markdown(f"- {t('ethics_tip_3')}")
        
        # Initialize messages if not exists
        if 'ethics_messages' not in st.session_state:
            st.session_state.ethics_messages = []
        
        if 'ethics_audio_responses' not in st.session_state:
            st.session_state.ethics_audio_responses = {}
        
        # Chat messages display with translation support
        for i, message in enumerate(st.session_state.ethics_messages):
            if not isinstance(message, dict):
                logger.warning(f"Invalid message format at index {i}: {message}")
                continue
                
            message_key = f"ethics_msg_{i}_{message.get('timestamp', time.time())}"
            
            if message.get("role") == "user":
                st.markdown(f"""
                <div style="background: #e8f4fd; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #1976d2;" {lang_attr}>
                    <strong>🙋 {t('you')}:</strong><br>{message.get('content', '')}
                </div>
                """, unsafe_allow_html=True)
            elif message.get("role") == "assistant":
                st.markdown(f"""
                <div style="background: #f3e5f5; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #7b1fa2;" {lang_attr}>
                    <strong>📋 {t('ethics_advisor')}:</strong><br>{message.get('content', '')}
                </div>
                """, unsafe_allow_html=True)
                
                # Add audio support if enabled
                if st.session_state.get('audio_enabled', True):
                    if message_key not in st.session_state.ethics_audio_responses:
                        try:
                            from audio_manager import AudioManager
                            audio_manager = AudioManager()
                            if audio_manager.is_available():
                                with st.spinner(t('generating_audio')):
                                    audio_bytes = audio_manager.generate_audio_response(
                                        message.get('content', ''), 
                                        st.session_state.get('selected_voice', 'alloy')
                                    )
                                    if audio_bytes:
                                        st.session_state.ethics_audio_responses[message_key] = audio_bytes
                        except Exception as e:
                            logger.error(f"Error generating audio: {e}")
                    
                    # Display audio player if available
                    if message_key in st.session_state.ethics_audio_responses:
                        try:
                            from audio_manager import AudioManager
                            audio_manager = AudioManager()
                            audio_html = audio_manager.create_audio_player(
                                st.session_state.ethics_audio_responses[message_key], 
                                key=message_key
                            )
                            st.markdown(audio_html, unsafe_allow_html=True)
                        except Exception as e:
                            logger.error(f"Error displaying audio player: {e}")
        
        # Chat input with translation
        placeholder_text = t('ethics_placeholder')
        if prompt := st.chat_input(placeholder_text):
            try:
                logger.info(f"Processing user input: {prompt[:100]}...")
                
                # Add user message
                st.session_state.ethics_messages.append({
                    "role": "user",
                    "content": prompt,
                    "timestamp": time.time()
                })
                
                # Generate ethics response
                consulting_msg = t('consulting_ethics')
                with st.spinner(consulting_msg):
                    ethics_doc = st.session_state.get('ethics_document')
                    if not ethics_doc or not ethics_doc.get('content'):
                        st.error(t('no_docs_error'))
                        return
                    
                    response = generate_ethics_response(
                        prompt,
                        ethics_doc['content']
                    )
                
                # Add AI response
                ai_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": time.time()
                }
                st.session_state.ethics_messages.append(ai_message)
                
                logger.info("Successfully processed user input and generated response")
                st.rerun()
                
            except Exception as e:
                error_msg = t('response_error', error=str(e), default=f"Error processing your question: {str(e)}")
                st.error(error_msg)
                logger.error(f"Error processing chat input: {str(e)}")
        
        # Control buttons with translation support
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button(f"🔄 {t('new_session')}", type="secondary"):
                st.session_state.ethics_messages = []
                st.session_state.ethics_audio_responses = {}
                st.rerun()
        
        with col2:
            if st.button(f"🔙 {t('back_to_menu')}", type="secondary"):
                st.session_state.conversation_step = 'welcome'
                # Don't clear ethics messages - keep them for when user returns
                st.rerun()
        
        with col3:
            if st.button(f"🗑️ {t('clear_chat')}", type="secondary"):
                st.session_state.ethics_messages = []
                st.session_state.ethics_audio_responses = {}
                st.rerun()
                
    except Exception as e:
        critical_error_msg = t('critical_error', default='Critical error in ethics interface')
        st.error(f"❌ **{critical_error_msg}**: {str(e)}")
        logger.error(f"Critical error in render_ethics_chat_interface: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Show debug information
        with st.expander("🔧 Debug Information", expanded=True):
            st.code(f"""
            Error: {str(e)}
            Session state keys: {list(st.session_state.keys())}
            Current language: {getattr(st.session_state, 'language', 'Not set')}
            Ethics document loaded: {'ethics_document' in st.session_state}
            """)
        
        if st.button(t('back_to_welcome')):
            st.session_state.conversation_step = 'welcome'
            st.rerun()

def initialize_ethics_session_state():
    """Initialize ethics-specific session state variables"""
    try:
        if 'ethics_document' not in st.session_state:
            st.session_state.ethics_document = None
        if 'ethics_messages' not in st.session_state:
            st.session_state.ethics_messages = []
        if 'ethics_audio_responses' not in st.session_state:
            st.session_state.ethics_audio_responses = {}
        logger.info("Ethics session state initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing ethics session state: {e}")
