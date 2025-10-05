from google import genai
from google.genai import types
import json
from app.LLM.geminiResponseSchema import suggestions_schema


def suggest_next_contribution_period(
    client: genai.Client,
    model_name: str,
    old_profile_json: str,
) -> str:
    """
    Zwraca parę kolejnych etapów w zyciu człowieka.
    """

    # 1. Kontekst systemowy (Rola i zasady)
    system_instruction = (
        "Jesteś precyzyjnym systemem generowania danych JSON. "
        "Twoim jedynym zadaniem jest przeanalizowanie ISTNIEJĄCEGO JSON-a opisującego dotychczasowe życie podatnika ZUS."
        "i podanie 4 propozycji następnego etapu w życiu człowieka poprzez zwrócenie NOWEGO OBIEKTU JSON."
        "Zasady działania: "
        "1. ZAWSZE przestrzegaj podanego schematu. "
        "3. Użyj logiki i kontekstu, aby stworzyć propozycje kolejnego etapu w zyciu człowieka"
    )

    prompt_content = (
        f"ISTNIEJĄCY PROFIL JSON:\n{old_profile_json}\n\n"
        "Zwróc 4 propozycje następnego etapu w zyciu człowieka (contribution_period). Szczególną uwagę zwróć na logikę dat i okresów."
    )

    # 3. Konfiguracja API
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=suggestions_schema,
        temperature=0.9,  # BARDZO wysoka temperatura dla kreatywności
    )

    response = client.models.generate_content(
        model=model_name, contents=prompt_content, config=config
    )

    # Wartość 0.01 minimalizuje 'kreatywność' i maksymalizuje trzymanie się zasad i logiki.
    return response.text
