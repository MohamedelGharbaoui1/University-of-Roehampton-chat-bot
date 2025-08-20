# main.py - Fixed version with correct import names

import streamlit as st
import logging
import traceback

# Import our modules - FIXED IMPORT NAMES
from config import Config
from session_manager import SessionManager
from database_manager import DatabaseManager
from ai_assistant import AIAssistant  # Fixed: was AiAssistant
from audio_manager import AudioManager
from ui_components import UIComponents
from conversation_flows import ConversationFlows
from localization import init_language_system

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
    """Main University Chatbot Application"""
    
    def __init__(self):
        self.setup_page_config()
        self.ai_assistant = AIAssistant()  # Fixed: was AiAssistant
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
                'About': f"# {Config.PROJECT_NAME}\nGuided coursework assistant for University of Roehampton students"
            }
        )
    
    def initialize_app(self):
        """Initialize the application"""
        # Initialize session state
        SessionManager.initialize_session_state()
        
        # Initialize language system
        init_language_system()
        
        # Apply CSS styling
        st.markdown(self.ui_components.get_enhanced_css(), unsafe_allow_html=True)
        
        # Load student database if not loaded
        self.load_database()
    
    def load_database(self):
        """Load student database"""
        if not st.session_state.database_loaded:
            with st.spinner("Loading student database..."):
                database, message = DatabaseManager.load_student_database()
                if database:
                    st.session_state.student_database = database
                    st.session_state.database_loaded = True
                    logger.info("Student database loaded successfully")
                else:
                    st.error(f"Failed to load student database: {message}")
                    self.show_setup_error(message)
                    st.stop()
    
    def show_setup_error(self, message: str):
        """Show setup error information"""
        st.error(f"❌ **Setup Error:** {message}")
        
        # Validate configuration and show specific errors
        is_valid, errors = Config.validate_setup()
        if not is_valid:
            st.markdown("### Configuration Issues:")
            for error in errors:
                st.markdown(f"- ❌ {error}")
            
            st.markdown("### Setup Instructions:")
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
                st.error("Unknown conversation step. Please restart.")
                if st.button("🔄 Restart"):
                    SessionManager.reset_conversation()
                    st.rerun()
                    
        except Exception as e:
            logger.error(f"Error rendering screen {step}: {e}")
            self.show_screen_error(e)
    
    def render_ethics_interface(self):
        """Render ethics chat interface"""
        if ETHICS_AVAILABLE:
            render_ethics_chat_interface()
        else:
            st.error("Ethics assistance is not available.")
            st.info("Please ensure 'reforming_modernity.pdf' is in your data folder and ethics_handler.py is properly configured.")
            if st.button("🔙 Back"):
                st.session_state.conversation_step = 'welcome'
                st.rerun()
    
    def render_sidebar(self):
        """Render sidebar with controls and information"""
        database_stats = DatabaseManager.get_database_stats()
        self.ui_components.render_sidebar(database_stats)
    
    def render_progress_indicator(self):
        """Render progress indicator if not on welcome screen"""
        if st.session_state.conversation_step != 'welcome':
            self.ui_components.render_progress_indicator()
            st.markdown("---")
    
    def show_screen_error(self, error: Exception):
        """Show error information for screen rendering issues"""
        st.error(f"🚨 **Screen Error**: {str(error)}")
        
        # Show detailed error information for debugging
        if st.checkbox("Show detailed error information (for debugging)"):
            st.code(traceback.format_exc())
        
        st.info("Please try the following:")
        st.markdown("""
        1. **Refresh the page** and try again
        2. **Check your session state** - you may need to restart
        3. **Verify your data files** - ensure all required files exist
        4. **Check the logs** for more detailed error information
        5. **Restart the application** if the problem persists
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Application"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🏠 Go to Welcome"):
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
            st.error(f"🚨 **Critical Application Error**: {str(e)}")
            
            # Show detailed error information for debugging
            if st.checkbox("Show detailed error information (for debugging)"):
                st.code(traceback.format_exc())
            
            st.info("Please try the following:")
            st.markdown("""
            1. **Refresh the page** and try again
            2. **Check your .env file** - ensure OPENAI_API_KEY is set
            3. **Verify your data files** - ensure all required files exist
            4. **Check file permissions** - ensure the app can read your files
            5. **Restart the application** if the problem persists
            """)
            
            if st.button("🔄 Reset Application"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

def main():
    """Application entry point"""
    try:
        # Validate configuration before starting
        is_valid, errors = Config.validate_setup()
        
        if not is_valid:
            st.error("❌ **Configuration Error**")
            st.markdown("### Issues found:")
            for error in errors:
                st.markdown(f"- {error}")
            
            st.markdown("""
            ### Quick Setup:
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
        st.error(f"Failed to start application: {e}")
        logger.error(f"Startup error: {e}")
        
        if st.button("🔄 Retry"):
            st.rerun()

if __name__ == '__main__':
    main()