# localization.py - Enhanced Language Management System for University Chatbot

import json
from typing import Dict, Any, Optional
from pathlib import Path
import streamlit as st
import logging

logger = logging.getLogger(__name__)

class LanguageManager:
    """Enhanced language management system for University Chatbot"""
    
    def __init__(self):
        self.current_language = 'en'
        self.translations = {}
        self.rtl_languages = {'ar'}  # Right-to-left languages
        self.load_translations()
    
    def load_translations(self):
        """Load all translation dictionaries"""
        self.translations = {
            'en': self._get_english_translations(),
            'ar': self._get_arabic_translations(),
            'fr': self._get_french_translations(),
            'es': self._get_spanish_translations()
        }
        
        # Try to load from JSON files if they exist
        translations_dir = Path("translations")
        if translations_dir.exists():
            for lang_code in self.translations.keys():
                file_path = translations_dir / f"{lang_code}.json"
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            loaded_translations = json.load(f)
                            self.translations[lang_code].update(loaded_translations)
                            logger.info(f"Loaded translations from {lang_code}.json")
                    except Exception as e:
                        logger.error(f"Error loading {lang_code}.json: {e}")
    
    def set_language(self, lang_code: str):
        """Set current language and update session state"""
        if lang_code in self.translations:
            self.current_language = lang_code
            if 'language' not in st.session_state or st.session_state.language != lang_code:
                st.session_state.language = lang_code
                st.rerun()
    
    def get_text(self, key: str, default: str = None, **kwargs) -> str:
        """Get translated text with parameter substitution"""
        # Get translation from current language
        text = self.translations.get(self.current_language, {}).get(key)
        
        # Fallback to default parameter if provided
        if text is None and default is not None:
            text = default
        
        # Fallback to English if translation missing
        if text is None and self.current_language != 'en':
            text = self.translations.get('en', {}).get(key, key)
        
        # Final fallback to key itself
        if text is None:
            text = key
        
        # Parameter substitution
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass  # Ignore formatting errors
        
        return text
    
    def is_rtl(self) -> bool:
        """Check if current language is right-to-left"""
        return self.current_language in self.rtl_languages
    
    def get_language_options(self) -> Dict[str, str]:
        """Get available language options for UI"""
        return {
            'en': '🇺🇸 English',
            'ar': '🇸🇦 العربية',
            'fr': '🇫🇷 Français', 
            'es': '🇪🇸 Español'
        }
    
    def _get_english_translations(self) -> Dict[str, str]:
        """English translations (base language)"""
        return {
            # App Headers
            'app_title': 'University of Roehampton Assistant',
            'app_subtitle': 'Your intelligent academic companion',
            'welcome_message': 'How can I help you today?',
            'powered_by': 'Powered by AI',
            
            # Navigation & Controls
            'language_selector': 'Language',
            'voice_settings': 'Voice Settings',
            'quick_actions': 'Quick Actions',
            'system_status': 'System Status',
            'student_information': 'Student Information',
            'current_session': 'Current Session',
            
            # Authentication
            'enter_student_id': 'Enter Your Student ID',
            'student_id_label': 'Student ID:',
            'student_id_placeholder': 'e.g., A00034131',
            'student_id_help': 'Enter your complete Roehampton University Student ID',
            'enter_access_code': 'Enter Your Access Code',
            'access_code_label': 'Access Code:',
            'access_code_placeholder': 'Enter your unique code',
            'access_code_help': 'Enter the numerical code provided to you',
            'verify_button': 'Verify ✅',
            'back_button': '🔙 Back',
            'next_button': 'Next ➡️',
            
            # Module Selection
            'select_module': 'Select Your Module',
            'module_label': 'Module:',
            'programme_label': 'Programme:',
            'choose_module': 'Choose the module you need assistance with:',
            'documents_available': 'documents available',
            'all_materials': 'All {module} Materials',
            'select_button': 'Select {module}',
            
            # Coursework Types
            'coursework_assistance': 'Coursework Assistance',
            'coursework_help_type': 'What type of coursework help do you need?',
            'assignment_questions': 'Assignment Questions',
            'assignment_questions_desc': 'Help understanding assignment requirements and questions',
            'reading_materials': 'Reading Materials',
            'reading_materials_desc': 'Assistance with course readings and materials',
            'concepts_theory': 'Concepts & Theory',
            'concepts_theory_desc': 'Explanation of key concepts and theories',
            'exam_preparation': 'Exam Preparation',
            'exam_preparation_desc': 'Help preparing for examinations',
            'general_questions': 'General Questions',
            'general_questions_desc': 'Any other questions about the module',
            
            # Chat Interface
            'course_assistant': 'Course Assistant',
            'ethics_advisor': 'Ethics Advisor',
            'you': 'You',
            'loading_materials': 'Loading your module materials...',
            'example_questions': 'Example Questions',
            'chat_placeholder': 'Ask me about your coursework...',
            'ethics_placeholder': 'Ask me about ethics based on the Reforming Modernity document...',
            'analyzing_materials': 'Analyzing your coursework materials...',
            'consulting_ethics': 'Consulting ethics guidance...',
            
            # Audio
            'enable_audio': 'Enable Audio Responses',
            'audio_help': 'Toggle audio responses for accessibility',
            'select_voice': 'Select Voice',
            'voice_help': 'Choose the voice for audio responses',
            'test_voice': 'Test Voice',
            'generating_audio': 'Generating audio...',
            'audio_ready': 'Audio ready!',
            'audio_error': 'Failed to generate audio',
            'audio_disabled': 'Audio responses are disabled',
            
            # Buttons and Actions
            'new_session': 'New Session',
            'clear_chat': 'Clear Chat',
            'change_module': 'Change Module',
            'start_over': 'Start Over',
            'back_to_menu': 'Back to Menu',
            'back_to_welcome': 'Back to Welcome',
            'back_to_modules': 'Back to Modules',
            'back_to_authentication': 'Back to Authentication',
            
            # Error Messages
            'api_key_missing': 'OpenAI API key not configured. Please check your .env file.',
            'no_docs_error': 'No document content available',
            'enter_question': 'Please ask a question about your coursework.',
            'enter_ethics_question': 'Please enter a question.',
            'no_modules_found': 'No modules found for your account. Please contact support.',
            'student_not_found': 'Student ID \'{student_id}\' not found in database',
            'invalid_code': 'Invalid code for student {student_id}',
            'auth_successful': 'Authentication successful',
            'auth_required': 'Student authentication required',
            'student_data_missing': 'Student data not loaded',
            
            # Status Messages
            'database_connected': 'Database Connected',
            'database_not_loaded': 'Database Not Loaded',
            'ai_service_connected': 'AI Service Connected',
            'ai_service_unavailable': 'AI Service Not Available',
            
            # Welcome Screen
            'ethics_document_help': 'Ethics Document Help',
            'ethics_help_desc': 'Get assistance with ethics-related documents and guidelines',
            'coursework_help': 'University Coursework Help',
            'coursework_help_desc': 'Get help with your specific coursework materials',
            
            # Ethics
            'ethics_guidance': 'Ethics Guidance',
            'ethics_document': 'Ethics Document',
            'about_ethics_document': 'About This Ethics Document',
            'ethics_assistant_usage': 'How to Use This Ethics Assistant',
            'ethics_examples': 'You can ask questions like:',
            'ethics_example_1': 'What are the main ethical principles discussed in this document?',
            'ethics_example_2': 'How does this document define ethical behavior?',
            'ethics_example_3': 'What guidance does this provide for [specific situation]?',
            'ethics_example_4': 'Can you summarize the key ethical concepts covered?',
            'ethics_tips': 'Tips:',
            'ethics_tip_1': 'Be specific about what ethical guidance you\'re looking for',
            'ethics_tip_2': 'Ask about concepts, principles, or situations mentioned in the document',
            'ethics_tip_3': 'Request examples or applications of ethical principles',
            
            # Progress and Features
            'step_label': 'Step {current} of {total}',
            'welcome_features': 'Feature Highlights',
            'feature_ethics_title': 'Ethics Guidance',
            'feature_ethics_desc': 'Access comprehensive ethics guidance based on university policies',
            'feature_coursework_title': 'Coursework Support',
            'feature_coursework_desc': 'Get personalized help with your module materials and assignments',
            'feature_secure_title': 'Secure Access',
            'feature_secure_desc': 'Student authentication ensures you only access your own materials',
            'feature_audio_title': 'Audio Support',
            'feature_audio_desc': 'Listen to responses with text-to-speech functionality',
        }
    
    def _get_arabic_translations(self) -> Dict[str, str]:
        """Arabic translations"""
        return {
            # App Headers
            'app_title': 'مساعد جامعة روهامبتون',
            'app_subtitle': 'رفيقك الأكاديمي الذكي',
            'welcome_message': 'كيف يمكنني مساعدتك اليوم؟',
            'powered_by': 'مدعوم بالذكاء الاصطناعي',
            
            # Navigation & Controls
            'language_selector': 'اللغة',
            'voice_settings': 'إعدادات الصوت',
            'quick_actions': 'الإجراءات السريعة',
            'system_status': 'حالة النظام',
            'student_information': 'معلومات الطالب',
            'current_session': 'الجلسة الحالية',
            
            # Authentication
            'enter_student_id': 'أدخل رقم الطالب الجامعي',
            'student_id_label': 'رقم الطالب:',
            'student_id_placeholder': 'مثال: A00034131',
            'student_id_help': 'أدخل رقم الطالب الكامل لجامعة روهامبتون',
            'enter_access_code': 'أدخل رمز الوصول',
            'access_code_label': 'رمز الوصول:',
            'access_code_placeholder': 'أدخل الرمز الفريد الخاص بك',
            'access_code_help': 'أدخل الرمز الرقمي المقدم لك',
            'verify_button': 'تحقق ✅',
            'back_button': '🔙 رجوع',
            'next_button': 'التالي ➡️',
            
            # Module Selection
            'select_module': 'اختر الوحدة الدراسية',
            'module_label': 'الوحدة:',
            'programme_label': 'البرنامج:',
            'choose_module': 'اختر الوحدة الدراسية التي تحتاج المساعدة فيها:',
            'documents_available': 'مستندات متاحة',
            'all_materials': 'جميع مواد {module}',
            'select_button': 'اختر {module}',
            
            # Coursework Types
            'coursework_assistance': 'مساعدة الواجبات الدراسية',
            'coursework_help_type': 'ما نوع المساعدة في الواجبات التي تحتاجها؟',
            'assignment_questions': 'أسئلة الواجبات',
            'assignment_questions_desc': 'مساعدة في فهم متطلبات وأسئلة الواجبات',
            'reading_materials': 'المواد القرائية',
            'reading_materials_desc': 'مساعدة في قراءات ومواد المقرر',
            'concepts_theory': 'المفاهيم والنظريات',
            'concepts_theory_desc': 'شرح المفاهيم والنظريات الأساسية',
            'exam_preparation': 'الاستعداد للامتحانات',
            'exam_preparation_desc': 'مساعدة في الاستعداد للامتحانات',
            'general_questions': 'أسئلة عامة',
            'general_questions_desc': 'أي أسئلة أخرى حول الوحدة الدراسية',
            
            # Chat Interface
            'course_assistant': 'مساعد المقرر',
            'ethics_advisor': 'مستشار الأخلاق',
            'you': 'أنت',
            'loading_materials': 'جارٍ تحميل مواد الوحدة الدراسية...',
            'example_questions': 'أمثلة على الأسئلة',
            'chat_placeholder': 'اسألني عن واجباتك الدراسية...',
            'ethics_placeholder': 'اسألني عن الأخلاق بناءً على وثيقة إصلاح الحداثة...',
            'analyzing_materials': 'جارٍ تحليل مواد واجباتك الدراسية...',
            'consulting_ethics': 'جارٍ استشارة التوجيه الأخلاقي...',
            
            # Audio
            'enable_audio': 'تفعيل الاستجابات الصوتية',
            'audio_help': 'تبديل الاستجابات الصوتية لإمكانية الوصول',
            'select_voice': 'اختر الصوت',
            'voice_help': 'اختر الصوت للاستجابات الصوتية',
            'test_voice': 'اختبار الصوت',
            'generating_audio': 'جارٍ إنشاء الصوت...',
            'audio_ready': 'الصوت جاهز!',
            'audio_error': 'فشل في إنشاء الصوت',
            'audio_disabled': 'الاستجابات الصوتية معطلة',
            
            # Buttons and Actions
            'new_session': 'جلسة جديدة',
            'clear_chat': 'مسح المحادثة',
            'change_module': 'تغيير الوحدة',
            'start_over': 'البدء من جديد',
            'back_to_menu': 'العودة للقائمة',
            'back_to_welcome': 'العودة للترحيب',
            'back_to_modules': 'العودة للوحدات',
            'back_to_authentication': 'العودة للمصادقة',
            
            # Error Messages
            'api_key_missing': 'مفتاح OpenAI API غير مكوّن. يرجى التحقق من ملف .env الخاص بك.',
            'no_docs_error': 'لا يوجد محتوى وثيقة متاح',
            'enter_question': 'يرجى طرح سؤال حول واجباتك الدراسية.',
            'enter_ethics_question': 'يرجى إدخال سؤال.',
            'no_modules_found': 'لم يتم العثور على وحدات لحسابك. يرجى الاتصال بالدعم.',
            'student_not_found': 'رقم الطالب \'{student_id}\' غير موجود في قاعدة البيانات',
            'invalid_code': 'رمز غير صحيح للطالب {student_id}',
            'auth_successful': 'المصادقة ناجحة',
            'auth_required': 'مصادقة الطالب مطلوبة',
            'student_data_missing': 'بيانات الطالب غير محملة',
            
            # Status Messages
            'database_connected': 'قاعدة البيانات متصلة',
            'database_not_loaded': 'قاعدة البيانات غير محملة',
            'ai_service_connected': 'خدمة الذكاء الاصطناعي متصلة',
            'ai_service_unavailable': 'خدمة الذكاء الاصطناعي غير متاحة',
            
            # Welcome Screen
            'ethics_document_help': 'مساعدة الوثائق الأخلاقية',
            'ethics_help_desc': 'احصل على مساعدة في الوثائق والإرشادات المتعلقة بالأخلاق',
            'coursework_help': 'مساعدة الواجبات الجامعية',
            'coursework_help_desc': 'احصل على مساعدة في مواد واجباتك المحددة',
            
            # Ethics
            'ethics_guidance': 'التوجيه الأخلاقي',
            'ethics_document': 'الوثيقة الأخلاقية',
            'about_ethics_document': 'حول هذه الوثيقة الأخلاقية',
            'ethics_assistant_usage': 'كيفية استخدام مساعد الأخلاق هذا',
            'ethics_examples': 'يمكنك طرح أسئلة مثل:',
            'ethics_example_1': 'ما هي المبادئ الأخلاقية الرئيسية المناقشة في هذه الوثيقة؟',
            'ethics_example_2': 'كيف تعرّف هذه الوثيقة السلوك الأخلاقي؟',
            'ethics_example_3': 'ما التوجيه الذي تقدمه هذه الوثيقة لـ [موقف محدد]؟',
            'ethics_example_4': 'هل يمكنك تلخيص المفاهيم الأخلاقية الرئيسية المغطاة؟',
            'ethics_tips': 'نصائح:',
            'ethics_tip_1': 'كن محدداً حول التوجيه الأخلاقي الذي تبحث عنه',
            'ethics_tip_2': 'اسأل عن المفاهيم أو المبادئ أو المواقف المذكورة في الوثيقة',
            'ethics_tip_3': 'اطلب أمثلة أو تطبيقات للمبادئ الأخلاقية',
            
            # Progress and Features
            'step_label': 'الخطوة {current} من {total}',
            'welcome_features': 'أبرز الميزات',
            'feature_ethics_title': 'التوجيه الأخلاقي',
            'feature_ethics_desc': 'الوصول إلى التوجيه الأخلاقي الشامل القائم على سياسات الجامعة',
            'feature_coursework_title': 'دعم الواجبات الدراسية',
            'feature_coursework_desc': 'احصل على مساعدة شخصية في مواد وحداتك وواجباتك',
            'feature_secure_title': 'وصول آمن',
            'feature_secure_desc': 'مصادقة الطالب تضمن وصولك فقط إلى موادك الخاصة',
            'feature_audio_title': 'دعم صوتي',
            'feature_audio_desc': 'استمع إلى الردود باستخدام وظيفة النص إلى كلام',
        }
    
    def _get_french_translations(self) -> Dict[str, str]:
        """French translations"""
        return {
            # App Headers
            'app_title': 'Assistant Université de Roehampton',
            'app_subtitle': 'Votre compagnon académique intelligent',
            'welcome_message': 'Comment puis-je vous aider aujourd\'hui ?',
            'powered_by': 'Alimenté par IA',
            
            # Navigation & Controls
            'language_selector': 'Langue',
            'voice_settings': 'Paramètres Vocaux',
            'quick_actions': 'Actions Rapides',
            'system_status': 'État du Système',
            'student_information': 'Informations Étudiant',
            'current_session': 'Session Actuelle',
            
            # Authentication
            'enter_student_id': 'Entrez Votre ID Étudiant',
            'student_id_label': 'ID Étudiant :',
            'student_id_placeholder': 'ex: A00034131',
            'student_id_help': 'Entrez votre ID complet d\'étudiant de l\'Université de Roehampton',
            'enter_access_code': 'Entrez Votre Code d\'Accès',
            'access_code_label': 'Code d\'Accès :',
            'access_code_placeholder': 'Entrez votre code unique',
            'access_code_help': 'Entrez le code numérique qui vous a été fourni',
            'verify_button': 'Vérifier ✅',
            'back_button': '🔙 Retour',
            'next_button': 'Suivant ➡️',
            
            # Module Selection
            'select_module': 'Sélectionnez Votre Module',
            'module_label': 'Module :',
            'programme_label': 'Programme :',
            'choose_module': 'Choisissez le module pour lequel vous avez besoin d\'aide :',
            'documents_available': 'documents disponibles',
            'all_materials': 'Tous les Matériaux {module}',
            'select_button': 'Sélectionner {module}',
            
            # Coursework Types
            'coursework_assistance': 'Assistance aux Devoirs',
            'coursework_help_type': 'Quel type d\'aide aux devoirs avez-vous besoin ?',
            'assignment_questions': 'Questions d\'Assignation',
            'assignment_questions_desc': 'Aide pour comprendre les exigences et questions d\'assignation',
            'reading_materials': 'Matériaux de Lecture',
            'reading_materials_desc': 'Assistance avec les lectures et matériaux de cours',
            'concepts_theory': 'Concepts et Théorie',
            'concepts_theory_desc': 'Explication des concepts et théories clés',
            'exam_preparation': 'Préparation aux Examens',
            'exam_preparation_desc': 'Aide pour se préparer aux examens',
            'general_questions': 'Questions Générales',
            'general_questions_desc': 'Toute autre question concernant le module',
            
            # Chat Interface
            'course_assistant': 'Assistant de Cours',
            'ethics_advisor': 'Conseiller en Éthique',
            'you': 'Vous',
            'loading_materials': 'Chargement de vos matériaux de module...',
            'example_questions': 'Exemples de Questions',
            'chat_placeholder': 'Posez-moi des questions sur vos devoirs...',
            'ethics_placeholder': 'Posez-moi des questions sur l\'éthique basées sur le document Reforming Modernity...',
            'analyzing_materials': 'Analyse de vos matériaux de devoirs...',
            'consulting_ethics': 'Consultation des conseils éthiques...',
            
            # Audio
            'enable_audio': 'Activer les Réponses Audio',
            'audio_help': 'Basculer les réponses audio pour l\'accessibilité',
            'select_voice': 'Sélectionner la Voix',
            'voice_help': 'Choisissez la voix pour les réponses audio',
            'test_voice': 'Tester la Voix',
            'generating_audio': 'Génération audio...',
            'audio_ready': 'Audio prêt !',
            'audio_error': 'Échec de la génération audio',
            'audio_disabled': 'Réponses audio désactivées',
            
            # Buttons and Actions
            'new_session': 'Nouvelle Session',
            'clear_chat': 'Effacer le Chat',
            'change_module': 'Changer de Module',
            'start_over': 'Recommencer',
            'back_to_menu': 'Retour au Menu',
            'back_to_welcome': 'Retour à l\'Accueil',
            'back_to_modules': 'Retour aux Modules',
            'back_to_authentication': 'Retour à l\'Authentification',
            
            # Error Messages
            'api_key_missing': 'Clé API OpenAI non configurée. Veuillez vérifier votre fichier .env.',
            'no_docs_error': 'Aucun contenu de document disponible',
            'enter_question': 'Veuillez poser une question sur vos devoirs.',
            'enter_ethics_question': 'Veuillez entrer une question.',
            'no_modules_found': 'Aucun module trouvé pour votre compte. Veuillez contacter le support.',
            'student_not_found': 'ID étudiant \'{student_id}\' non trouvé dans la base de données',
            'invalid_code': 'Code invalide pour l\'étudiant {student_id}',
            'auth_successful': 'Authentification réussie',
            'auth_required': 'Authentification étudiant requise',
            'student_data_missing': 'Données étudiant non chargées',
            
            # Status Messages
            'database_connected': 'Base de Données Connectée',
            'database_not_loaded': 'Base de Données Non Chargée',
            'ai_service_connected': 'Service IA Connecté',
            'ai_service_unavailable': 'Service IA Non Disponible',
            
            # Welcome Screen
            'ethics_document_help': 'Aide Documents Éthiques',
            'ethics_help_desc': 'Obtenez de l\'aide avec les documents et directives liés à l\'éthique',
            'coursework_help': 'Aide Devoirs Universitaires',
            'coursework_help_desc': 'Obtenez de l\'aide avec vos matériaux de devoirs spécifiques',
            
            # Ethics
            'ethics_guidance': 'Conseils Éthiques',
            'ethics_document': 'Document Éthique',
            'about_ethics_document': 'À Propos de ce Document Éthique',
            'ethics_assistant_usage': 'Comment Utiliser cet Assistant Éthique',
            'ethics_examples': 'Vous pouvez poser des questions comme :',
            'ethics_example_1': 'Quels sont les principaux principes éthiques discutés dans ce document ?',
            'ethics_example_2': 'Comment ce document définit-il le comportement éthique ?',
            'ethics_example_3': 'Quels conseils cela fournit-il pour [situation spécifique] ?',
            'ethics_example_4': 'Pouvez-vous résumer les concepts éthiques clés couverts ?',
            'ethics_tips': 'Conseils :',
            'ethics_tip_1': 'Soyez spécifique sur les conseils éthiques que vous recherchez',
            'ethics_tip_2': 'Posez des questions sur les concepts, principes ou situations mentionnés dans le document',
            'ethics_tip_3': 'Demandez des exemples ou applications de principes éthiques',
            
            # Progress and Features
            'step_label': 'Étape {current} sur {total}',
            'welcome_features': 'Points Forts des Fonctionnalités',
            'feature_ethics_title': 'Conseils Éthiques',
            'feature_ethics_desc': 'Accédez à des conseils éthiques complets basés sur les politiques universitaires',
            'feature_coursework_title': 'Support aux Devoirs',
            'feature_coursework_desc': 'Obtenez une aide personnalisée avec vos matériaux de module et devoirs',
            'feature_secure_title': 'Accès Sécurisé',
            'feature_secure_desc': 'L\'authentification étudiant garantit que vous n\'accédez qu\'à vos propres matériaux',
            'feature_audio_title': 'Support Audio',
            'feature_audio_desc': 'Écoutez les réponses avec la fonctionnalité de synthèse vocale',
        }
    
    def _get_spanish_translations(self) -> Dict[str, str]:
        """Spanish translations"""
        return {
            # App Headers
            'app_title': 'Asistente Universidad de Roehampton',
            'app_subtitle': 'Tu compañero académico inteligente',
            'welcome_message': '¿Cómo puedo ayudarte hoy?',
            'powered_by': 'Impulsado por IA',
            
            # Navigation & Controls
            'language_selector': 'Idioma',
            'voice_settings': 'Configuración de Voz',
            'quick_actions': 'Acciones Rápidas',
            'system_status': 'Estado del Sistema',
            'student_information': 'Información del Estudiante',
            'current_session': 'Sesión Actual',
            
            # Authentication
            'enter_student_id': 'Ingresa tu ID de Estudiante',
            'student_id_label': 'ID de Estudiante:',
            'student_id_placeholder': 'ej: A00034131',
            'student_id_help': 'Ingresa tu ID completo de estudiante de la Universidad de Roehampton',
            'enter_access_code': 'Ingresa tu Código de Acceso',
            'access_code_label': 'Código de Acceso:',
            'access_code_placeholder': 'Ingresa tu código único',
            'access_code_help': 'Ingresa el código numérico que se te proporcionó',
            'verify_button': 'Verificar ✅',
            'back_button': '🔙 Atrás',
            'next_button': 'Siguiente ➡️',
            
            # Module Selection
            'select_module': 'Selecciona tu Módulo',
            'module_label': 'Módulo:',
            'programme_label': 'Programa:',
            'choose_module': 'Elige el módulo con el que necesitas ayuda:',
            'documents_available': 'documentos disponibles',
            'all_materials': 'Todos los Materiales de {module}',
            'select_button': 'Seleccionar {module}',
            
            # Coursework Types
            'coursework_assistance': 'Asistencia con Tareas',
            'coursework_help_type': '¿Qué tipo de ayuda con tareas necesitas?',
            'assignment_questions': 'Preguntas de Asignación',
            'assignment_questions_desc': 'Ayuda para entender los requisitos y preguntas de asignación',
            'reading_materials': 'Materiales de Lectura',
            'reading_materials_desc': 'Asistencia con lecturas y materiales del curso',
            'concepts_theory': 'Conceptos y Teoría',
            'concepts_theory_desc': 'Explicación de conceptos y teorías clave',
            'exam_preparation': 'Preparación para Exámenes',
            'exam_preparation_desc': 'Ayuda para prepararse para exámenes',
            'general_questions': 'Preguntas Generales',
            'general_questions_desc': 'Cualquier otra pregunta sobre el módulo',
            
            # Chat Interface
            'course_assistant': 'Asistente del Curso',
            'ethics_advisor': 'Asesor de Ética',
            'you': 'Tú',
            'loading_materials': 'Cargando tus materiales del módulo...',
            'example_questions': 'Preguntas de Ejemplo',
            'chat_placeholder': 'Pregúntame sobre tus tareas...',
            'ethics_placeholder': 'Pregúntame sobre ética basado en el documento Reforming Modernity...',
            'analyzing_materials': 'Analizando tus materiales de tareas...',
            'consulting_ethics': 'Consultando orientación ética...',
            
            # Audio
            'enable_audio': 'Habilitar Respuestas de Audio',
            'audio_help': 'Alternar respuestas de audio para accesibilidad',
            'select_voice': 'Seleccionar Voz',
            'voice_help': 'Elige la voz para las respuestas de audio',
            'test_voice': 'Probar Voz',
            'generating_audio': 'Generando audio...',
            'audio_ready': '¡Audio listo!',
            'audio_error': 'Error al generar audio',
            'audio_disabled': 'Respuestas de audio deshabilitadas',
            
            # Buttons and Actions
            'new_session': 'Nueva Sesión',
            'clear_chat': 'Limpiar Chat',
            'change_module': 'Cambiar Módulo',
            'start_over': 'Empezar de Nuevo',
            'back_to_menu': 'Volver al Menú',
            'back_to_welcome': 'Volver al Inicio',
            'back_to_modules': 'Volver a Módulos',
            'back_to_authentication': 'Volver a Autenticación',
            
            # Error Messages
            'api_key_missing': 'Clave API de OpenAI no configurada. Por favor verifica tu archivo .env.',
            'no_docs_error': 'No hay contenido de documento disponible',
            'enter_question': 'Por favor haz una pregunta sobre tus tareas.',
            'enter_ethics_question': 'Por favor ingresa una pregunta.',
            'no_modules_found': 'No se encontraron módulos para tu cuenta. Por favor contacta soporte.',
            'student_not_found': 'ID de estudiante \'{student_id}\' no encontrado en la base de datos',
            'invalid_code': 'Código inválido para el estudiante {student_id}',
            'auth_successful': 'Autenticación exitosa',
            'auth_required': 'Autenticación de estudiante requerida',
            'student_data_missing': 'Datos del estudiante no cargados',
            
            # Status Messages
            'database_connected': 'Base de Datos Conectada',
            'database_not_loaded': 'Base de Datos No Cargada',
            'ai_service_connected': 'Servicio IA Conectado',
            'ai_service_unavailable': 'Servicio IA No Disponible',
            
            # Welcome Screen
            'ethics_document_help': 'Ayuda con Documentos de Ética',
            'ethics_help_desc': 'Obtén asistencia con documentos y directrices relacionados con ética',
            'coursework_help': 'Ayuda con Tareas Universitarias',
            'coursework_help_desc': 'Obtén ayuda con tus materiales de tareas específicos',
            
            # Ethics
            'ethics_guidance': 'Orientación Ética',
            'ethics_document': 'Documento de Ética',
            'about_ethics_document': 'Acerca de este Documento de Ética',
            'ethics_assistant_usage': 'Cómo Usar este Asistente de Ética',
            'ethics_examples': 'Puedes hacer preguntas como:',
            'ethics_example_1': '¿Cuáles son los principales principios éticos discutidos en este documento?',
            'ethics_example_2': '¿Cómo define este documento el comportamiento ético?',
            'ethics_example_3': '¿Qué orientación proporciona esto para [situación específica]?',
            'ethics_example_4': '¿Puedes resumir los conceptos éticos clave cubiertos?',
            'ethics_tips': 'Consejos:',
            'ethics_tip_1': 'Sé específico sobre la orientación ética que buscas',
            'ethics_tip_2': 'Pregunta sobre conceptos, principios o situaciones mencionados en el documento',
            'ethics_tip_3': 'Solicita ejemplos o aplicaciones de principios éticos',
            
            # Progress and Features
            'step_label': 'Paso {current} de {total}',
            'welcome_features': 'Características Destacadas',
            'feature_ethics_title': 'Orientación Ética',
            'feature_ethics_desc': 'Accede a orientación ética integral basada en políticas universitarias',
            'feature_coursework_title': 'Soporte de Tareas',
            'feature_coursework_desc': 'Obtén ayuda personalizada con tus materiales de módulo y tareas',
            'feature_secure_title': 'Acceso Seguro',
            'feature_secure_desc': 'La autenticación de estudiante asegura que solo accedas a tus propios materiales',
            'feature_audio_title': 'Soporte de Audio',
            'feature_audio_desc': 'Escucha respuestas con funcionalidad de texto a voz',
        }


