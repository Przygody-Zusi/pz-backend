initial_profile = """
{"profile":{"date_of_birth":"2000","gender":"male","employment_start_date":"2022","actual_retirement_age":65},"retirement_goals":{"initial_prompt":"Jestem informatykiem lat 24, chcę przejść na emeryturę w wieku 60 lat i cieszyć się przeciętnym życiem.","expected_retirement_age":60,"expected_retirement_salary":2400.0,"expected_life_status":0.5},"contribution_periods":[{"start_date":"2022","end_date":"2027","gross_income":6000.0,"employment_type":"employment_contract"},{"start_date":"2028","end_date":"2050","gross_income":15000.0,"employment_type":"self_employed"},{"start_date":"2051","end_date":"2060","gross_income":18000.0,"employment_type":"employment_contract"}]}
"""

suggestions = """
[{"start_date":"2054","end_date":"2059","gross_income":15000.0,"employment_type":"self_employed"},{"start_date":"2054","end_date":"2059","gross_income":12000.0,"employment_type":"employment_contract"},{"start_date":"2054","end_date":"2057","gross_income":13000.0,"employment_type":"self_employed"},{"start_date":"2054","end_date":"2056","gross_income":8000.0,"employment_type":"employment_contract"}]
"""
