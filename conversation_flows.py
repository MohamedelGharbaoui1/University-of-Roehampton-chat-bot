# conversation_flows.py - Updated conversation flow management with proper RTL support

import streamlit as st
import time
import logging
from typing import Dict, Any
from localization import t, language_manager

logger = logging.getLogger(__name__)

class ConversationFlows:
    """Manages conversation flows and screen rendering with full RTL translation support"""
    
    def __init__(self, ai_assistant, audio_manager):
        self.ai_assistant = ai_assistant
        self.audio_manager = audio_manager
    
    def render_student_id_input(self):
        """Render student ID input screen with translation support"""
        lang_attr = f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 🆔 Step 2: {t('enter_student_id')}")
        st.markdown(f"{t('student_id_help')} **{st.session_state.selected_path}** assistance.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show error if exists
        if st.session_state.get('error_message'):
            st.error(st.session_state.error_message)
            if st.session_state.get('retry_count', 0) > 2:
                st.warning("Having trouble? Please contact IT support or check your credentials.")
        
        # Create a form to ensure proper input handling
        with st.form("student_id_form"):
            student_id = st.text_input(
                t('student_id_label'),
                placeholder=t('student_id_placeholder'),
                help=t('student_id_help'),
                value=""
            )
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                back_clicked = st.form_submit_button(
                    t('back_button'), 
                    type="secondary"
                )
            
            with col2:
                next_clicked = st.form_submit_button(
                    t('next_button'), 
                    type="primary"
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
                st.error(t('enter_question'))
    
    def render_code_input(self):
        """Render access code input screen with translation support"""
        lang_attr = f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 🔐 Step 3: {t('enter_access_code')}")
        st.markdown(f"{t('student_id_label')} **{st.session_state.student_id}**")
        st.markdown(t('access_code_help'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show error if exists
        if st.session_state.get('error_message'):
            st.error(st.session_state.error_message)
        
        # Create a form for proper input handling
        with st.form("access_code_form"):
            code = st.text_input(
                t('access_code_label'),
                type="password",
                placeholder=t('access_code_placeholder'),
                help=t('access_code_help'),
                value=""
            )
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                back_clicked = st.form_submit_button(
                    t('back_button'), 
                    type="secondary"
                )
            
            with col2:
                verify_clicked = st.form_submit_button(
                    t('verify_button'), 
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
                    
                    st.success(f"✅ {t('auth_successful')}, {st.session_state.student_id}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    # Translate error message if it contains placeholders
                    if 'not found' in message:
                        translated_message = t('student_not_found', student_id=st.session_state.student_id)
                    elif 'Invalid code' in message:
                        translated_message = t('invalid_code', student_id=st.session_state.student_id)
                    else:
                        translated_message = message
                    
                    st.session_state.error_message = translated_message
                    st.session_state.retry_count = st.session_state.get('retry_count', 0) + 1
                    st.rerun()
            else:
                st.error(t('enter_ethics_question'))
    
    def render_module_selection(self):
        """Render module selection screen with translation support"""
        lang_attr = f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 📚 Step 4: {t('select_module')}")
        st.markdown(f"{t('student_id_label')} **{st.session_state.student_id}**")
        st.markdown(f"{t('programme_label')} **{st.session_state.student_data['programme']}**")
        st.markdown(t('choose_module'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Import here to avoid circular imports
        from database_manager import DatabaseManager
        
        # Get modules from the database
        student_modules = DatabaseManager.get_student_modules(st.session_state.student_id)
        
        if not student_modules:
            st.error(f"❌ {t('no_modules_found')}")
            if st.button(t('back_to_authentication'), key="no_modules_back"):
                st.session_state.conversation_step = 'code'
                st.rerun()
            return
        
        # Display modules
        for module_name, pdfs in student_modules.items():
            st.markdown(f"**📖 {module_name}**")
            
            if len(pdfs) > 1:
                # Multi-PDF module
                st.markdown(f"*({len(pdfs)} {t('documents_available')})*")
                
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
                    f"📚 {t('all_materials', module=module_name)}", 
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
                        'display_name': t('all_materials', module=module_name),
                        'is_multi_pdf': True,
                        'all_pdfs': pdfs
                    }
                    st.session_state.conversation_step = 'coursework'
                    st.rerun()
            
            else:
                # Single PDF module
                pdf_data = pdfs[0]
                if st.button(
                    t('select_button', module=module_name), 
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
        if st.button(t('back_to_authentication'), 
                    type="secondary",
                    key="module_back_btn",
                    use_container_width=True):
            st.session_state.conversation_step = 'code'
            st.rerun()
    
    def render_coursework_selection(self):
        """Render coursework selection screen with translation support"""
        lang_attr = f'lang="{language_manager.current_language}"' if language_manager.current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 📋 Step 5: {t('coursework_assistance')}")
        st.markdown(f"{t('module_label')} **{st.session_state.selected_module['module']}**")
        st.markdown(t('coursework_help_type'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Coursework options with translations
        coursework_options = [
            {
                'title': t('assignment_questions'),
                'description': t('assignment_questions_desc'),
                'type': 'assignment'
            },
            {
                'title': t('reading_materials'),
                'description': t('reading_materials_desc'),
                'type': 'reading'
            },
            {
                'title': t('concepts_theory'),
                'description': t('concepts_theory_desc'),
                'type': 'concepts'
            },
            {
                'title': t('exam_preparation'),
                'description': t('exam_preparation_desc'),
                'type': 'exam'
            },
            {
                'title': t('general_questions'),
                'description': t('general_questions_desc'),
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
        if st.button(t('back_to_modules'), type="secondary", key="coursework_back"):
            st.session_state.conversation_step = 'module'
            st.rerun()
    
    def render_chat_interface(self):
        """Render the chat interface for coursework with proper RTL translation support"""
        # Import here to avoid circular imports
        from document_processor import DocumentProcessor
        from session_manager import SessionManager
        
        # Load document if not already loaded
        if not st.session_state.get('current_document') and st.session_state.get('selected_module'):
            with st.spinner(t('loading_materials')):
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
        
        # Header with translations and RTL support
        current_language = getattr(st.session_state, 'language', 'en')
        lang_attr = f'lang="{current_language}"' if current_language != 'en' else ''
        
        st.markdown(f'<div {lang_attr}>', unsafe_allow_html=True)
        st.markdown(f"### 📚 {st.session_state.selected_module['module']}")
        st.markdown(f"**Coursework Type:** {st.session_state.selected_coursework['title']}")
        st.markdown(f"**{t('programme_label')}** {st.session_state.student_data['programme']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example questions
        self._render_example_questions()
        
        # Chat messages with RTL support
        self._render_chat_messages_with_rtl()
        
        # Chat input
        self._handle_chat_input()
        
        # Control buttons
        self._render_chat_controls()
    
    def _render_example_questions(self):
        """Render example questions based on coursework type with translation support"""
        with st.expander(f"💡 {t('example_questions')}", expanded=False):
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
    
    def _render_chat_messages_with_rtl(self):
        """Render chat messages with audio support and proper RTL translation"""
        current_language = getattr(st.session_state, 'language', 'en')
        lang_attr = f'lang="{current_language}"' if current_language != 'en' else ''
        
        for i, message in enumerate(st.session_state.get('messages', [])):
            message_key = f"msg_{i}_{message.get('timestamp', time.time())}"
            
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background: #e3f2fd; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #2196f3;" {lang_attr}>
                    <strong>🙋 {t('you')}:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                assistant_title = t('course_assistant')
                st.markdown(f"""
                <div style="background: #f1f8e9; color: #000; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #4caf50;" {lang_attr}>
                    <strong>🤖 {assistant_title}:</strong><br>{message["content"]}
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
                with st.spinner(t('generating_audio')):
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
        """Handle chat input and response generation with translation support"""
        placeholder_text = t('chat_placeholder')
        
        if prompt := st.chat_input(placeholder_text):
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
            with st.spinner(t('analyzing_materials')):
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
                    with st.spinner(t('generating_audio')):
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
        """Render chat control buttons with translation support"""
        from session_manager import SessionManager
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button(f"🔄 {t('new_session')}", type="secondary", key="new_session_btn"):
                SessionManager.reset_conversation()
                st.rerun()
        
        with col2:
            if st.button(f"🔙 {t('change_module')}", type="secondary", key="change_module_btn"):
                st.session_state.conversation_step = 'module'
                st.session_state.messages = []
                st.session_state.current_document = None
                st.rerun()
