# ai_assistant.py - Complete AI response generation and interaction

import logging
from typing import Dict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIAssistant:
    """Handles AI response generation and OpenAI interactions"""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 1500
        self.temperature = 0.3
        self.max_content_length = 15000
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            logger.warning("OpenAI API key not found")
    
    def is_available(self) -> bool:
        """Check if AI assistant is available"""
        return self.client is not None
    
    def generate_coursework_response(self, question: str, document_content: str, module_info: Dict) -> str:
        """Enhanced AI response generation for coursework with support for multiple documents"""
        if not self.client:
            return "🔑 **OpenAI API key not configured. Please check your .env file.**"
        
        if not document_content:
            return f"📄 **No document content available for {module_info.get('module', 'this module')}**"
        
        if not question or not question.strip():
            return "❓ **Please ask a question about your coursework.**"
        
        try:
            # Create enhanced context-aware prompt
            document_info = self._format_document_info(module_info)
            system_prompt = self._create_coursework_system_prompt(document_content, document_info, module_info)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                return "❌ **No response generated from OpenAI**"
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return f"❌ **Error generating response: {str(e)}**"
    
    def generate_ethics_response(self, question: str, document_content: str, student_info: Dict) -> str:
        """Generate AI response for ethics-related questions"""
        if not self.client:
            return "🔑 **OpenAI API key not configured. Please check your .env file.**"
        
        if not document_content or not document_content.strip():
            return "📄 **No ethics document content available**"
        
        if not question or not question.strip():
            return "❓ **No question provided**"
        
        try:
            # Safely get student info with defaults
            student_id = student_info.get('student_id', 'Unknown') if student_info else 'Unknown'
            programme = student_info.get('programme', 'Unknown') if student_info else 'Unknown'
            
            # Truncate content if too long
            truncated_content = document_content[:self.max_content_length]
            
            system_prompt = self._create_ethics_system_prompt(truncated_content, student_id, programme)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            if response and response.choices and len(response.choices) > 0:
                result = response.choices[0].message.content.strip()
                logger.info("Successfully generated ethics response")
                return result
            else:
                return "❌ **No response generated from OpenAI**"
            
        except Exception as e:
            logger.error(f"Error in generate_ethics_response: {str(e)}")
            return f"❌ **Error generating response: {str(e)}**"
    
    def _format_document_info(self, module_info: Dict) -> str:
        """Format document information for display"""
        if not module_info:
            return "No module information available"
            
        if module_info.get('pdf_file') == 'multiple':
            document_info = f"Multiple documents loaded for {module_info.get('module', 'Unknown Module')}:\n"
            all_pdfs = module_info.get('all_pdfs', [])
            for pdf_data in all_pdfs:
                display_name = pdf_data.get('display_name', 'Unknown Document')
                coursework_type = pdf_data.get('coursework_type', 'Unknown Type')
                pdf_file = pdf_data.get('pdf_file', 'Unknown File')
                document_info += f"- {display_name} ({coursework_type}) - File: {pdf_file}\n"
        else:
            display_name = module_info.get('display_name', 'Unknown Document')
            coursework_type = module_info.get('coursework_type', 'Unknown Type')
            pdf_file = module_info.get('pdf_file', 'Unknown File')
            document_info = f"Document: {display_name} ({coursework_type}) - File: {pdf_file}"
        
        return document_info
    
    def _create_coursework_system_prompt(self, document_content: str, document_info: str, module_info: Dict) -> str:
        """Create system prompt for coursework assistance"""
        module_name = module_info.get('module', 'Unknown Module')
        programme = module_info.get('programme', 'Unknown Programme')
        coursework_type = module_info.get('coursework_type', 'Course Materials')
        
        # Truncate content if too long
        truncated_content = document_content[:self.max_content_length]
        
        return f"""You are an expert academic assistant for University of Roehampton students. You are helping with the module: "{module_name}" from the {programme} programme.

{document_info}

DOCUMENT CONTENT:
{truncated_content}

INSTRUCTIONS:
- Answer questions based ONLY on the provided document content
- If multiple documents are provided, clearly indicate which document contains specific information using the format **[Source: Document Name]**
- When referencing content, use the file names shown above for clarity
- Be helpful and educational, explaining concepts clearly
- If information isn't in the document(s), say so clearly
- Provide specific references to sections when possible
- Help with coursework understanding, but don't do the work for the student
- Encourage critical thinking and learning
- Be supportive and encouraging

CONTEXT:
- Module: {module_name}
- Programme: {programme}
- Materials: {coursework_type}

Remember: You are helping a Roehampton University student understand their coursework materials. Always cite your sources when multiple documents are available."""
    
    def _create_ethics_system_prompt(self, document_content: str, student_id: str, programme: str) -> str:
        """Create system prompt for ethics assistance"""
        return f"""You are an expert ethics advisor for University of Roehampton students. You are helping with ethics guidance based on the "Reforming Modernity" document.

STUDENT INFORMATION:
- Student ID: {student_id}
- Programme: {programme}

ETHICS DOCUMENT CONTENT:
{document_content}

INSTRUCTIONS:
- Answer ethics questions based ONLY on the provided "Reforming Modernity" document content
- Provide thoughtful, well-reasoned ethical guidance based on what's actually in the document
- Reference specific sections, concepts, or examples from the document when relevant
- If the document discusses specific ethical frameworks, theories, or principles, use those
- Help students understand and apply the ethical concepts presented in this document
- Encourage critical thinking about ethical issues as presented in the material
- Be supportive and educational in your approach
- If a question cannot be answered from the document content, clearly state this and suggest what topics the document does cover
- Always maintain academic integrity and professional ethics standards

CONTEXT:
- Document: Reforming Modernity (University Ethics Material)
- Purpose: Ethics guidance based on this specific document
- Audience: Roehampton University student

Remember: Base your responses strictly on the actual content of the "Reforming Modernity" document. If the document focuses on specific ethical themes, theories, or applications, emphasize those in your responses."""
    
    def test_connection(self) -> tuple[bool, str]:
        """Test the OpenAI connection"""
        if not self.client:
            return False, "OpenAI client not initialized"
        
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"