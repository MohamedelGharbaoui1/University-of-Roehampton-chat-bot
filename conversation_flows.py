# conversation_flows.py - Fixed conversation flow management with proper input fields

import streamlit as st
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConversationFlows:
    """Manages conversation flows and screen rendering"""
    
    def __init__(self, ai_assistant, audio_manager):
        self.ai_assistant = ai_assistant
        self.audio_manager = audio_manager
    
    def render_student_id_input(self):
        """Render student ID input screen - FIXED VERSION"""
        st.markdown("### 🆔 Step 2: Enter Your Student ID")
        st.markdown(f"Please enter your Roehampton University Student ID to continue with **{st.session_state.selected_path}** assistance.")
        
        # Show error if exists
        if st.session_state.get('error_message'):
            st.error(st.session_state.error_message)
            if st.session_state.get('retry_count', 0) > 2:
                st.warning("Having trouble? Please contact IT support or check your credentials.")
        
        # Create a form to ensure proper input handling
        with st.form("student_id_form"):
            student_id = st.text_input(
                "Student ID:",
                placeholder="e.g., A00034131",
                help="Enter your complete Roehampton University Student ID",
                value=""  # Ensure empty initial value
            )
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                back_clicked = st.form_submit_button(
                    "🔙 Back", 
                    type="secondary"
                )
            
            with col2:
                next_clicked = st.form_submit_button(
                    "Next ➡️", 
                    type="primary",
                    disabled=False  # Don't disable in form
                )
        
        # Handle form submissions
        if back_clicked:
            st.session_state.conversation_step = 'welcome'
            st.session_state.error_message = None
            st.session_state.retry_count = 0
            st.rerun()
        
        if next_clicked:
            if student_id and student_id.strip():
                st.session_state.student_id = student_id.strip().upper()
                st.session_state.conversation_step = 'code'
                st.session_state.error_message = None
                st.rerun()
            else:
                st.error("Please enter your Student ID before continuing.")
    
    def render_code_input(self):
        """Render access code input screen - FIXED VERSION"""
        st.markdown("### 🔐 Step 3: Enter Your Access Code")
        st.markdown(f"Student ID: **{st.session_state.student_id}**")
        st.markdown("Please enter your unique access code to verify your identity.")
        
        # Show error if exists
        if st.session_state.get('error_message'):
            st.error(st.session_state.error_message)
        
        # Create a form for proper input handling
        with st.form("access_code_form"):
            code = st.text_input(
                "Access Code:",
                type="password",
                placeholder="Enter your unique code",
                help="Enter the numerical code provided to you",
                value=""  # Ensure empty initial value
            )
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                back_clicked = st.form_submit_button(
                    "🔙 Back", 
                    type="secondary"
                )
            
            with col2:
                verify_clicked = st.form_submit_button(
                    "Verify ✅", 
                    type="primary"
                )
        
        # Handle form submissions
        if back_clicked:
            st.session_state.conversation_step = 'student_id'
            st.session_state.error_message = None
            st.rerun()
        
        if verify_clicked:
            if code and code.strip():
                # Import here to avoid circular imports
                from database_manager import DatabaseManager
                
                # Validate credentials
                is_valid, student_data, message = DatabaseManager.validate_student_credentials(
                    st.session_state.student_id, 
                    code
                )
                
                if is_valid:
                    st.session_state.student_code = code
                    st.session_state.student_data = student_data
                    st.session_state.available_modules = student_data['modules']
                    st.session_state.error_message = None
                    st.session_state.retry_count = 0
                    
                    if st.session_state.selected_path == 'ethics':
                        st.session_state.conversation_step = 'ethics_chat'
                    else:
                        st.session_state.conversation_step = 'module'
                    
                    st.success(f"✅ Welcome, {st.session_state.student_id}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.error_message = message
                    st.session_state.retry_count = st.session_state.get('retry_count', 0) + 1
                    st.rerun()
            else:
                st.error("Please enter your access code before continuing.")
    
    def render_module_selection(self):
        """Render module selection screen"""
        st.markdown("### 📚 Step 4: Select Your Module")
        st.markdown(f"Student ID: **{st.session_state.student_id}**")
        st.markdown(f"Programme: **{st.session_state.student_data['programme']}**")
        st.markdown("Choose the module you need assistance with:")
        
        # Import here to avoid circular imports
        from database_manager import DatabaseManager
        
        # Get modules from the database
        student_modules = DatabaseManager.get_student_modules(st.session_state.student_id)
        
        if not student_modules:
            st.error("❌ No modules found for your account. Please contact support.")
            if st.button("🔙 Back to Authentication", key="no_modules_back"):
                st.session_state.conversation_step = 'code'
                st.rerun()
            return
        
        # Display modules
        for module_name, pdfs in student_modules.items():
            st.markdown(f"**📖 {module_name}**")
            
            if len(pdfs) > 1:
                # Multi-PDF module
                st.markdown(f"*({len(pdfs)} documents available)*")
                
                # Individual PDF buttons
                cols = st.columns(len(pdfs))
                for i, pdf_data in enumerate(pdfs):
                    with cols[i]:
                        if st.button(
                            f"📄 {pdf_data['coursework_type']}", 
                            key=f"{module_name}_pdf_{i}_{pdf_data['pdf_file']}", 
                            help=f"Select {pdf_data['display_name']}",
                            use_container_width=True
                        ):
                            st.session_state.selected_module = {
                                'module': module_name,
                                'programme': pdf_data['programme'],
                                'pdf_file': pdf_data['pdf_file'],
                                'coursework_type': pdf_data['coursework_type'],
                                'display_name': pdf_data['display_name'],
                                'is_multi_pdf': True,
                                'all_pdfs': pdfs
                            }
                            st.session_state.conversation_step = 'coursework'
                            st.rerun()
                
                # Select all button
                if st.button(
                    f"📚 All {module_name} Materials", 
                    key=f"{module_name}_all_pdfs",
                    help=f"Load all {len(pdfs)} documents together",
                    type="secondary",
                    use_container_width=True
                ):
                    st.session_state.selected_module = {
                        'module': module_name,
                        'programme': pdfs[0]['programme'],
                        'pdf_file': 'multiple',
                        'coursework_type': 'All Materials',
                        'display_name': f"All {module_name} Materials",
                        'is_multi_pdf': True,
                        'all_pdfs': pdfs
                    }
                    st.session_state.conversation_step = 'coursework'
                    st.rerun()
            
            else:
                # Single PDF module
                pdf_data = pdfs[0]
                if st.button(
                    f"Select {module_name}", 
                    key=f"{module_name}_single",
                    help=f"Access {pdf_data['pdf_file']}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.selected_module = {
                        'module': module_name,
                        'programme': pdf_data['programme'],
                        'pdf_file': pdf_data['pdf_file'],
                        'coursework_type': pdf_data.get('coursework_type', 'Course Materials'),
                        'display_name': pdf_data.get('display_name', module_name),
                        'is_multi_pdf': False,
                        'all_pdfs': pdfs
                    }
                    st.session_state.conversation_step = 'coursework'
                    st.rerun()
            
            st.markdown("---")
        
        # Back button
        if st.button("🔙 Back to Authentication", 
                    type="secondary",
                    key="module_back_btn",
                    use_container_width=True):
            st.session_state.conversation_step = 'code'
            st.rerun()
    
    def render_coursework_selection(self):
        """Render coursework selection screen"""
        st.markdown("### 📋 Step 5: Coursework Assistance")
        st.markdown(f"Module: **{st.session_state.selected_module['module']}**")
        st.markdown("What type of coursework help do you need?")
        
        # Coursework options
        coursework_options = [
            {
                'title': 'Assignment Questions',
                'description': 'Help understanding assignment requirements and questions',
                'type': 'assignment'
            },
            {
                'title': 'Reading Materials',
                'description': 'Assistance with course readings and materials',
                'type': 'reading'
            },
            {
                'title': 'Concepts & Theory',
                'description': 'Explanation of key concepts and theories',
                'type': 'concepts'
            },
            {
                'title': 'Exam Preparation',
                'description': 'Help preparing for examinations',
                'type': 'exam'
            },
            {
                'title': 'General Questions',
                'description': 'Any other questions about the module',
                'type': 'general'
            }
        ]
        
        for option in coursework_options:
            if st.button(
                f"📝 {option['title']}", 
                help=option['description'],
                use_container_width=True,
                key=f"coursework_{option['type']}"
            ):
                st.session_state.selected_coursework = option
                st.session_state.conversation_step = 'chat'
                st.rerun()
        
        # Back button
        if st.button("🔙 Back to Modules", type="secondary", key="coursework_back"):
            st.session_state.conversation_step = 'module'
            st.rerun()
    
    def render_chat_interface(self):
        """Render the chat interface for coursework"""
        # Import here to avoid circular imports
        from document_processor import DocumentProcessor
        from session_manager import SessionManager
        
        # Load document if not already loaded
        if not st.session_state.get('current_document') and st.session_state.get('selected_module'):
            with st.spinner("Loading your module materials..."):
                content, metadata, message = DocumentProcessor.load_document_for_module(st.session_state.selected_module)
                if content:
                    st.session_state.current_document = {
                        'content': content,
                        'metadata': metadata,
                        'module': st.session_state.selected_module
                    }
                    st.success(message)
                else:
                    st.error(message)
                    return
        
        # Header
        st.markdown(f"### 📚 {st.session_state.selected_module['module']}")
        st.markdown(f"**Coursework Type:** {st.session_state.selected_coursework['title']}")
        st.markdown(f"**Programme:** {st.session_state.student_data['programme']}")
        
        # Example questions
        self._render_example_questions()
        
        # Chat messages
        self._render_chat_messages()
        
        # Chat input
        self._handle_chat_input()
        
        # Control buttons
        self._render_chat_controls()
    
    def _render_example_questions(self):
        """Render example questions based on coursework type"""
        with st.expander("💡 Example Questions", expanded=False):
            coursework_type = st.session_state.selected_coursework['type']
            examples = {
                'assignment': [
                    "What are the key requirements for this assignment?",
                    "How should I structure my report?",
                    "What citation format should I use?",
                    "What are the assessment criteria?"
                ],
                'reading': [
                    "Can you summarize the main concepts in this module?",
                    "What are the key theories I should understand?",
                    "Which readings are most important for the exam?",
                    "How do these concepts relate to practical applications?"
                ],
                'concepts': [
                    "Can you explain [specific concept] in simple terms?",
                    "How does [theory A] relate to [theory B]?",
                    "What are some real-world examples of this concept?",
                    "Why is this concept important in the field?"
                ],
                'exam': [
                    "What topics are likely to be on the exam?",
                    "How should I prepare for this type of assessment?",
                    "Can you create practice questions for me?",
                    "What are the key points I should remember?"
                ],
                'general': [
                    "What are the learning objectives for this module?",
                    "How can I improve my understanding of this subject?",
                    "What additional resources do you recommend?",
                    "How does this module connect to my overall programme?"
                ]
            }
            
            for example in examples.get(coursework_type, examples['general']):
                st.markdown(f"- \"{example}\"")
    
    def _render_chat_messages(self):
        """Render chat messages with audio support"""
        for i, message in enumerate(st.session_state.get('messages', [])):
            message_key = f"msg_{i}_{message.get('timestamp', time.time())}"
            
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background: #e3f2fd; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #2196f3;">
                    <strong>🙋 You:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f1f8e9; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #4caf50;">
                    <strong>🤖 Course Assistant:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Add audio player if audio is enabled
                if st.session_state.get('audio_enabled', True):
                    self._handle_audio_for_message(message, message_key)
    
    def _handle_audio_for_message(self, message: Dict[str, Any], message_key: str):
        """Handle audio generation and display for a message"""
        # Check if we already have audio for this message
        if message_key not in st.session_state.get('audio_responses', {}):
            # Generate audio for this message
            if self.audio_manager and self.audio_manager.is_available():
                with st.spinner('Generating audio...'):
                    audio_bytes = self.audio_manager.generate_audio_response(
                        message["content"], 
                        st.session_state.get('selected_voice', 'alloy')
                    )
                    if audio_bytes:
                        if 'audio_responses' not in st.session_state:
                            st.session_state.audio_responses = {}
                        st.session_state.audio_responses[message_key] = audio_bytes
        
        # Display audio player if we have audio
        if message_key in st.session_state.get('audio_responses', {}):
            audio_html = self.audio_manager.create_audio_player(
                st.session_state.audio_responses[message_key], 
                key=message_key
            )
            st.markdown(audio_html, unsafe_allow_html=True)
    
    def _handle_chat_input(self):
        """Handle chat input and response generation"""
        if prompt := st.chat_input("Ask me about your coursework..."):
            # Initialize messages if not exists
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": time.time()
            })
            
            # Generate AI response
            with st.spinner("Analyzing your coursework materials..."):
                response = self.ai_assistant.generate_coursework_response(
                    prompt,
                    st.session_state.current_document['content'],
                    st.session_state.current_document['module']
                )
            
            # Add AI response
            ai_message = {
                "role": "assistant",
                "content": response,
                "timestamp": time.time()
            }
            st.session_state.messages.append(ai_message)
            
            # Pre-generate audio if enabled
            if st.session_state.get('audio_enabled', True) and response and self.audio_manager and self.audio_manager.is_available():
                message_key = f"msg_{len(st.session_state.messages)-1}_{ai_message['timestamp']}"
                try:
                    with st.spinner('Preparing audio...'):
                        audio_bytes = self.audio_manager.generate_audio_response(
                            response, 
                            st.session_state.get('selected_voice', 'alloy')
                        )
                        if audio_bytes:
                            if 'audio_responses' not in st.session_state:
                                st.session_state.audio_responses = {}
                            st.session_state.audio_responses[message_key] = audio_bytes
                except Exception as e:
                    logger.error(f"Error pre-generating audio: {e}")
            
            st.rerun()
    
    def _render_chat_controls(self):
        """Render chat control buttons"""
        from session_manager import SessionManager
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 New Session", type="secondary", key="new_session_btn"):
                SessionManager.reset_conversation()
                st.rerun()
        
        with col2:
            if st.button("🔙 Change Module", type="secondary", key="change_module_btn"):
                st.session_state.conversation_step = 'module'
                st.session_state.messages = []
                st.session_state.current_document = None
                st.rerun()