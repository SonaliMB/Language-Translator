from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

# Initialopenai.OpenAIenAI client with your API key
client = OpenAI(api_key=api_key)


# Keep this list in sync with LANGUAGES in index.html
SUPPORTED_LANGUAGES = {
    "Arabic", "Bengali", "Chinese (Simplified)", "Chinese (Traditional)", "Czech",
    "Dutch", "English", "Filipino", "French", "German", "Greek", "Hebrew", "Hindi",
    "Hungarian", "Indonesian", "Italian", "Japanese", "Korean", "Malay", "Marathi",
    "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Spanish", "Swahili",
    "Swedish", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese",
}
AUTO_DETECT = "Auto-detect"

# Create class with pydantic BaseModel
class TranslationRequest(BaseModel):
    input_str: str
    source_language: str = "English"
    target_language: str = "German"

def translate_text(input_str, source_language, target_language):
    if source_language == AUTO_DETECT:
        instruction = (
            f"You are an expert translator who detects the language of the text "
            f"and translates it into {target_language}. Only return the translated text."
        )
    else:
        instruction = (
            f"You are an expert translator who translates text from {source_language} "
            f"to {target_language}. Only return the translated text."
        )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": input_str},
        ],
    )
    return completion.choices[0].message.content


# Initialize FastAPI client
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/languages/")
async def languages():
    return {"source": [AUTO_DETECT, *sorted(SUPPORTED_LANGUAGES)], "target": sorted(SUPPORTED_LANGUAGES)}

@app.post("/translate/")  # This line decorates 'translate' as a POST endpoint
async def translate(request: TranslationRequest):
    if request.source_language != AUTO_DETECT and request.source_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported source language: {request.source_language}")
    if request.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported target language: {request.target_language}")
    if request.source_language == request.target_language:
        raise HTTPException(status_code=400, detail="Source and target languages must be different.")
    try:
        # Call your translation function
        translated_text = translate_text(request.input_str, request.source_language, request.target_language)
        return {"translated_text": translated_text}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))