from google import genai
from google.genai import types
from app.LLM.geminiResponseSchema import response_schema


def generate_initial_profile(client, model_name, prompt) -> str:
    system_instruction = (
        "Jesteś precyzyjnym generatorem profilu płatnika ZUS w formacie JSON. "
        "Twoim jedynym zadaniem jest wygenerowanie kompletnego i realistycznego obiektu JSON, "
        "który ŚCIŚLE przestrzega podanego schematu i jest oparty na prośbie użytkownika. "
        "NIE GENERUJ żadnego dodatkowego tekstu ani wyjaśnień."
        "Wygeneruj kompletny przykładowy JSON. "
        f"Dane powinny odpowiadać opisowi: \nJest rok 2025. {prompt} \n\n"
        "Wypełnij listę 'contribution_periods' 3 elementami contribution_period, opisującymi 3 etapy w życiu tego człowieka. np. Pierwsza Praca, Szczyt kariery, Dojrzała kariera. Każdy z tych bloków wypełnij odpowiednimi szczegółami."
    )
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=response_schema,  # Użyj swojego wcześniej zdefiniowanego schematu
        # Wartość kreatywności może być wyższa (0.7), aby wygenerować bardziej zróżnicowane przykładowe dane
        temperature=0.7,
    )
    response = client.models.generate_content(
        model=model_name, contents=prompt, config=config
    )
    return response.text
