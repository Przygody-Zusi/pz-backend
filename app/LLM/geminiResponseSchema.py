from google.genai import types

# Definicja schematu dla pojedynczego obiektu w tablicy 'contribution_periods'
contribution_period_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        # "period_name": types.Schema(
        #     type=types.Type.STRING, description="Nazwa okresu składkowego."
        # ),
        "start_date": types.Schema(
            type=types.Type.STRING,
            description="Data rozpoczęcia okresu w formacie YYYY",
        ),
        "end_date": types.Schema(
            type=types.Type.STRING,
            description="Data zakończenia okresu w formacie YYYY",
        ),
        "gross_income": types.Schema(
            type=types.Type.NUMBER,
            description="Roczny dochód brutto w tym okresie.",
        ),
        "employment_type": types.Schema(
            type=types.Type.STRING,
            description="Rodzaj zatrudnienia (enum).",
            enum=[
                "employment_contract",
                "self_employed",
                "mandate_contract",
                "maternity_leave",
                "parental_leave",
                "no_employment",
            ],
        ),
    },
    required=["start_date", "end_date", "gross_income", "employment_type"],
)


# Główny schemat odpowiedzi
response_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        # --- Sekcja PROFILE ---
        "profile": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "date_of_birth": types.Schema(
                    type=types.Type.STRING,
                    description="Data urodzenia w formacie YYYY",
                ),
                "gender": types.Schema(
                    type=types.Type.STRING,
                    description="Płeć (enum).",
                    enum=["male", "female"],
                ),
                "employment_start_date": types.Schema(
                    type=types.Type.STRING,
                    description="Data rozpoczęcia pierwszej pracy/zatrudnienia w formacie YYYY",
                ),
                "actual_retirement_age": types.Schema(
                    type=types.Type.INTEGER,
                    description="Aktualny (domyślny) wiek przejścia na emeryturę.",
                ),
                "initial_amount": types.Schema(
                    type=types.Type.NUMBER,
                    description="Wysokość zgromadzonych środków na koncie i na subkoncie w ZUS.",
                ),
            },
            required=[
                "date_of_birth",
                "gender",
                "employment_start_date",
                "actual_retirement_age",
                "initial_amount",
            ],
        ),
        # --- Sekcja RETIREMENT_GOALS ---
        "retirement_goals": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "initial_prompt": types.Schema(
                    type=types.Type.STRING,
                    description="Oryginalna prośba tekstowa od użytkownika dotycząca celów emerytalnych.",
                ),
                "expected_retirement_age": types.Schema(
                    type=types.Type.INTEGER,
                    description="Oczekiwany wiek przejścia na emeryturę.",
                ),
                "expected_retirement_salary": types.Schema(
                    type=types.Type.NUMBER,
                    description="Oczekiwana pensja na emeryturze.",
                ),
                "expected_life_status": types.Schema(
                    type=types.Type.NUMBER,
                    description="Oczekiwana jakość życia na emeryturze, wartość FLOAT w zakresie od 0.0 (żebrak) do 1.0 (milioner).",
                ),
            },
            required=[
                "initial_prompt",
                "expected_retirement_age",
                "expected_life_status",
            ],
        ),
        # --- Sekcja CONTRIBUTION_PERIODS ---
        "contribution_periods": types.Schema(
            type=types.Type.ARRAY,
            description="Lista historycznych okresów składkowych i nieskładkowych.",
            items=contribution_period_schema,
        ),
    },
    required=["profile", "retirement_goals", "contribution_periods"],
)

suggestions_schema = types.Schema(
    type=types.Type.ARRAY,
    description="Sugestie dla kolejnego kroku.",
    items=contribution_period_schema,
)
