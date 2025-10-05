from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from app.LLM.geminiCall import (
    generate_profile,
    update_profile,
    generate_suggestions_for_next_step,
    generate_profile_based_on_info,
    generate_profile_mock,
    generate_suggestions_for_next_step_mock,
    analyze_goals,
    AnalyzeGoalRequest,
    GenerateProfileRequest,
    UpdateProfileRequest,
    SuggestNextStepRequest,
)

app = FastAPI()


# Allow your frontend origin — for dev you can use *
app.add_middleware(
    CORSMiddleware,
    # or ["http://localhost:3000", "http://127.0.0.1:5173"]
    allow_origins=["*"],
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
    return generate_profile(request)


@app.post("/api/LLM/update", response_description="Zaktualizowany profil JSON")
def update_profile_endpoint(request: UpdateProfileRequest):
    return update_profile(request)


@app.post(
    "/api/LLM/suggest",
    response_description="Propozycje kolejnego etapu w zyciu człowieka",
)
def suggest_next_step_endpoint(request: SuggestNextStepRequest):
    return generate_suggestions_for_next_step(request)


@app.post(
    "/api/LLM/generate_based_on_info",
    response_description="Wygenerowany profil JSON",
)
def generate_profile_based_on_info_endpoint(request: SuggestNextStepRequest):
    return generate_profile_based_on_info(request)


@app.post(
    "/api/LLM/analyze_goals",
    response_description="Propozycje kolejnego etapu w zyciu człowieka",
)
def analyze_goals_endpoint(request: AnalyzeGoalRequest):
    return analyze_goals(request)


@app.post(
    "/api/LLM/suggest_mock",
    response_description="Propozycje kolejnego etapu w zyciu człowieka",
)
def suggest_next_step_mock_endpoint(request: SuggestNextStepRequest):
    return generate_suggestions_for_next_step_mock(request)


@app.post(
    "/api/LLM/generate_mock",
    response_description="Wygenerowany profil JSON",
)
def generate_profile_mock_endpoint(request: GenerateProfileRequest):
    return generate_profile_mock(request)


@app.post("/api/generate-profile")
def generate_profile_simple_endpoint(request: GenerateProfileRequest):
    """Simple endpoint for frontend to generate retirement profile"""
    result = generate_profile_mock(request)
    return {"profile": result}


@app.post(
    "/api/LLM/generate_based_on_info_mock",
    response_description="Wygenerowany profil JSON",
)
def generate_profile_mock_endpoint2(request: SuggestNextStepRequest):
    return generate_profile_mock(request)
