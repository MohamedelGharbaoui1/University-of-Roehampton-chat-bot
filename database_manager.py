# database_manager.py - Student database management

import pandas as pd
import streamlit as st
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages student database operations"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_student_database() -> Tuple[Optional[Dict], str]:
        """Load student database from Excel file with support for multiple PDFs per module"""
        try:
            excel_path = Path(Config.STUDENT_DATA_FILE)
            if not excel_path.exists():
                return None, f"Student database file not found: {Config.STUDENT_DATA_FILE}"
            
            # Read Excel file
            df = pd.read_excel(excel_path)
            
            # Validate required columns
            required_columns = ['Student ID', 'Code', 'Programme', 'Module', 'PDF File']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return None, f"Missing required columns in Excel file: {missing_columns}"
            
            # Create enhanced data structures to handle multiple PDFs per module
            student_database = {
                'students': {},  # student_id -> {code, programme, modules}
                'student_codes': {},  # student_id -> code
                'student_modules': {},  # student_id -> {module_name: [pdf_files]}
                'programme_modules': {}  # programme -> {module_name: [pdf_files]}
            }
            
            for _, row in df.iterrows():
                student_id = str(row['Student ID'])
                code = int(row['Code'])
                programme = row['Programme']
                module = row['Module']
                pdf_file = row['PDF File']
                
                # Initialize student if not exists
                if student_id not in student_database['students']:
                    student_database['students'][student_id] = {
                        'code': code,
                        'programme': programme,
                        'modules': {}
                    }
                    student_database['student_codes'][student_id] = code
                    student_database['student_modules'][student_id] = {}
                
                # Initialize module if not exists for this student
                if module not in student_database['student_modules'][student_id]:
                    student_database['student_modules'][student_id][module] = []
                
                # Create PDF data with enhanced info
                pdf_data = {
                    'pdf_file': pdf_file,
                    'programme': programme,
                    'coursework_type': DatabaseManager._extract_coursework_type(pdf_file),
                    'display_name': DatabaseManager._format_display_name(pdf_file)
                }
                
                student_database['student_modules'][student_id][module].append(pdf_data)
                student_database['students'][student_id]['modules'][module] = student_database['student_modules'][student_id][module]
                
                # Add to programme modules
                if programme not in student_database['programme_modules']:
                    student_database['programme_modules'][programme] = {}
                
                if module not in student_database['programme_modules'][programme]:
                    student_database['programme_modules'][programme][module] = []
                
                # Check if this PDF is already in the programme module list
                if not any(p['pdf_file'] == pdf_file for p in student_database['programme_modules'][programme][module]):
                    student_database['programme_modules'][programme][module].append(pdf_data)
            
            logger.info(f"Loaded {len(student_database['students'])} students from database")
            
            # Log modules with multiple PDFs
            for student_id, modules in student_database['student_modules'].items():
                for module_name, pdfs in modules.items():
                    if len(pdfs) > 1:
                        logger.info(f"Student {student_id}, Module '{module_name}' has {len(pdfs)} PDFs")
            
            return student_database, "Database loaded successfully"
            
        except Exception as e:
            logger.error(f"Error loading student database: {e}")
            return None, f"Error loading database: {str(e)}"
    
    @staticmethod
    def validate_student_credentials(student_id: str, code: str) -> Tuple[bool, Optional[Dict], str]:
        """Validate student ID and code"""
        if not st.session_state.student_database:
            return False, None, "Student database not loaded"
        
        student_id = student_id.strip().upper()
        
        try:
            code = int(code.strip())
        except ValueError:
            return False, None, "Code must be a number"
        
        # Check if student exists
        if student_id not in st.session_state.student_database['students']:
            return False, None, f"Student ID '{student_id}' not found in database"
        
        # Check if code matches
        stored_code = st.session_state.student_database['student_codes'][student_id]
        if code != stored_code:
            return False, None, f"Invalid code for student {student_id}"
        
        # Return student data
        student_data = st.session_state.student_database['students'][student_id]
        return True, student_data, "Authentication successful"
    
    @staticmethod
    def get_student_modules(student_id: str) -> Dict[str, list]:
        """Get modules for a specific student"""
        if not st.session_state.student_database:
            return {}
        
        return st.session_state.student_database['student_modules'].get(student_id, {})
    
    @staticmethod
    def get_database_stats() -> Dict[str, Any]:
        """Get database statistics"""
        if not st.session_state.student_database:
            return {'students': 0, 'programmes': 0, 'modules': 0}
        
        total_students = len(st.session_state.student_database['students'])
        total_programmes = len(st.session_state.student_database['programme_modules'])
        
        # Count total unique modules
        all_modules = set()
        for programme_modules in st.session_state.student_database['programme_modules'].values():
            all_modules.update(programme_modules.keys())
        
        return {
            'students': total_students,
            'programmes': total_programmes,
            'modules': len(all_modules)
        }
    
    @staticmethod
    def _extract_coursework_type(pdf_filename: str) -> str:
        """Extract coursework type from PDF filename"""
        filename_lower = pdf_filename.lower()
        
        # Coursework patterns
        patterns = {
            'coursework1': 'Coursework 1',
            'coursework2': 'Coursework 2',
            'coursework3': 'Coursework 3',
            'assignment1': 'Assignment 1',
            'assignment2': 'Assignment 2',
            'assignment3': 'Assignment 3',
            'exam': 'Exam Material',
            'lecture': 'Lecture Notes',
            'reading': 'Reading Material'
        }
        
        for pattern, coursework_type in patterns.items():
            if pattern in filename_lower:
                return coursework_type
        
        return 'Course Materials'
    
    @staticmethod
    def _format_display_name(pdf_filename: str) -> str:
        """Create user-friendly display name from PDF filename"""
        # Remove extension and replace underscores
        name = Path(pdf_filename).stem.replace('_', ' ')
        
        # Capitalize each word
        name = ' '.join(word.capitalize() for word in name.split())
        
        return name
