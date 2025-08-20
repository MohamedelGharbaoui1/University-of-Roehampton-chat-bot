# session_manager.py - Fixed session state management for the University Chatbot

import streamlit as st
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages Streamlit session state for the University Chatbot"""
    
    @staticmethod
    def initialize_session_state() -> None:
        """Initialize all session state variables with proper defaults"""
        
        # Conversation flow states
        if 'conversation_step' not in st.session_state:
            st.session_state.conversation_step = 'welcome'
        
        # Authentication data - Initialize with None
        auth_keys = ['student_id', 'student_code', 'student_data', 'selected_path']
        for key in auth_keys:
            if key not in st.session_state:
                st.session_state[key] = None
        
        # Module and coursework selection
        if 'available_modules' not in st.session_state:
            st.session_state.available_modules = []
        if 'selected_module' not in st.session_state:
            st.session_state.selected_module = None
        if 'selected_coursework' not in st.session_state:
            st.session_state.selected_coursework = None
        if 'current_document' not in st.session_state:
            st.session_state.current_document = None
        
        # Chat data
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'audio_enabled' not in st.session_state:
            st.session_state.audio_enabled = True
        if 'selected_voice' not in st.session_state:
            st.session_state.selected_voice = 'alloy'
        if 'audio_responses' not in st.session_state:
            st.session_state.audio_responses = {}
        
        # Error handling
        if 'error_message' not in st.session_state:
            st.session_state.error_message = None
        if 'retry_count' not in st.session_state:
            st.session_state.retry_count = 0
        
        # Database
        if 'student_database' not in st.session_state:
            st.session_state.student_database = None
        if 'database_loaded' not in st.session_state:
            st.session_state.database_loaded = False
        
        # Ethics-specific states
        if 'selected_ethics_category' not in st.session_state:
            st.session_state.selected_ethics_category = None
        if 'ethics_document' not in st.session_state:
            st.session_state.ethics_document = None
        
        # Language system
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        
        logger.info("Session state initialized successfully")
    
    @staticmethod
    def reset_conversation() -> None:
        """Reset conversation to welcome state"""
        # Reset conversation flow states
        st.session_state.conversation_step = 'welcome'
        
        # Reset authentication data
        st.session_state.student_id = None
        st.session_state.student_code = None
        st.session_state.student_data = None
        st.session_state.selected_path = None
        
        # Reset module and coursework selection
        st.session_state.available_modules = []
        st.session_state.selected_module = None
        st.session_state.selected_coursework = None
        st.session_state.current_document = None
        
        # Reset chat data
        st.session_state.messages = []
        st.session_state.audio_responses = {}
        
        # Reset error handling
        st.session_state.error_message = None
        st.session_state.retry_count = 0
        
        # Reset ethics-specific states
        st.session_state.selected_ethics_category = None
        if 'ethics_document' in st.session_state:
            st.session_state.ethics_document = None
        
        logger.info("Conversation reset successfully")
    
    @staticmethod
    def clear_chat() -> None:
        """Clear only chat messages and audio responses"""
        st.session_state.messages = []
        st.session_state.audio_responses = {}
        logger.info("Chat cleared successfully")
    
    @staticmethod
    def clear_error() -> None:
        """Clear error messages"""
        st.session_state.error_message = None
        st.session_state.retry_count = 0
    
    @staticmethod
    def set_error(message: str) -> None:
        """Set error message and increment retry count"""
        st.session_state.error_message = message
        st.session_state.retry_count = st.session_state.get('retry_count', 0) + 1
    
    @staticmethod
    def get_session_info() -> Dict[str, Any]:
        """Get current session information for debugging"""
        return {
            'conversation_step': st.session_state.get('conversation_step'),
            'student_id': st.session_state.get('student_id'),
            'selected_path': st.session_state.get('selected_path'),
            'selected_module': st.session_state.get('selected_module'),
            'messages_count': len(st.session_state.get('messages', [])),
            'database_loaded': st.session_state.get('database_loaded', False),
            'language': st.session_state.get('language', 'en'),
            'error_message': st.session_state.get('error_message'),
            'retry_count': st.session_state.get('retry_count', 0)
        }
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is properly authenticated"""
        return (
            st.session_state.get('student_id') is not None and
            st.session_state.get('student_code') is not None and
            st.session_state.get('student_data') is not None
        )
    
    @staticmethod
    def has_selected_module() -> bool:
        """Check if user has selected a module"""
        return st.session_state.get('selected_module') is not None
    
    @staticmethod
    def has_selected_coursework() -> bool:
        """Check if user has selected coursework type"""
        return st.session_state.get('selected_coursework') is not None
    
    @staticmethod
    def get_current_step() -> str:
        """Get current conversation step"""
        return st.session_state.get('conversation_step', 'welcome')
    
    @staticmethod
    def set_step(step: str) -> None:
        """Set conversation step"""
        st.session_state.conversation_step = step
        logger.info(f"Conversation step set to: {step}")
    
    @staticmethod
    def debug_session_state() -> None:
        """Debug function to display session state (for development)"""
        if st.checkbox("🔧 Show Session State Debug Info"):
            st.json(SessionManager.get_session_info())
            
            with st.expander("Full Session State"):
                # Filter out potentially large data
                filtered_state = {}
                for key, value in st.session_state.items():
                    if key in ['student_database', 'current_document', 'audio_responses']:
                        if isinstance(value, dict):
                            filtered_state[key] = f"<dict with {len(value)} keys>"
                        elif isinstance(value, list):
                            filtered_state[key] = f"<list with {len(value)} items>"
                        else:
                            filtered_state[key] = f"<{type(value).__name__}>"
                    else:
                        filtered_state[key] = value
                
                st.json(filtered_state)