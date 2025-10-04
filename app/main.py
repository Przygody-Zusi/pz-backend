from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from app.LLM.geminiCall import (
    generate_profile,
    update_profile,
    GenerateProfileRequest,
    UpdateProfileRequest,
)

app = FastAPI()


# Allow your frontend origin — for dev you can use *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000", "http://127.0.0.1:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResposne(BaseModel):
    result: str


@app.post("/api/hello", response_model=GenerateResposne)
async def hello(req: GenerateRequest):
    hello_reposnse = f"Echo from backend: {req.prompt}"
    return {"result": hello_reposnse, "magic_number": 42}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/LLM/generate", response_description="Wygenerowany profil JSON")
def generate_profile_endpoint(request: GenerateProfileRequest):
    generate_profile(request)


@app.post("/api/LLM/update", response_description="Zaktualizowany profil JSON")
def update_profile_endpoint(request: UpdateProfileRequest):
    update_profile(request)
