from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from services.parser_service import extract_name, extract_resume_data, extract_text_from_docx, extract_text_from_pdf
from services.model_service import generate_interview_questions
from fastapi.responses import JSONResponse

model_router = APIRouter()

@model_router.post("/generate")
async def upload_resume(
    file: UploadFile = File(...), 
    jobRole: str = Form(...),
    experience: str = Form(...),
    topics: str = Form(None)
):
    try:
        print(f"Received file: {file.filename}")
        print(f"Job Role: {jobRole}, Experience: {experience}, Topics: {topics}")

        file_ext = file.filename.split('.')[-1].lower()
        
        if file_ext == "pdf":
            print("Processing PDF file")
            text = extract_text_from_pdf(file.file)
        elif file_ext == "docx":
            print("Processing DOCX file")
            text = extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Upload a PDF or DOCX file.")
        
        print("Extracted text length:", len(text))

        extracted_data = extract_resume_data(text)
        print("Extracted resume data:", extracted_data)

        # Make sure this is actually an async function
        interview_questions = await generate_interview_questions(extracted_data, jobRole, experience, topics)
        print("Generated questions:", interview_questions)

        return {"success": True, "data": interview_questions}

    except Exception as e:
        import traceback
        traceback.print_exc()  # This will print the full error to the terminal
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
