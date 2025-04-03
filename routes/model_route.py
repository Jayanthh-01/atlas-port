from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import Dict, Any
from services.parser_service import extract_name, extract_resume_data, extract_text_from_docx, extract_text_from_pdf
from groq import Groq
import os
import json  # Add this import

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API"))  # Make sure the env var matches

model_router = APIRouter()

async def generate_interview_questions(resume_text: str) -> Dict[str, Any]:
    prompt = f"""
    You are a resume analyzer and interview question generator. Please analyze the following resume and return:
    1. A summary of the candidate's profile
    2. Key skills identified
    3. Experience level assessment
    4. 15 relevant interview questions

    Resume:
    {resume_text}

    Return the response in the following JSON format:
    {{
        "candidate_profile": {{
            "experience_level": "entry/mid/senior",
            "key_skills": ["skill1", "skill2"],
            "primary_domain": "main field",
            "years_of_experience": "X years"
        }},
        "interview_questions": [
            {{
                "id": 1,
                "question": "detailed question",
                "expected_answer": "key points to look for",
                "difficulty": "easy/medium/hard",
                "type": "technical/behavioral",
                "skill_tested": "specific skill"
            }}
        ]
    }}
    """
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a resume analyzer and interview question generator."},
                {"role": "user", "content": prompt},
            ],
            model=os.getenv("GROQ_MODEL", "llama3-70b-8192"),  # Updated model name
            response_format={"type": "json_object"}  # Ensure JSON output
        )
        
        # Parse the JSON response
        return json.loads(chat_completion.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {str(e)}")

@model_router.post("/generate")
async def upload_resume(file: UploadFile = File(...)):
    """API endpoint to upload a resume and generate interview questions."""
    try:
        if file.filename.endswith(".pdf"):
            text =  extract_text_from_pdf(file.file)
        elif file.filename.endswith(".docx"):
            text =  extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Upload a PDF or DOCX file.")

        # Extract structured resume data
        extracted_data = extract_resume_data(text)

        # Generate interview questions
        interview_questions = await generate_interview_questions(extracted_data)

        return {"success": True, "data": interview_questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")