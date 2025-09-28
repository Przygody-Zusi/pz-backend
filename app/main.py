from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
