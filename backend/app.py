from fastapi import FastAPI
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from models import GenerateResponseMode, GneneratedResponseModel


app = FastAPI(title="QA Agent Application", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}



@app.post("/generate",response_model=GneneratedResponseModel)
def generate_with_gemini(body :  GenerateResponseMode):
    """Calls the LLM for text generation."""
    if not body.apikey:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="API key is missing")
    
    genai.configure(api_key=body.apikey)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash',system_instruction= "you are a usefull assistant help me for the question is ask from the context i am giving you apart from the context dont give me any other infromation that is strictly probhited no hallution adn just extrat the information form the context i am giving you if u dont have any infromation  in the context dont answer it  ")
        response = model.generate_content(body.prompt)
        return GneneratedResponseModel(response=response.text)
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 