# resumes/utils.py
import os
import re

def parse_resume(file):
    """
    Basic resume parsing function
    """
    try:
        # Get file extension
        ext = os.path.splitext(file.name)[1].lower()

        # Read file content
        text = file.read().decode('utf-8', errors='ignore')

        # Extract basic information
        return {
            'skills': extract_skills(text),
            'experience': extract_experience(text),
            'education': extract_education(text),
            'raw_text': text
        }
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return {}

def extract_skills(text):
    """
    Extract skills from resume text
    """
    # Predefined skill keywords
    skill_keywords = [
        'python', 'django', 'flask', 'javascript', 'react',
        'machine learning', 'data analysis', 'sql', 'git',
        'html', 'css', 'nodejs', 'tensorflow', 'keras'
    ]

    # Case-insensitive skill extraction
    skills = [
        skill for skill in skill_keywords
        if skill.lower() in text.lower()
    ]

    return list(set(skills))

def extract_experience(text):
    """
    Extract work experience details
    """
    # Experience patterns
    experience_patterns = [
        r'(\d+)\s*(?:years?|yrs?)\s*of\s*experience',
        r'worked\s*(?:at|in)\s*(.+?)\s*(?:from|between)\s*(\d{4})\s*(?:to)?\s*(\d{4})?'
    ]

    experiences = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        experiences.extend(matches)

    return experiences

def extract_education(text):
    """
    Extract education information
    """
    education_patterns = [
        r'(?:Bachelor|Master|PhD|Degree)\s*(?:of|in)\s*(.+?)\s*(?:from|at)\s*(.+?)(?:\n|$)',
        r'(?:Graduated|Completed)\s*(.+?)\s*(?:from|at)\s*(.+?)(?:\n|$)'
    ]

    educations = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        educations.extend(matches)

    return educations
