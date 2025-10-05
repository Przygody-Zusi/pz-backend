from google import genai
from google.genai import types
from app.LLM.geminiResponseSchema import response_schema

retirement_goals = {
    "mieszkanie dla dwoch osob": 36000,
    "podroze dwa razy w roku": 20000,
    "utrzymanie dla dwoch osob": 30000,
    "utrzymanie małego gospodarstwa i ogrodu": 40000,
    "zeglowanie po bałtyku przez 3 miesiące w roku": 60000,
    "dobre_zycie powyżej średniej": 48000,
}


def c_how_many_more_years(
    last_salary, total_savings_contemporary, goal, years_to_live_average
):
    years = (years_to_live_average * goal - total_savings_contemporary) / (
        last_salary * 12 + goal
    )
    return round(years, 1)


def check_how_many_more_years_for_goals(last_salary, valorized, years_to_live_average):
    how_many_more_years_context = ""
    for goal_name, goal_value in retirement_goals.items():
        how_many_more_years = c_how_many_more_years(
            last_salary, valorized, goal_value, years_to_live_average
        )
        if how_many_more_years < 0:
            how_many_more_years_context += f"cel {goal_name} zostanie osiągnięty w momencie przejścia na emeryturę\n"
        else:
            how_many_more_years_context += f"{goal_name} wymaga dodatkowych {how_many_more_years:.2f} lat pracy po planowanym wieku emerytalnym\n"
    print(how_many_more_years_context)
    return how_many_more_years_context


def analyze_outputs(
    client,
    model_name,
    last_salary,
    total_savings_contemporary,
    years_to_live_average,
    retirement_goals,
    replacement_rate,
    monthlyRetirement,
) -> str:
    system_instruction = (
        "Jesteś Krytykiem"
        "Twoim jedynym zadaniem jest wygenerowanie opisu tego na co stać osobę z podaną emeryturą oraz czy spełniła swoje założenia."
        "NIE GENERUJ żadnego dodatkowego tekstu ani wyjaśnień."
        "Pisz w liczbie drugiej - opis ma być skierowany do opisywanej osoby"
        f"Przeanalizuj które z poniższych celów może interesować odbiorcę bazując na jego cozekiwaniach oraz zawrzyj informacje na temat tego ile jeszcze lat potrzebuje pracować aby osiągnąć dany cel. {check_how_many_more_years_for_goals(last_salary, total_savings_contemporary, years_to_live_average)} \n\n"
        f"Zawrzyj informacje o stopie zastąpowania: {replacement_rate}\n Oraz o miesięcznej otrzymywanej emeryturze: {monthlyRetirement}"
        "Weź pod uwagę cele z poniższego słownika"
    )
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        # Wartość kreatywności może być wyższa (0.7), aby wygenerować bardziej zróżnicowane przykładowe dane
        temperature=0.7,
    )
    response = client.models.generate_content(
        model=model_name, contents=str(retirement_goals), config=config
    )
    return response.text
