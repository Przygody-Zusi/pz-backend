from google import genai
from google.genai import types
import json
from app.LLM.geminiResponseSchema import response_schema


def update_user_profile(
    client: genai.Client,
    model_name: str,
    old_profile_json: str,
    user_change_prompt: str,
) -> str:
    """
    Aktualizuje istniejący profil JSON na podstawie prośby użytkownika
    i wymusza zgodność ze schematem.
    """

    # 1. Kontekst systemowy (Rola i zasady)
    system_instruction = (
        "Jesteś precyzyjnym systemem aktualizacji danych JSON. "
        "Twoim jedynym zadaniem jest przeanalizowanie ISTNIEJĄCEGO JSON-a i PROŚBY UŻYTKOWNIKA "
        "i zwrócenie NOWEGO, ZAKTUALIZOWANEGO OBIEKTU JSON. "
        "Zasady działania: "
        "1. ZAWSZE przestrzegaj podanego schematu. "
        "2. Skopiuj wszystkie pola, które NIE są wymienione w prośbie użytkownika, bez zmian (np. 'person_id', 'date_of_birth'). "
        "3. Użyj logiki i kontekstu, aby zaktualizować tylko te pola, na które ma wpływ prośba użytkownika. "
        "4. NIE GENERUJ żadnego dodatkowego tekstu ani wyjaśnień; zwróć czysty JSON."
    )

    # 2. Prompt użytkownika (Łączy dane wejściowe)
    # Ta konstrukcja jasno oddziela stary stan od żądanej zmiany.
    prompt_content = (
        f"ISTNIEJĄCY PROFIL JSON:\n{old_profile_json}\n\n"
        f"PROŚBA UŻYTKOWNIKA DO AKTUALIZACJI:\n{user_change_prompt}\n\n"
        "Zaktualizuj profil. Szczególną uwagę zwróć na logikę dat i okresów."
    )

    # 3. Konfiguracja API
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=0.01,  # BARDZO niska temperatura dla precyzyjnej i nielosowej aktualizacji danych
    )

    response = client.models.generate_content(
        model=model_name, contents=prompt_content, config=config
    )

    # Wartość 0.01 minimalizuje 'kreatywność' i maksymalizuje trzymanie się zasad i logiki.
    return response.text
