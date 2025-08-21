# app.py - Main University Chatbot Application with Translation Support

import streamlit as st
import logging
import traceback

# Import our modules
from config import Config
from session_manager import SessionManager
from database_manager import DatabaseManager
from ai_assistant import AIAssistant
from audio_manager import AudioManager
from ui_components import UIComponents
from conversation_flows import ConversationFlows
from localization import init_language_system, t

# Import ethics handler if available
try:
    from ethics_handler import render_ethics_chat_interface
    ETHICS_AVAILABLE = True
except ImportError:
    ETHICS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversityChatbot:
    """Main University Chatbot Application with multi-language support"""
    
    def __init__(self):
        self.setup_page_config()
        self.ai_assistant = AIAssistant()
        self.audio_manager = AudioManager()
        self.ui_components = UIComponents(self.audio_manager)
        self.conversation_flows = ConversationFlows(self.ai_assistant, self.audio_manager)
        
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=Config.PROJECT_NAME,
            page_icon=Config.PAGE_ICON,
            layout=Config.LAYOUT,
            initial_sidebar_state=Config.INITIAL_SIDEBAR_STATE,
            menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': f"# {Config.PROJECT_NAME}\n{t('app_subtitle', default='Guided coursework assistant for University of Roehampton students')}"
            }
        )
    
    def initialize_app(self):
        """Initialize the application with translation support"""
        try:
            # Initialize session state
            SessionManager.initialize_session_state()
            
            # Initialize language system
            init_language_system()
            
            # Apply CSS styling (includes RTL support)
            st.markdown(self.ui_components.get_enhanced_css(), unsafe_allow_html=True)
            
            # Load student database if not loaded
            self.load_database()
            
        except Exception as e:
            logger.error(f"Error initializing app: {e}")
            st.error(f"Initialization error: {str(e)}")
    
    def load_database(self):
        """Load student database with translation support"""
        if not st.session_state.database_loaded:
            loading_message = t('loading_docs', default="Loading student database...")
            with st.spinner(loading_message):
                try:
                    database, message = DatabaseManager.load_student_database()
                    if database:
                        st.session_state.student_database = database
                        st.session_state.database_loaded = True
                        logger.info("Student database loaded successfully")
                    else:
                        error_msg = f"Failed to load student database: {message}"
                        st.error(error_msg)
                        self.show_setup_error(message)
                        st.stop()
                except Exception as e:
                    logger.error(f"Database loading error: {e}")
                    st.error(f"Database error: {str(e)}")
                    st.stop()
    
    def show_setup_error(self, message: str):
        """Show setup error information with translation support"""
        st.error(f"❌ **{t('setup_error', default='Setup Error')}:** {message}")
        
        # Validate configuration and show specific errors
        is_valid, errors = Config.validate_setup()
        if not is_valid:
            st.markdown(f"### {t('configuration_issues', default='Configuration Issues')}:")
            for error in errors:
                st.markdown(f"- ❌ {error}")
            
            st.markdown(f"### {t('setup_instructions', default='Setup Instructions')}:")
            st.markdown("""
            1. **Create a `.env` file** with your OpenAI API key:
               ```
               OPENAI_API_KEY=your_api_key_here
               ```
            
            2. **Create required folders:**
               - `data/` - for your documents
               - `assets/` - for logos and images
            
            3. **Add your student data file:** `student_modules_with_pdfs.xlsx`
            
            4. **Add ethics document:** `data/reforming_modernity.pdf`
            """)
    
    def render_current_screen(self):
        """Render the appropriate screen based on conversation step"""
        step = st.session_state.conversation_step
        
        try:
            if step == 'welcome':
                self.ui_components.render_welcome_screen()
            
            elif step == 'student_id':
                self.conversation_flows.render_student_id_input()
            
            elif step == 'code':
                self.conversation_flows.render_code_input()
            
            elif step == 'module':
                self.conversation_flows.render_module_selection()
            
            elif step == 'coursework':
                self.conversation_flows.render_coursework_selection()
            
            elif step == 'chat':
                self.conversation_flows.render_chat_interface()
            
            elif step == 'ethics_chat':
                self.render_ethics_interface()
            
            else:
                unknown_step_msg = t('unknown_step', default="Unknown conversation step. Please restart.")
                st.error(unknown_step_msg)
                if st.button(f"🔄 {t('start_over')}"):
                    SessionManager.reset_conversation()
                    st.rerun()
                    
        except Exception as e:
            logger.error(f"Error rendering screen {step}: {e}")
            self.show_screen_error(e)
    
    def render_ethics_interface(self):
        """Render ethics chat interface with translation support"""
        if ETHICS_AVAILABLE:
            try:
                render_ethics_chat_interface()
            except Exception as e:
                logger.error(f"Error in ethics interface: {e}")
                st.error(f"Ethics interface error: {str(e)}")
                if st.button(f"🔙 {t('back_button')}"):
                    st.session_state.conversation_step = 'welcome'
                    st.rerun()
        else:
            ethics_unavailable_msg = t('ethics_unavailable', default="Ethics assistance is not available.")
            st.error(ethics_unavailable_msg)
            st.info("Please ensure 'reforming_modernity.pdf' is in your data folder and ethics_handler.py is properly configured.")
            if st.button(f"🔙 {t('back_button')}"):
                st.session_state.conversation_step = 'welcome'
                st.rerun()
    
    def render_sidebar(self):
        """Render sidebar with controls and information"""
        try:
            database_stats = DatabaseManager.get_database_stats()
            self.ui_components.render_sidebar(database_stats)
        except Exception as e:
            logger.error(f"Error rendering sidebar: {e}")
            with st.sidebar:
                st.error(f"Sidebar error: {str(e)}")
    
    def render_progress_indicator(self):
        """Render progress indicator if not on welcome screen"""
        if st.session_state.conversation_step != 'welcome':
            try:
                self.ui_components.render_progress_indicator()
                st.markdown("---")
            except Exception as e:
                logger.error(f"Error rendering progress indicator: {e}")
    
    def show_screen_error(self, error: Exception):
        """Show error information for screen rendering issues with translation support"""
        screen_error_msg = t('screen_error', default='Screen Error')
        st.error(f"🚨 **{screen_error_msg}**: {str(error)}")
        
        # Show detailed error information for debugging
        debug_label = t('show_debug', default="Show detailed error information (for debugging)")
        if st.checkbox(debug_label):
            st.code(traceback.format_exc())
        
        try_following_msg = t('try_following', default="Please try the following:")
        st.info(try_following_msg)
        st.markdown("""
        1. **Refresh the page** and try again
        2. **Check your session state** - you may need to restart
        3. **Verify your data files** - ensure all required files exist
        4. **Check the logs** for more detailed error information
        5. **Restart the application** if the problem persists
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🔄 {t('start_over')}"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button(f"🏠 {t('back_to_welcome')}"):
                st.session_state.conversation_step = 'welcome'
                st.rerun()
    
    def run(self):
        """Main application runner"""
        try:
            # Initialize the application
            self.initialize_app()
            
            # Render sidebar
            self.render_sidebar()
            
            # Render progress indicator
            self.render_progress_indicator()
            
            # Render current screen
            self.render_current_screen()
            
        except Exception as e:
            logger.error(f"Critical application error: {e}")
            
            critical_error_msg = t('critical_error', default='Critical Application Error')
            st.error(f"🚨 **{critical_error_msg}**: {str(e)}")
            
            # Show detailed error information for debugging
            debug_label = t('show_debug', default="Show detailed error information (for debugging)")
            if st.checkbox(debug_label):
                st.code(traceback.format_exc())
            
            try_following_msg = t('try_following', default="Please try the following:")
            st.info(try_following_msg)
            st.markdown("""
            1. **Refresh the page** and try again
            2. **Check your .env file** - ensure OPENAI_API_KEY is set
            3. **Verify your data files** - ensure all required files exist
            4. **Check file permissions** - ensure the app can read your files
            5. **Restart the application** if the problem persists
            """)
            
            if st.button(f"🔄 {t('start_over')}"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

def validate_environment():
    """Validate environment and configuration"""
    try:
        # Check if required modules can be imported
        required_modules = [
            'config', 'session_manager', 'database_manager', 
            'ai_assistant', 'audio_manager', 'ui_components', 
            'conversation_flows', 'localization'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError as e:
                missing_modules.append(f"{module}: {str(e)}")
        
        return len(missing_modules) == 0, missing_modules
        
    except Exception as e:
        return False, [f"Environment validation error: {str(e)}"]

def main():
    """Application entry point"""
    try:
        # Validate environment first
        env_valid, env_errors = validate_environment()
        if not env_valid:
            st.error("❌ **Environment Error**")
            st.markdown("### Missing modules or import errors:")
            for error in env_errors:
                st.markdown(f"- {error}")
            st.markdown("### Please check your installation and file structure.")
            return
        
        # Validate configuration
        is_valid, errors = Config.validate_setup()
        
        if not is_valid:
            config_error_msg = t('configuration_error', default='Configuration Error')
            st.error(f"❌ **{config_error_msg}**")
            
            issues_found_msg = t('issues_found', default='Issues found')
            st.markdown(f"### {issues_found_msg}:")
            for error in errors:
                st.markdown(f"- {error}")
            
            quick_setup_msg = t('quick_setup', default='Quick Setup')
            st.markdown(f"""
            ### {quick_setup_msg}:
            1. Create a `.env` file with: `OPENAI_API_KEY=your_key_here`
            2. Create folders: `data/`, `assets/`
            3. Add your Excel file: `student_modules_with_pdfs.xlsx`
            4. Add ethics document: `data/reforming_modernity.pdf`
            """)
            return
        
        # Create and run the application
        app = UniversityChatbot()
        app.run()
        
    except Exception as e:
        startup_error_msg = f"Failed to start application: {e}"
        st.error(startup_error_msg)
        logger.error(f"Startup error: {e}")
        
        # Show detailed error for debugging
        if st.checkbox("Show startup error details"):
            st.code(traceback.format_exc())
        
        retry_msg = t('retry', default='Retry')
        if st.button(f"🔄 {retry_msg}"):
            st.rerun()

if __name__ == '__main__':
    main()