# Create global language manager instance
language_manager = LanguageManager()

def t(key: str, default: str = None, **kwargs) -> str:
    """Convenient translation function"""
    return language_manager.get_text(key, default=default, **kwargs)

def init_language_system():
    """Initialize language system in session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    language_manager.current_language = st.session_state.language

def render_language_selector():
    """Render language selector in sidebar"""
    languages = language_manager.get_language_options()
    
    selected_language = st.selectbox(
        t('language_selector'),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(st.session_state.language),
        key="language_selector"
    )
    
    if selected_language != st.session_state.language:
        language_manager.set_language(selected_language)

def get_rtl_css() -> str:
    """Generate RTL CSS if needed"""
    if language_manager.is_rtl():
        return """
        <style>
            /* RTL Support for Arabic */
            .arabic-text, [lang="ar"] {
                direction: rtl;
                text-align: right;
                font-family: 'Noto Sans Arabic', 'Arial', 'Tahoma', sans-serif !important;
            }
            
            .stSelectbox > div > div {
                direction: rtl;
                text-align: right;
            }
            
            .stTextInput > div > div > input {
                direction: rtl;
                text-align: right;
            }
            
            .stButton > button {
                direction: rtl;
            }
            
            /* Reverse flex direction for RTL */
            .rtl-flex {
                flex-direction: row-reverse;
            }
        </style>
        """
    return ""
