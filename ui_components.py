# ui_components.py - UI components and styling

import base64
import streamlit as st
import logging
from pathlib import Path
from typing import Optional
from config import Config
from localization import t, language_manager, render_language_selector, get_rtl_css
from audio_manager import AudioManager

logger = logging.getLogger(__name__)

class UIComponents:
    """Handles UI components and styling for the University Chatbot"""
    
    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
    
    @staticmethod
    def load_logo_from_assets() -> Optional[str]:
        """Load logo from assets folder and encode as base64"""
        possible_paths = [
            Path(Config.ASSETS_FOLDER) / "logo.png",
            Path(Config.ASSETS_FOLDER) / "logo.jpg", 
            Path(Config.ASSETS_FOLDER) / "logo.jpeg",
            Path(Config.ASSETS_FOLDER) / "logo.svg",
            Path(Config.ASSETS_FOLDER) / "roehampton_logo.png",
            Path(Config.ASSETS_FOLDER) / "university_logo.png"
        ]
        
        for logo_path in possible_paths:
            if logo_path.exists():
                try:
                    with open(logo_path, "rb") as img_file:
                        img_bytes = img_file.read()
                        img_base64 = base64.b64encode(img_bytes).decode()
                        logger.info(f"Successfully loaded logo from: {logo_path}")
                        return img_base64
                except Exception as e:
                    logger.warning(f"Error loading logo from {logo_path}: {e}")
                    continue
        
        logger.info("No logo found in assets folder")
        return None
    
    @staticmethod
    def get_enhanced_css() -> str:
        """Get enhanced CSS with official Roehampton University brand colors"""
        base_css = """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap');
            
            /* Roehampton University Brand Colors */
            :root {
                --roehampton-green: #00A86B;
                --roehampton-dark-green: #008756;
                --roehampton-light-green: #33BA85;
                --roehampton-navy: #1E3A5F;
                --roehampton-charcoal: #2C3E50;
                --success-color: #00A86B;
                --primary-color: #00A86B;
                --secondary-color: #1E3A5F;
                --error-color: #E74C3C;
                --warning-color: #F39C12;
                --info-color: #3498DB;
                --background-light: #F8FFFE;
                --background-white: #FFFFFF;
                --text-primary: #2C3E50;
                --text-secondary: #7F8C8D;
                --border-color: #E8F5F0;
                --shadow: 0 2px 4px rgba(0, 168, 107, 0.1);
                --shadow-lg: 0 8px 25px rgba(0, 168, 107, 0.15);
            }
            
            /* Global font with multi-language support */
            .main, .sidebar .sidebar-content {
                font-family: 'Inter', 'Noto Sans Arabic', 'Arial', sans-serif !important;
                background-color: var(--background-light);
            }
            
            /* Arabic text specific styling */
            [lang="ar"], .arabic-text {
                font-family: 'Noto Sans Arabic', 'Arial', 'Tahoma', sans-serif !important;
                line-height: 1.8 !important;
                text-align: right !important;
            }
            
            /* Roehampton University Branded Header */
            .roehampton-header {
                background: linear-gradient(135deg, var(--roehampton-green), var(--roehampton-dark-green));
                padding: 2.5rem 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
                box-shadow: var(--shadow-lg);
                position: relative;
                overflow: hidden;
            }
            
            .roehampton-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: shimmer 3s infinite;
            }
            
            @keyframes shimmer {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .logo-title-container {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 2rem;
                margin-bottom: 1rem;
                position: relative;
                z-index: 1;
            }
            
            .roehampton-logo {
                height: 90px;
                width: auto;
                background: white;
                padding: 0.75rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            
            .roehampton-header h1 {
                margin: 0;
                font-weight: 700;
                font-size: 2.8rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .roehampton-header p {
                margin: 0;
                opacity: 0.95;
                font-size: 1.3rem;
                font-weight: 400;
            }
            
            /* Feature grid for welcome screen */
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1.5rem;
                margin: 2rem 0;
            }
            
            .feature-card {
                background: var(--background-white);
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow);
                transition: all 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-3px);
                box-shadow: var(--shadow-lg);
                border-color: var(--roehampton-light-green);
            }
            
            .feature-icon {
                font-size: 2.5rem;
                margin-bottom: 1rem;
                text-align: center;
            }
            
            .feature-title {
                font-size: 1.2rem;
                font-weight: 600;
                color: var(--roehampton-green);
                margin-bottom: 0.5rem;
                text-align: center;
            }
            
            .feature-description {
                color: var(--text-secondary);
                text-align: center;
                line-height: 1.5;
            }
            
            /* Branded Buttons */
            .stButton > button {
                border-radius: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
                border: none;
                font-size: 1.1rem;
                padding: 0.8rem 1.5rem;
            }
            
            .stButton > button[data-baseweb="button"][kind="primary"] {
                background: linear-gradient(135deg, var(--roehampton-green), var(--roehampton-dark-green));
                color: white;
                box-shadow: var(--shadow);
            }
            
            .stButton > button[data-baseweb="button"][kind="primary"]:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
                background: linear-gradient(135deg, var(--roehampton-dark-green), var(--roehampton-green));
            }
            
            .stButton > button[data-baseweb="button"][kind="secondary"] {
                background: white;
                color: var(--roehampton-green);
                border: 2px solid var(--roehampton-green);
            }
            
            .stButton > button[data-baseweb="button"][kind="secondary"]:hover {
                background: var(--roehampton-green);
                color: white;
                transform: translateY(-1px);
            }
            
            /* Progress indicator */
            .stProgress > div > div > div {
                background: linear-gradient(90deg, var(--roehampton-green), var(--roehampton-light-green));
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .roehampton-header h1 {
                    font-size: 2rem;
                }
                
                .logo-title-container {
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .roehampton-logo {
                    height: 70px;
                }
            }
        </style>
        """
        
        # Add RTL-specific CSS if needed
        rtl_css = get_rtl_css()
        return base_css + rtl_css
    
    def render_voice_selector(self):
        """Render voice selector in sidebar"""
        st.markdown(f"### 🎤 {t('voice_settings', default='Voice Settings')}")
        
        # Audio toggle
        current_audio_state = st.session_state.get('audio_enabled', True)
        audio_enabled = st.checkbox(
            f"🔊 {t('enable_audio', default='Enable Audio Responses')}", 
            value=current_audio_state,
            help=t('audio_help', default='Toggle audio responses for accessibility')
        )
        st.session_state.audio_enabled = audio_enabled
        
        if audio_enabled:
            # Voice selection
            voice_options = list(Config.SUPPORTED_VOICES.keys())
            current_voice = st.session_state.get('selected_voice', Config.TTS_VOICE)
            
            # Find current voice index
            try:
                current_index = voice_options.index(current_voice)
            except ValueError:
                current_index = 0
            
            selected_voice = st.selectbox(
                f"🎭 {t('select_voice', default='Select Voice')}", 
                options=voice_options,
                format_func=lambda x: Config.SUPPORTED_VOICES[x],
                index=current_index,
                help=t('voice_help', default='Choose the voice for audio responses')
            )
            
            st.session_state.selected_voice = selected_voice
            
            # Test voice button
            if st.button(f"🎵 {t('test_voice', default='Test Voice')}", type="secondary"):
                if self.audio_manager.is_available():
                    with st.spinner(t('generating_audio', default='Generating audio...')):
                        audio_bytes = self.audio_manager.test_voice(selected_voice)
                        
                    if audio_bytes:
                        audio_html = self.audio_manager.create_audio_player(audio_bytes, key="voice_test")
                        st.markdown(audio_html, unsafe_allow_html=True)
                        st.success(t('audio_ready', default='Audio ready!'))
                    else:
                        st.error(t('audio_error', default='Failed to generate audio'))
                else:
                    st.error("Audio service not available")
        else:
            st.info(t('audio_disabled', default='Audio responses are disabled'))
    
    def render_welcome_screen(self):
        """Render welcome screen with official Roehampton University branding"""
        logo_base64 = self.load_logo_from_assets()
        
        if logo_base64:
            st.markdown(f"""
            <div class="roehampton-header">
                <div class="logo-title-container">
                    <img src="data:image/png;base64,{logo_base64}" alt="University of Roehampton Logo" class="roehampton-logo">
                    <div>
                        <h1>University Assistant</h1>
                    </div>
                </div>
                <p>Your intelligent academic companion for coursework and ethics guidance</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="roehampton-header">
                <h1>🎓 University of Roehampton Assistant</h1>
                <p>Your intelligent academic companion for coursework and ethics guidance</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### How can I help you today?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Ethics Document Help", 
                        help="Get assistance with ethics-related documents and guidelines",
                        use_container_width=True,
                        type="primary",
                        key="welcome_ethics_btn"):
                st.session_state.selected_path = 'ethics'
                st.session_state.conversation_step = 'student_id'
                st.rerun()
        
        with col2:
            if st.button("📚 University Coursework Help", 
                        help="Get help with your specific coursework materials",
                        use_container_width=True,
                        type="primary",
                        key="welcome_coursework_btn"):
                st.session_state.selected_path = 'coursework'
                st.session_state.conversation_step = 'student_id'
                st.rerun()
        
        # Feature highlights
        st.markdown("---")
        st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Ethics Guidance</div>
                <div class="feature-description">Access comprehensive ethics guidance based on university policies and the "Reforming Modernity" framework</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Coursework Support</div>
                <div class="feature-description">Get personalized help with your module materials, assignments, and academic questions</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">Secure Access</div>
                <div class="feature-description">Student authentication ensures you only access your own academic materials and information</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Audio Support</div>
                <div class="feature-description">Listen to responses with text-to-speech functionality for enhanced accessibility</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional information
        st.markdown("---")
        st.markdown("""
        **What you can do:**
        - 📋 **Ethics Documents**: Access university ethics guidelines and policies
        - 📚 **Coursework Help**: Get assistance with your enrolled modules and assignments
        - 🔐 **Secure Access**: Authentication ensures you only see your own materials
        - 🎤 **Audio Support**: Listen to responses with text-to-speech functionality
        """)
    
    @staticmethod
    def render_progress_indicator():
        """Render progress indicator for guided flow"""
        steps = {
            'welcome': 1,
            'path_selection': 1,
            'student_id': 2,
            'code': 3,
            'module': 4,
            'coursework': 5,
            'chat': 6
        }
        
        current_step = steps.get(st.session_state.conversation_step, 1)
        total_steps = 6
        
        progress = current_step / total_steps
        
        st.progress(progress)
        st.caption(f"Step {current_step} of {total_steps}")
    
    def render_sidebar(self, database_stats: dict):
        """Render sidebar with student info and controls"""
        with st.sidebar:
            # Language selector
            st.markdown(f"### 🌐 {t('language_selector')}")
            render_language_selector()
            
            # Voice settings
            self.render_voice_selector()
            
            st.markdown("---")
            
            # Student information (if authenticated)
            if st.session_state.student_id and st.session_state.student_data:
                st.markdown("### 👤 Student Information")
                st.markdown(f"""
                <div style="background: #f0f2f6; color: #000; padding: 1rem; border-radius: 8px;">
                    <p><strong>ID:</strong> {st.session_state.student_id}</p>
                    <p><strong>Programme:</strong> {st.session_state.student_data['programme']}</p>
                    <p><strong>Modules:</strong> {len(st.session_state.available_modules)}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
            
            # Current session info
            if st.session_state.conversation_step != 'welcome':
                st.markdown("### 📍 Current Session")
                st.markdown(f"**Path:** {st.session_state.selected_path or 'Not selected'}")
                
                if st.session_state.selected_path == 'ethics':
                    st.markdown("**Document:** Reforming Modernity")
                    if st.session_state.selected_ethics_category:
                        st.markdown(f"**Category:** {st.session_state.selected_ethics_category['title']}")
                elif st.session_state.selected_module:
                    st.markdown(f"**Module:** {st.session_state.selected_module['module']}")
                    if st.session_state.selected_coursework:
                        st.markdown(f"**Type:** {st.session_state.selected_coursework['title']}")
                
                st.markdown("---")
            
            # Database status
            st.markdown("### 📊 System Status")
            if st.session_state.database_loaded:
                st.success("✅ Database Connected")
                st.markdown(f"**Students:** {database_stats['students']}")
                st.markdown(f"**Programmes:** {database_stats['programmes']}")
            else:
                st.error("❌ Database Not Loaded")
            
            if Config.OPENAI_API_KEY:
                st.success("✅ AI Service Connected")
            else:
                st.error("❌ AI Service Not Available")
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            
            if st.button("🏠 Start Over", use_container_width=True, type="secondary"):
                from session_manager import SessionManager
                SessionManager.reset_conversation()
                st.rerun()
            
            if st.session_state.conversation_step == 'chat':
                if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
                    from session_manager import SessionManager
                    SessionManager.clear_chat()
                    st.rerun()