from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from generate import generate_story

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    top_k: int = 3

@app.post("/generate")
def generate(request: GenerateRequest):
    story = generate_story(request.prompt, top_k=request.top_k)
    return {"result": story}