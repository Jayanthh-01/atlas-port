from fastapi import APIRouter, HTTPException, File, UploadFile,Form
from services.parser_service import extract_resume_data, extract_text_from_docx, extract_text_from_pdf
from services.ats_service import ats_metrics
from typing import Dict, Any
ats_router=APIRouter()

@ats_router.post("/ats-details")
async def get_ats_details(file:UploadFile=File(...),job_description:str=Form(...)):
    try:
        if file.filename.endswith(".pdf"):
            text =  extract_text_from_pdf(file.file)
        elif file.filename.endswith(".docx"):
            text =  extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Upload a PDF or DOCX file.")

        
        ats_metric =await  ats_metrics(text,job_description)


        return {"success": True, "data": ats_metric}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")