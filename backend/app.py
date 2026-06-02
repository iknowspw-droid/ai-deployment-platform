import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="AI Chat Backend", version="1.0")

# Conceptual Guard: Ensure the system crashes immediately if the API key is missing
# This follows the "Fail-Fast" cloud principle.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY environment variable is not set!", file=sys.stderr)
    sys.exit(1)

# Initialize the official Google GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Define the structure of the incoming request using Pydantic for data validation
class ChatRequest(BaseModel):
    prompt: str

@app.get("/health")
def health_check():
    """
    Why this matters: Kubernetes needs a health check endpoint (Probe) 
    to verify if the container is alive and running properly.
    """
    return {"status": "healthy", "version": "1.0"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Asynchronous endpoint to forward user prompts to Gemini 2.5 Flash
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
    try:
        # We use gemini-2.5-flash as it is the standard, fast, free-tier model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.prompt,
        )
        return {"response": response.text}
        
    except Exception as e:
        # Standard production practice: Log the actual error to stdout/stderr 
        # for our log pipeline (Fluent-Bit) to scrape later.
        print(f"ERROR calling Gemini API: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")
