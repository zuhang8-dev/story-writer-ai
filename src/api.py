from fastapi import FastAPI
from pydantic import BaseModel
from generate import generate_story

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    top_k: int = 3

@app.post("/generate")
def generate(request: GenerateRequest):
    story = generate_story(request.prompt, top_k=request.top_k)
    return {"result": story}