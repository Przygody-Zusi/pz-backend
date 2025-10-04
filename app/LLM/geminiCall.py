from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Zmiana importów dla struktury folderów:
# Zakładamy, że moduły są w folderze LLM/
from app.LLM.geminiResponseSchema import response_schema
from app.LLM.geminiCreateInitialProfile import generate_initial_profile
from app.LLM.geminiUpdateProfile import update_user_profile

# --- INICJALIZACJA I KONFIGURACJA KLIENTA ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
client = genai.Client(api_key=GEMINI_API_KEY)


# --- DEFINICJE MODELI DANYCH DLA FASTAPI ---
class GenerateProfileRequest(BaseModel):
    """Model dla endpointu /generate"""

    prompt: str = Field(
        ...,
        description="Opis użytkownika dla stworzenia wstępnego profilu (np. 'Jestem informatykiem, 24 lata...').",
    )


class UpdateProfileRequest(BaseModel):
    """Model dla endpointu /update"""

    old_profile: str = Field(
        ..., description="Istniejący profil JSON, który ma zostać zaktualizowany."
    )
    prompt: str = Field(
        ...,
        description="Prośba użytkownika o modyfikację profilu (np. 'Chcę przejść na emeryturę w wieku 70 lat').",
    )


# --- ENDPOINTY ---


def generate_profile(request: GenerateProfileRequest):
    """
    Generuje nowy profil emerytalny w formacie JSON na podstawie opisu użytkownika.
    """
    try:
        # Wywołanie funkcji z LLM/geminiCreateInitialProfile.py
        # Używa wbudowanej w tę funkcję konfiguracji wymuszającej JSON Schema
        new_profile_json = generate_initial_profile(client, MODEL_NAME, request.prompt)

        # Zwracamy surowy tekst JSON jako odpowiedź
        print(new_profile_json)
        return new_profile_json

    except Exception as e:
        print(f"Błąd generowania: {e}")
        # Pamiętaj, że HTTPException z poprawnym statusem to standard FastAPI
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}. Sprawdź logs."
        )


def update_profile(request: UpdateProfileRequest):
    """
    Aktualizuje istniejący profil JSON na podstawie prośby użytkownika o zmianę.
    """
    try:
        # Wywołanie funkcji z LLM/geminiUpdateProfile.py
        # Używa wbudowanej w tę funkcję konfiguracji wymuszającej JSON Schema (T=0.01)
        updated_profile_json = update_user_profile(
            client=client,
            model_name=MODEL_NAME,
            old_profile_json=request.old_profile,
            user_change_prompt=request.prompt,
        )

        # Zwracamy surowy tekst JSON jako odpowiedź
        return updated_profile_json

    except Exception as e:
        print(f"Błąd aktualizacji: {e}")
        raise HTTPException(
            status_code=500, detail=f"Update failed: {str(e)}. Sprawdź logs."
        )
