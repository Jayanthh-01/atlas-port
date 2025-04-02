from fastapi import HTTPException
from fastapi import  HTTPException
import pdfplumber
import docx
import spacy
import re
from typing import Dict, Any

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("spaCy model 'en_core_web_sm' not found. Run 'python -m spacy download en_core_web_sm'.")


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from an uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting PDF text: {str(e)}")
    return text.strip()

def extract_text_from_docx(docx_file) -> str:
    """Extract text from an uploaded DOCX file."""
    try:
        doc = docx.Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting DOCX text: {str(e)}")

def extract_name(text: str) -> str:
    """Extract the name using Named Entity Recognition (NER) with spaCy."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"

def extract_skills(text: str) -> list:
    """Extract skills based on predefined keywords."""
    skills = [
        "Python", "JavaScript", "React", "Node.js", "Machine Learning", "Django", "Flask", "SQL",
        "Docker", "Kubernetes", "Go", "Rust", "C++", "AWS", "Azure", "TensorFlow", "PyTorch"
    ]
    return [skill for skill in skills if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]

def extract_roles(text: str) -> list:
    """Extract roles based on predefined job titles."""
    roles = [
        "Software Engineer", "Data Scientist", "Backend Developer", "Frontend Developer",
        "DevOps Engineer", "Machine Learning Engineer", "Full Stack Developer", "Product Manager"
    ]
    return [role for role in roles if re.search(rf"\b{role}\b", text, re.IGNORECASE)]

def extract_resume_data(text: str) -> Dict[str, Any]:  # Changed return type
    """Extract structured resume data."""
    return {
        "name": extract_name(text),  # Ensure this is a string
        "skills": extract_skills(text),
        "roles": extract_roles(text)
    }