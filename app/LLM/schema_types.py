from pydantic import BaseModel, Field
from typing import List

# --- Enumy/Typy dla pól o zdefiniowanych wartościach ---
# Używamy typowania str zamiast Enum, aby uprościć walidację w Pydantic
GenderType = str  # Oczekiwane: "male" lub "female"
# Oczekiwane: "employment_contract", "self_employed", itd.
EmploymentType = str


# --- 1. MODELE CZĘŚCIOWE ---


class ProfileData(BaseModel):
    """Część 'profile' - dane podstawowe."""

    date_of_birth: int = Field(..., description="Data urodzenia (YYYY).")
    gender: GenderType = Field(..., description="Płeć: male|female.")
    employment_start_date: int = Field(
        ..., description="Data rozpoczęcia pracy (YYYY)."
    )
    actual_retirement_age: int = Field(
        65, description="Faktyczny, ustawowy wiek emerytalny."
    )
    initial_amount: float = Field(
        0.0, description="Początkowa kwota oszczędności emerytalnych."
    )


class RetirementGoals(BaseModel):
    """Część 'retirement_goals' - cele."""

    initial_prompt: str = Field(
        ..., description="Oryginalna prośba użytkownika użyta do generacji profilu."
    )
    expected_retirement_age: int = Field(
        65, description="Oczekiwany wiek przejścia na emeryturę."
    )
    expected_retirement_salary: float = Field(
        2400, description="Oczekiwana pensja na emeryturze."
    )
    expected_life_status: float = Field(
        ...,
        description="Oczekiwany standard życia na emeryturze (0.0 - najniższy, 1.0 - najwyższy).",
    )


class ContributionPeriod(BaseModel):
    """Element listy 'contribution_periods'."""

    start_date: int = Field(..., description="Rok rozpoczęcia okresu (YYYY).")
    end_date: int = Field(..., description="Rok zakończenia okresu (YYYY).")
    gross_income: float = Field(..., description="Przychód brutto w tym okresie.")
    employment_type: EmploymentType = Field(
        ...,
        description="Typ zatrudnienia: employment_contract|self_employed|mandate_contract|...",
    )


# --- 2. GŁÓWNY MODEL PROFILU ---


class UserProfile(BaseModel):
    """Kompletny, zagnieżdżony schemat profilu użytkownika (cały obiekt JSON)."""

    profile: ProfileData
    retirement_goals: RetirementGoals
    contribution_periods: List[ContributionPeriod]
