from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

# 1. Zmiana importów dla struktury folderów:
# Zakładamy, że moduły są w folderze LLM/
from app.LLM.geminiResponseSchema import response_schema
from app.LLM.geminiCreateInitialProfile import generate_initial_profile
from app.LLM.geminiUpdateProfile import update_user_profile
from app.LLM.geminiSuggestNextStep import suggest_next_contribution_period
from app.LLM.schema_types import UserProfile
from app.LLM.geminiAnalyzeOutputs import analyze_outputs

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

    old_profile: UserProfile = Field(
        ..., description="Istniejący profil JSON, który ma zostać zaktualizowany."
    )
    prompt: str = Field(
        ...,
        description="Prośba użytkownika o modyfikację profilu (np. 'Chcę przejść na emeryturę w wieku 70 lat').",
    )


class SuggestNextStepRequest(BaseModel):
    """Model dla endpointu /suggest"""

    old_profile: UserProfile = Field(
        ...,
        description="Istniejący profil JSON, do którego ma zostać sugerowany następny etap.",
    )


class AnalyzeGoalRequest(BaseModel):
    """Model dla endpointu /analyze"""

    profile: UserProfile = Field(
        ...,
        description="Istniejący profil JSON, który ma zostać analizowany.",
    )
    raw: float = (
        Field(
            ...,
            description="cała odłożona pensja na emeryturze",
        ),
    )
    total_savings_contemporary: float = Field(
        ...,
        description="suma odłożonych składków na emeryturze w termina złotego 2025",
    )
    monthlyRetirement: float = Field(
        ...,
        description="miesięczna pensja na emeryturze",
    )
    yearsToLiveAverage: float = Field()
    replacementRate: float = Field(
        ...,
        description="Stopa zastępowania",
    )
    avgMonthlySalary: float = Field(
        ...,
        description="Srednia miesieczna pensja",
    )


def analyze_goals(request: AnalyzeGoalRequest):
    try:
        if len(request.profile.contribution_periods) == 0:
            last_salary = request.avgMonthlySalary
        else:
            last_salary = request.profile.contribution_periods[-1].gross_income
        total_savings_contemporary = request.total_savings_contemporary
        years_to_live_average = request.yearsToLiveAverage
        retirement_goals = request.profile.retirement_goals
        replacement_rate = request.replacementRate
        monthlyRetirement = request.monthlyRetirement
        return analyze_outputs(
            client,
            MODEL_NAME,
            last_salary,
            total_savings_contemporary,
            years_to_live_average,
            retirement_goals,
            replacement_rate,
            monthlyRetirement,
        )

    except Exception as e:
        print(f"Błąd generowania: {e}")
        # Pamiętaj, että HTTPException z poprawnym statusem to standard FastAPI
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}. Sprawdź logs."
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
        return json.loads(new_profile_json)

    except Exception as e:
        print(f"Błąd generowania: {e}")
        # Pamiętaj, że HTTPException z poprawnym statusem to standard FastAPI
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}. Sprawdź logs."
        )


def generate_profile_based_on_info(request: SuggestNextStepRequest):
    """
    Generuje nowy profil emerytalny w formacie JSON na podstawie bazowych informacji.
    """
    try:
        # Wywołanie funkcji z LLM/geminiCreateInitialProfile.py
        # Używa wbudowanej w tę funkcję konfiguracji wymuszającej JSON Schema
        new_profile_json = generate_initial_profile(
            client, MODEL_NAME, str(request.old_profile)
        )

        # Zwracamy surowy tekst JSON jako odpowiedź
        print(new_profile_json)
        return json.loads(new_profile_json)

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
        return json.loads(updated_profile_json)

    except Exception as e:
        print(f"Błąd aktualizacji: {e}")
        raise HTTPException(
            status_code=500, detail=f"Update failed: {str(e)}. Sprawdź logs."
        )


def generate_suggestions_for_next_step(request: SuggestNextStepRequest):
    """
    Sugeruje kolejne kroki emerytalne na podstawie istniejącego profilu.
    """
    try:
        # Wywołanie funkcji z LLM/geminiSuggestNextStep.py
        # Używa wbudowanej w tę funkcją konfiguracji wymuszającej JSON Schema (T=0.01)
        suggestions = suggest_next_contribution_period(
            client=client,
            model_name=MODEL_NAME,
            old_profile_json=request.old_profile,
        )

        # Zwracamy surowy tekst JSON jako odpowiedź
        return json.loads(suggestions)

    except Exception as e:
        print(f"Błąd sugerowania: {e}")
        raise HTTPException(
            status_code=500, detail=f"Suggestion failed: {str(e)}. Sprawdź logs."
        )


def generate_suggestions_for_next_step_mock(request: SuggestNextStepRequest):
    """
    Sugeruje kolejne kroki emerytalne na podstawie istniejącego profilu.
    """
    try:
        from app.LLM.mock import suggestions

        # Zwracamy surowy tekst JSON jako odpowiedź
        return json.loads(suggestions)

    except Exception as e:
        print(f"Błąd sugerowania: {e}")
        raise HTTPException(
            status_code=500, detail=f"Suggestion failed: {str(e)}. Sprawdź logs."
        )


def generate_profile_mock(request):
    """
    Generuje nowy profil emerytalny w formacie JSON na podstawie opisu użytkownika.
    """
    try:
        # Wywołanie funkcji z LLM/geminiCreateInitialProfile.py
        # Używa wbudowanej w tę funkcję konfiguracji wymuszającej JSON Schema
        from app.LLM.mock import initial_profile

        # Zwracamy surowy tekst JSON jako odpowiedź
        print(initial_profile)
        return json.loads(initial_profile)

    except Exception as e:
        print(f"Błąd generowania: {e}")
        # Pamiętaj, że HTTPException z poprawnym statusem to standard FastAPI
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}. Sprawdź logs."
        )
