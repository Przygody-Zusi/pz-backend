from fastapi import FASTAPI
from pydantic import BaseModel

app = FASTAPI()


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResposne(BaseModel):
    result: str


@app.post("/api/hello", response_model=GenerateResposne)
async def hello(req: GenerateRequest):
    hello_reposnse = f"Echo from backend: {req.prompt}"
    return {"result": hello_reposnse}


@app.get("/health")
async def health():
    return {"status": "ok"}
