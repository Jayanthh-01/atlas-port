from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Dict, Any
from services.parser_service import extract_name, extract_resume_data, extract_text_from_docx, extract_text_from_pdf
from services.model_service import generate_interview_questions
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, File, UploadFile, Form

model_router=APIRouter()

@model_router.post("/generate")
async def upload_resume(
    file: UploadFile = File(...), 
    jobRole: str = Form(...),
    experience: str = Form(...),
    topics: str = Form(None)
):
    """API endpoint to upload a resume and generate interview questions."""
    try:
       
        if file.filename.endswith(".pdf"):
            text =  extract_text_from_pdf(file.file)
        elif file.filename.endswith(".docx"):
            text =  extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Upload a PDF or DOCX file.")

        
        extracted_data = extract_resume_data(text)

       
        interview_questions = await generate_interview_questions(extracted_data, jobRole, experience, topics)

        return {"success": True, "data": interview_questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
