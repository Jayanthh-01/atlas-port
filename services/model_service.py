from groq import Groq
import os
from fastapi import HTTPException
from typing import Dict, Any

import json  
groq_client = Groq(api_key=os.getenv("GROQ_API")) 


async def generate_interview_questions(resume_text: str, job_role: str, experience: str, topics: str) -> Dict[str, Any]:
    prompt = f"""
    You are a resume analyzer and interview question generator. Please analyze the following resume and return:
    1. A summary of the candidate's profile
    2. Key skills identified
    3. Experience level assessment
    4. 15 relevant interview questions

    Job Role: {job_role}
    Experience Level: {experience}
    Special Topics: {topics}

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
            model=os.getenv("GROQ_MODEL", "qwen-2.5-coder-32b"),  
            response_format={"type": "json_object"}  
        )
        
        
        return json.loads(chat_completion.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {str(e)}")
