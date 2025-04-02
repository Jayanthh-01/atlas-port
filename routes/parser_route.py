from fastapi import APIRouter,HTTPException,FastAPI, File, UploadFile
from typing import Dict, Any
from services.parser_service import extract_name,extract_resume_data,extract_text_from_docx,extract_text_from_pdf
parser_router=APIRouter()
@parser_router.post("/upload")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:  # Changed return type
    """API endpoint to upload a resume and extract structured data."""
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Upload a PDF or DOCX file.")

    extracted_data = extract_resume_data(text)
    return extracted_data