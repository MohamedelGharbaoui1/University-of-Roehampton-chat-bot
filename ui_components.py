# ui_components.py - UI components and styling with translation support

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
    """Handles UI components and styling for the University Chatbot with translation support"""
    
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
        """Get enhanced CSS with official Roehampton University brand colors and RTL support"""
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
                direction: rtl;
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
            
            /* Language selector styling */
            .language-info {
                background: var(--background-white);
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid var(--roehampton-green);
                margin-bottom: 1rem;
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
        """Render voice selector in sidebar with translation support"""
        st.markdown(f"### 🎤 {t('voice_settings')}")
        
        # Audio toggle
        current_audio_state = st.session_state.get('audio_enabled', True)
        audio_enabled = st.checkbox(
            f"🔊 {t('enable_audio')}", 
            value=current_audio_state,
            help=t('audio_help')
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
                f"🎭 {t('select_voice')}", 
                options=voice_options,
                format_func=lambda x: Config.SUPPORTED_VOICES[x],
                index=current_index,
                help=t('voice_help')
            )
            
            st.session_state.selected_voice = selected_voice
            
            # Test voice button
            if st.button(f"🎵 {t('test_voice')}", type="secondary"):
                if self.audio_manager.is_available():
                    with st.spinner(t('generating_audio')):
                        audio_bytes = self.audio_manager.test_voice(selected_voice)
                        
                    if audio_bytes:
                        audio_html = self.audio_manager.create_audio_player(audio_bytes, key="voice_test")
                        st.markdown(audio_html, unsafe_allow_html=True)
                        st.success(t('audio_ready'))
                    else:
                        st.error(t('audio_error'))
                else:
                    st.error(t('ai_service_unavailable'))
        else:
            st.info(t('audio_disabled'))
    
    def render_welcome_screen(self):
        """Render welcome screen with translation support"""
        logo_base64 = self.load_logo_from_assets()
        
        # Get translated content
        app_title = t('app_title')
        app_subtitle = t('app_subtitle')
        welcome_message = t('welcome_message')
        
        if logo_base64:
            st.markdown(f"""
            <div class="roehampton-header" {f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''}>
                <div class="logo-title-container">
                    <img src="data:image/png;base64,{logo_base64}" alt="University of Roehampton Logo" class="roehampton-logo">
                    <div>
                        <h1>{app_title}</h1>
                    </div>
                </div>
                <p>{app_subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="roehampton-header" {f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''}>
                <h1>🎓 {app_title}</h1>
                <p>{app_subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### {welcome_message}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"📋 {t('ethics_document_help')}", 
                        help=t('ethics_help_desc'),
                        use_container_width=True,
                        type="primary",
                        key="welcome_ethics_btn"):
                st.session_state.selected_path = 'ethics'
                st.session_state.conversation_step = 'ethics_chat'
                st.rerun()
        
        with col2:
            if st.button(f"📚 {t('coursework_help')}", 
                        help=t('coursework_help_desc'),
                        use_container_width=True,
                        type="primary",
                        key="welcome_coursework_btn"):
                st.session_state.selected_path = 'coursework'
                st.session_state.conversation_step = 'student_id'
                st.rerun()
        
        # Feature highlights with translations
        st.markdown("---")
        feature_grid_lang = f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''
        st.markdown(f"""
        <div class="feature-grid" {feature_grid_lang}>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">{t('feature_ethics_title')}</div>
                <div class="feature-description">{t('feature_ethics_desc')}</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">{t('feature_coursework_title')}</div>
                <div class="feature-description">{t('feature_coursework_desc')}</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">{t('feature_secure_title')}</div>
                <div class="feature-description">{t('feature_secure_desc')}</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">{t('feature_audio_title')}</div>
                <div class="feature-description">{t('feature_audio_desc')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_progress_indicator():
        """Render progress indicator for guided flow with translation support"""
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
        st.caption(t('step_label', current=current_step, total=total_steps))
    
    def render_sidebar(self, database_stats: dict):
        """Render sidebar with student info and controls with translation support"""
        with st.sidebar:
            # Language selector
            st.markdown(f"### 🌍 {t('language_selector')}")
            render_language_selector()
            
            # Voice settings
            self.render_voice_selector()
            
            st.markdown("---")
            
            # Student information (if authenticated)
            if st.session_state.student_id and st.session_state.student_data:
                st.markdown(f"### 👤 {t('student_information')}")
                st.markdown(f"""
                <div style="background: #f0f2f6; color: #000; padding: 1rem; border-radius: 8px;">
                    <p><strong>ID:</strong> {st.session_state.student_id}</p>
                    <p><strong>{t('programme_label')}</strong> {st.session_state.student_data['programme']}</p>
                    <p><strong>{t('module_label')}</strong> {len(st.session_state.available_modules)}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
            
            # Current session info
            if st.session_state.conversation_step != 'welcome':
                st.markdown(f"### 📁 {t('current_session')}")
                st.markdown(f"**Path:** {st.session_state.selected_path or 'Not selected'}")
                
                if st.session_state.selected_path == 'ethics':
                    st.markdown(f"**{t('ethics_document')}:** Reforming Modernity")
                elif st.session_state.selected_module:
                    st.markdown(f"**{t('module_label')}** {st.session_state.selected_module['module']}")
                    if st.session_state.selected_coursework:
                        st.markdown(f"**Type:** {st.session_state.selected_coursework['title']}")
                
                st.markdown("---")
            
            # Database status
            st.markdown(f"### 📊 {t('system_status')}")
            if st.session_state.database_loaded:
                st.success(f"✅ {t('database_connected')}")
                st.markdown(f"**Students:** {database_stats['students']}")
                st.markdown(f"**Programmes:** {database_stats['programmes']}")
            else:
                st.error(f"❌ {t('database_not_loaded')}")
            
            if Config.OPENAI_API_KEY:
                st.success(f"✅ {t('ai_service_connected')}")
            else:
                st.error(f"❌ {t('ai_service_unavailable')}")
            
            st.markdown("---")
            
            # Quick actions
            st.markdown(f"### ⚡ {t('quick_actions')}")
            
            if st.button(f"🏠 {t('start_over')}", use_container_width=True, type="secondary"):
                from session_manager import SessionManager
                SessionManager.reset_conversation()
                st.rerun()
            
            if st.session_state.conversation_step == 'chat':
                if st.button(f"🗑️ {t('clear_chat')}", use_container_width=True, type="secondary"):
                    from session_manager import SessionManager
                    SessionManager.clear_chat()
                    st.rerun()