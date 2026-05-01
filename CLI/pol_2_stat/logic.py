import math
import copy


# i should be writing my TO instead of coding this mess

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def economy_policy2stats(policy_state, stat_state) -> dict:
    import math
    gdp = float(stat_state.economy.get('gdp', 0) or 0)
    gdp = max(gdp, 1.0)

    econ = policy_state.economy
    tax = policy_state.taxation
    env = policy_state.environment
    soc = policy_state.social
    pol = policy_state.politics

    budget_share_gdp = _clamp(0.18 + float(econ['public_spending']) / 100.0 * 0.42, 0.15, 0.65)
    budget_balance = float(econ['budget_deficit'])
    deficit_share_gdp = (-budget_balance / 100.0) * budget_share_gdp

    progressivity = float(tax['high']) - float(tax['low'])
    tax_burden = (0.2 * tax['low'] + 0.3 * tax['medium'] + 0.5 * tax['high']) / 100.0

    inflation = 1.0
    inflation += max(deficit_share_gdp, 0.0) * 25.0
    inflation -= max(-deficit_share_gdp, 0.0) * 6.0
    inflation += float(econ['vat']) * 0.03
    inflation += (50.0 - float(econ['trade'])) * 0.05
    inflation += (100.0 - float(env['energy_mix'])) * 0.025
    inflation += (float(econ['labour_regulation']) - 50.0) * 0.02
    inflation = _clamp(inflation, 0.0, 15.0)

    wage_factor = float(econ['minimum_wage']) / 2000.0
    unemployment = (
        3.5
        + (float(econ['labour_regulation']) - 50.0) * 0.07
        + (wage_factor - 1.0) * 3.0
        - (float(econ['public_spending']) - 50.0) * 0.05
        - (float(econ['trade']) - 50.0) * 0.03
        - (float(soc['education_policy']) - 50.0) * 0.04
        + (tax_burden - 0.35) * 7.0
    )
    unemployment = _clamp(unemployment, 0.0, 25.0)

    debt_to_gdp = (
        15.0
        + max(deficit_share_gdp, 0.0) * 280.0
        - max(-deficit_share_gdp, 0.0) * 100.0
        + (float(econ['public_spending']) - 50.0) * 0.40
        + (float(econ['state_ownership']) - 50.0) * 0.25
        - (float(econ['trade']) - 50.0) * 0.20
        - progressivity * 0.10
        - (tax_burden - 0.35) * 50.0
    )
    debt_to_gdp = _clamp(debt_to_gdp, 0.0, 100.0)

    industry_gap = abs(float(econ["industry"]) - 50.0)
    ownership_gap = abs(float(econ["state_ownership"]) - 50.0)
    innovation = (
        30.0
        + (float(soc["education_policy"]) - 50.0) * 0.35
        + (float(econ["trade"]) - 50.0) * 0.25
        + (float(env["carbon_zero"]) - 50.0) * 0.08
        + (float(econ["public_spending"]) - 50.0) * 0.08
        - industry_gap * 0.15
        - ownership_gap * 0.12
        - (float(econ["labour_regulation"]) - 50.0) * 0.12
        - (float(pol["censorship"]) - 50.0) * 0.18
    )
    innovation = _clamp(innovation, 0.0, 100.0)

    pro_business = (
        (100.0 - float(econ["state_ownership"])) * 0.30
        + (100.0 - float(econ["labour_regulation"])) * 0.20
        + (100.0 - float(env["env_regulation"])) * 0.10
        + float(econ["trade"]) * 0.20
        + (100.0 - float(tax["high"])) * 0.20
    )
    pro_business = _clamp(pro_business, 0.0, 100.0)

    # GDP is in "mln", so log10() gives a stable scale across countries.
    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)
    big_business = int(round(_clamp(gdp_scale * (0.5 + pro_business / 100.0), 0.0, 100.0)))

    income_inequality = (
        35.0
        - progressivity * 0.35
        - (float(soc["social_policy"]) - 50.0) * 0.28
        - (float(soc["labour_policy"]) - 50.0) * 0.22
        - (float(soc["education_policy"]) - 50.0) * 0.12
        - (wage_factor - 1.0) * 4.5
        + (float(econ["trade"]) - 50.0) * 0.08
        - (float(econ["state_ownership"]) - 50.0) * 0.15
        + unemployment * 0.45
    )
    income_inequality = _clamp(income_inequality, 0.0, 100.0)

    gdp_score = _clamp(60.0 + (math.log10(gdp) - 5.0) * 15.0, 0.0, 100.0)
    safety_score = _clamp(
        100.0
        - unemployment * 2.0
        - inflation * 1.5
        - max(0.0, income_inequality - 30.0) * 0.5,
        0.0,
        100.0,
    )
    hdi = _clamp(
        0.25 * gdp_score
        + 0.25 * float(soc["healthcare_policy"])
        + 0.25 * float(soc["education_policy"])
        + 0.25 * safety_score,
        0.0,
        100.0,
    )

    stat_state.economy.update(
        {
            "hdi": round(hdi, 2),
            "inflation": round(inflation, 2),
            "unemployment": round(unemployment, 2),
            "debt_to_gdp": round(debt_to_gdp, 2),
            "innovation": round(innovation, 2),
            "big_business": big_business,
            "income_inequality": round(income_inequality, 2),
        }
    )
    return stat_state.economy

def innerworkings_policy2stats(policy_state, stat_state) -> dict:
    import math
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)

    econ = policy_state.economy
    tax = policy_state.taxation
    pol = policy_state.politics
    police = policy_state.police
    military = policy_state.military
    soc = policy_state.social
    env = policy_state.environment

    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    legitimacy = (
        38.0
        + (float(pol["election_fairness"]) - 50.0) * 0.48
        + (float(pol["judicial_independence"]) - 50.0) * 0.38
        + (float(soc["education_policy"]) - 50.0) * 0.13
        + (float(soc["healthcare_policy"]) - 50.0) * 0.11
        + (float(soc["social_policy"]) - 50.0) * 0.09
        - (float(pol["authoritarianism"]) - 50.0) * 0.36
        - (float(pol["censorship"]) - 50.0) * 0.30
        - (float(pol["surveillance"]) - 50.0) * 0.22
        - (float(pol["power_struggle"]) - 50.0) * 0.30
        - (float(pol["ngo_regulation"]) - 50.0) * 0.13
        - abs(float(police["police_style"]) - 55.0) * 0.07
    )
    legitimacy = _clamp(legitimacy, 0.0, 100.0)

    state_capacity = (
        45.0
        + gdp_scale * 1.05
        + (float(econ["public_spending"]) - 50.0) * 0.20
        + (float(police["police_funding"]) - 50.0) * 0.20
        + (float(military["military_budget"]) - 3.0) * 3.7
        + (float(soc["education_policy"]) - 50.0) * 0.16
        + (float(soc["healthcare_policy"]) - 50.0) * 0.09
        - (float(econ["labour_regulation"]) - 50.0) * 0.10
        - (float(env["env_regulation"]) - 50.0) * 0.06
        - abs(float(pol["power_struggle"]) - 50.0) * 0.15
    )
    state_capacity = _clamp(state_capacity, 0.0, 100.0)

    tax_burden = (0.2 * tax["low"] + 0.3 * tax["medium"] + 0.5 * tax["high"]) / 100.0
    corruption = (
        54.0
        - (float(pol["judicial_independence"]) - 50.0) * 0.45
        - (float(pol["election_fairness"]) - 50.0) * 0.32
        - (float(pol["censorship"]) - 50.0) * 0.14
        - (float(pol["surveillance"]) - 50.0) * 0.16
        - (float(pol["ngo_regulation"]) - 50.0) * 0.10
        + (float(pol["power_struggle"]) - 50.0) * 0.28
        + (float(econ["state_ownership"]) - 50.0) * 0.19
        + (tax_burden - 0.35) * 36.0
        - gdp_scale * 0.70
        - (float(soc["education_policy"]) - 50.0) * 0.07
    )
    corruption = _clamp(corruption, 0.0, 100.0)

    military_pos = (
        68.0
        + (float(military["military_budget"]) - 3.0) * 3.0
        + (float(military["conscription"]) - 50.0) * 0.06
        - (float(pol["authoritarianism"]) - 50.0) * 0.22
        - (float(pol["censorship"]) - 50.0) * 0.10
        - (float(pol["power_struggle"]) - 50.0) * 0.22
        + (float(pol["judicial_independence"]) - 50.0) * 0.12
    )
    military_pos = _clamp(military_pos, 0.0, 100.0)

    police_respect = (
        55.0
        - abs(float(police["police_style"]) - 55.0) * 0.45
        - (float(police["prison_policy"]) - 50.0) * 0.25
        - (float(police["death_pen"]) - 50.0) * 0.22
        - abs(float(police["police_funding"]) - 60.0) * 0.25
        + (float(pol["judicial_independence"]) - 50.0) * 0.13
        + (float(pol["election_fairness"]) - 50.0) * 0.07
        - (float(pol["surveillance"]) - 50.0) * 0.10
    )
    police_respect = _clamp(police_respect, 0.0, 100.0)

    rule_of_law = (
        45.0
        + (float(pol["judicial_independence"]) - 50.0) * 0.52
        + (float(pol["election_fairness"]) - 50.0) * 0.28
        - abs(float(police["police_funding"]) - 60.0) * 0.32
        - (float(pol["authoritarianism"]) - 50.0) * 0.32
        - (float(pol["censorship"]) - 50.0) * 0.22
        - (float(pol["surveillance"]) - 50.0) * 0.18
        - (float(pol["power_struggle"]) - 50.0) * 0.20
        - abs(float(police["police_style"]) - 55.0) * 0.15
        - (float(police["death_pen"]) - 50.0) * 0.12
    )
    rule_of_law = _clamp(rule_of_law, 0.0, 100.0)

    bureaucracy = (
        30.0
        + (float(econ["public_spending"]) - 50.0) * 0.32
        + (float(econ["state_ownership"]) - 50.0) * 0.28
        + (float(econ["labour_regulation"]) - 50.0) * 0.26
        + (float(env["env_regulation"]) - 50.0) * 0.16
        + (tax_burden - 0.35) * 45.0
        - gdp_scale * 0.70
        - (float(pol["power_struggle"]) - 50.0) * 0.18
    )
    bureaucracy = _clamp(bureaucracy, 0.0, 100.0)

    stat_state.inner_workings.update(
        {
            "legitimacy": round(legitimacy, 2),
            "state_capacity": round(state_capacity, 2),
            "corruption": round(corruption, 2),
            "military_pos": round(military_pos, 2),
            "police_respect": round(police_respect, 2),
            "rule_of_law": round(rule_of_law, 2),
            "bureaucracy": round(bureaucracy, 2),
        }
    )
    return stat_state.inner_workings

def humanrights_policy2stats(policy_state, stat_state) -> dict:
    import math
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)

    pol = policy_state.politics
    police = policy_state.police
    cult = policy_state.culture
    soc = policy_state.social

    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    freedom_of_speech = (
        35.0
        + (100.0 - float(pol["censorship"])) * 0.40
        + (100.0 - float(pol["authoritarianism"])) * 0.25
        + (100.0 - float(pol["internet_regulation"])) * 0.25
        + (100.0 - float(pol["surveillance"])) * 0.15
        + (50.0 - float(pol["media_ownership"])) * 0.12
    )
    freedom_of_speech = _clamp(freedom_of_speech, 0.0, 100.0)

    freedom_of_press = (
        30.0
        + (100.0 - float(pol["censorship"])) * 0.35
        + (100.0 - float(pol["authoritarianism"])) * 0.22
        + (100.0 - float(pol["internet_regulation"])) * 0.18
        + (100.0 - float(pol["surveillance"])) * 0.12
        + (float(pol["judicial_independence"]) - 50.0) * 0.15
        + (50.0 - float(pol["media_ownership"])) * 0.20
    )
    freedom_of_press = _clamp(freedom_of_press, 0.0, 100.0)

    freedom_of_assembly = (
        30.0
        + (100.0 - float(pol["authoritarianism"])) * 0.30
        + (100.0 - float(pol["surveillance"])) * 0.22
        + (100.0 - float(pol["ngo_regulation"])) * 0.25
        + (50.0 - float(police["police_style"])) * 0.25
        + (float(pol["election_fairness"]) - 50.0) * 0.15
    )
    freedom_of_assembly = _clamp(freedom_of_assembly, 0.0, 100.0)

    freedom_of_religion = (
        55.0
        + (100.0 - float(cult["religion_influence"])) * 0.28
        + (float(cult["minority_autonomy"]) - 50.0) * 0.20
        + (50.0 - float(cult["nationalism"])) * 0.12
        + (50.0 - float(cult["nation_ident"])) * 0.10
        + (100.0 - float(pol["authoritarianism"])) * 0.10
    )
    freedom_of_religion = _clamp(freedom_of_religion, 0.0, 100.0)

    political_rights = (
        30.0
        + (float(pol["election_fairness"]) - 50.0) * 0.40
        + (float(pol["judicial_independence"]) - 50.0) * 0.22
        + (100.0 - float(pol["authoritarianism"])) * 0.22
        + (100.0 - float(pol["censorship"])) * 0.10
        - abs(float(pol["power_struggle"]) - 50.0) * 0.10
    )
    political_rights = _clamp(political_rights, 0.0, 100.0)

    minority_rights = (
        45.0
        + (float(cult["minority_autonomy"]) - 50.0) * 0.40
        + (50.0 - float(cult["nationalism"])) * 0.18
        + (50.0 - float(cult["nation_ident"])) * 0.14
        + (float(soc["migration_policy"]) - 50.0) * 0.12
        + (100.0 - float(pol["authoritarianism"])) * 0.10
    )
    minority_rights = _clamp(minority_rights, 0.0, 100.0)

    due_process = (
        40.0
        + (float(pol["judicial_independence"]) - 50.0) * 0.45
        + (100.0 - float(pol["authoritarianism"])) * 0.10
        + (50.0 - float(police["police_style"])) * 0.18
        + (50.0 - float(police["prison_policy"])) * 0.12
        + (50.0 - float(police["death_pen"])) * 0.08
        + gdp_scale * 0.35
    )
    due_process = _clamp(due_process, 0.0, 100.0)

    freedom_to_privacy = (
        25.0
        + (100.0 - float(pol["surveillance"])) * 0.50
        + (100.0 - float(pol["authoritarianism"])) * 0.20
        + (100.0 - float(pol["internet_regulation"])) * 0.25
        + (50.0 - float(pol["censorship"])) * 0.10
        + (50.0 - float(police["police_style"])) * 0.15
    )
    freedom_to_privacy = _clamp(freedom_to_privacy, 0.0, 100.0)

    stat_state.human_rights.update(
        {
            "freedom_of_speech": round(freedom_of_speech, 2),
            "freedom_of_press": round(freedom_of_press, 2),
            "freedom_of_assembly": round(freedom_of_assembly, 2),
            "freedom_of_religion": round(freedom_of_religion, 2),
            "political_rights": round(political_rights, 2),
            "minority_rights": round(minority_rights, 2),
            "due_process": round(due_process, 2),
            "freedom_to_privacy": round(freedom_to_privacy, 2),
        }
    )
    return stat_state.human_rights

def security_policy2stats(policy_state, stat_state) -> dict:
    import math
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)
    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    eco = policy_state.economy
    pol = policy_state.politics
    police = policy_state.police
    mil = policy_state.military
    soc = policy_state.social
    cul = policy_state.culture

    crime_rate = (
        15.0
        + (float(pol['surveillance']) - 50.0) * 0.35
        + (100.0 - float(police['police_funding']) - 50.0) * 0.32
        + (float(soc['social_policy']) - 60.0) * 0.28
        + (float(soc['housing_policy']) - 60.0) * 0.22
        - (100.0 - police['police_style'] - 50.0) * 0.18
        - (100.0 - police['prison_policy'] - 50.0) * 0.18
        + gdp_scale * 0.12

    )
    crime_rate = _clamp(crime_rate, 0.0, 100.0)

    organised_crime = (
        18.0
        - float(pol['surveillance']) * 0.25
        + (100.0 - float(police['police_funding']) - 50.0) * 0.45
        + (float(soc['social_policy']) - 60.0) * 0.28
        + (float(soc['housing_policy']) - 60.0) * 0.32
        + (100.0 - police['police_style'] - 50.0) * 0.20
        + (100.0 - police['prison_policy'] - 50.0) * 0.20
        + gdp_scale * 0.60
        + (100.0 - float(eco['industry']) - 50.0) * 0.28
    )
    organised_crime = _clamp(organised_crime, 1.0, 100.0)
 
    border_control = (
        50.0
        + float(pol['authoritarianism']) * 0.20
        + float(police['police_funding']) * 0.30
        + (float(mil['military_budget']) - 2.5) * 20.00
        + (float(cul['nationalism']) - 60) * 0.20
        - (float(cul['minority_autonomy']) - 40.0) * 0.25
    )
    border_control = _clamp(border_control, 0.0, 100.0)

    internal_security = (
        + float(pol['surveillance']) * 0.30
        + (float(police['police_funding']) - 50.0) * 0.30
        + float(pol['internet_regulation']) * 0.35
        + float(police['police_funding']) * 0.35
        + (float(mil["military_budget"]) - 2.0) * 20.00
        + gdp_scale * 0.08
    )
    internal_security = _clamp(internal_security, 0.0, 100.0)
    
    cybersec = ( 
        50.0
        + float(eco['state_ownership']) * 0.15
        + (100.0 - float(pol['censorship']) - 40.0) * 0.20
        + float(pol['surveillance']) * 0.25
        + (float(pol['internet_regulation']) - 40.0) * 0.30
        + (float(police['police_funding']) - 30.0) * 0.40
        - gdp_scale * 0.40
    )
    cybersec = _clamp(cybersec, 1.0, 100.0)

    military_readiness = (
        20.0
        + float(pol['authoritarianism']) * 0.15
        + (float(mil["military_budget"]) - 2.0) * 30.00
        + (float(mil['conscription']) - 40.0) * 0.20
        + (float(mil['alliance_status']) - 60.0) * 0.25
        + gdp_scale * 0.10
    )
    military_readiness = _clamp(military_readiness, 0.0, 100.0)

    stat_state.security.update(
        {
            "crime_rate": round(crime_rate, 2),
            "organised_crime": round(organised_crime, 2),
            "border_control": round(border_control, 2),
            "internal_security": round(internal_security, 2),
            "cybersec": round(cybersec, 2),
            "military_readiness": round(military_readiness, 2),
        }
    )
    return stat_state.security

def democraphics_policy2stats(policy_state, stat_state):
    import math
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)
    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    eco = policy_state.economy
    pol = policy_state.politics
    soc = policy_state.social

    age_structure = (
        20.0
        - (float(soc['labour_policy']) - 50.0) * 0.28
        - (float(soc['migration_policy']) - 50.0) * 0.32
        + gdp_scale * 0.12
        + (float(soc['education_policy']) - 50.0) * 0.20
        + (float(soc['healthcare_policy']) - 50.0) * 0.15
    )
    age_structure = _clamp(age_structure, 0.0, 100.0)

    population_growth = (
        + (float(soc['social_policy']) - 40.0) * 0.30
        + (float(soc['labour_policy']) - 60.0) * 0.15
        + (float(soc['migration_policy']) - 50.0) * 0.25
        - gdp_scale * 0.05
        - (float(eco['minimum_wage']) - 2000.0) * 0.0002
        + (float(eco['labour_regulation']) - 50.0) * 0.10
    )
    population_growth = _clamp(population_growth, -5.0, 5.0)

    urbanization = (
        50.0
        + float(soc['education_policy']) * 0.30
        - (float(soc['housing_policy']) - 50.0) * 0.25
        + float(eco['industry']) * 0.20
        + gdp_scale * 0.10
        - float(soc['migration_policy']) * 0.15
    )
    urbanization = _clamp(urbanization, 0.0, 100.0)

    education_lvl = (
        30.0
        + float(soc['education_policy']) * 0.60
        + (float(eco['public_spending']) - 50.0) * 0.25
        + gdp_scale * 0.18
        - (float(eco['state_ownership']) - 50.0) * 0.25
        - (float(eco['labour_regulation']) - 50.0) * 0.25
    )
    education_lvl = _clamp(education_lvl, 0.0, 100.0)

    avg_age = (
        35.0
        - float(soc['migration_policy']) * 0.15
        + (30.0 - float(soc['labour_policy'])) * 0.10
        + (float(soc['healthcare_policy']) - 60.0) * 0.20
        + (float(soc['education_policy']) - 60.0) * 0.15
        + gdp_scale * 0.25
    )
    avg_age = _clamp(avg_age, 0.0, 100.0)

    stat_state.demographics.update(
        {
            "age_structure": round(age_structure, 2),
            "population_growth": round(population_growth, 2),
            "urbanization": round(urbanization, 2),
            "education_lvl": round(education_lvl, 2),
            "avg_age": round(avg_age, 2),
        }
    )
    return stat_state.demographics

def people_policy2stats(policy_state, stat_state):
    import math
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)
    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    eco = policy_state.economy
    pol = policy_state.politics
    police = policy_state.police
    mil = policy_state.military
    cul = policy_state.culture
    env = policy_state.environment
    soc = policy_state.social

    migration_rate = (
        + gdp_scale * 0.20
        + (float(soc['migration_policy']) - 60.0) * 0.20
        + (float(pol['censorship']) - 60.0) * 0.15
        + (float(pol['judicial_independence']) - 50.0) * 0.15
        + float(soc['social_policy']) * 0.20
        + float(soc['education_policy']) * 0.10
        - (float(pol['authoritarianism']) - 40.0) * 0.20
        - (float(cul['nationalism']) - 50.0) * 0.30
        + (float(cul['minority_autonomy']) - 50.0) * 0.30
    )
    migration_rate = _clamp(migration_rate, 1.0, 100.0)

    war_fatigue = (
        20.0
        - gdp_scale * 0.20
        + (float(mil['military_budget']) - 3.0) * 18.00
        + (float(mil['conscription']) - 50.0) * 0.28
        + (float(pol['authoritarianism']) - 40.0) * 0.22
        + (float(pol['censorship']) - 60.0) * 0.28
        + (float(mil['force_purpose']) - 70.0) * 0.22
        + (float(mil['intervention']) - 60.0) * 0.22
        - (float(mil['sanctions_policy']) - 50.0) * 0.20
    )
    war_fatigue = _clamp(war_fatigue, 0.0, 100.0)

    polarisation = (
        35.0
        + (float(pol['authoritarianism']) - 30.0) * 0.35
        + (float(pol['censorship']) - 20.0) * 0.30
        + (float(pol['power_struggle']) - 50.0) * 0.24
        + (float(soc['social_policy']) - 50.0) * 0.17
        + (float(cul['nationalism']) - 70.0) * 0.25
        - (float(soc['education_policy']) - 80.0) * 0.18
        - gdp_scale * 0.12
    )
    polarisation = _clamp(polarisation, 0.0, 100.0)
    
    terrorism = (
        20.0
        - (float(eco['trade']) - 60.0) * 0.25
        + (float(pol['authoritarianism']) - 30.0) * 0.40
        + (float(pol['censorship']) - 30.0) * 0.22
        + (100.0 - float(pol['election_fairness']) - 30.0) * 0.22
        - (float(pol['internet_regulation']) - 30.0) * 0.20
        - (float(cul['minority_autonomy']) - 40.0) * 0.28
        + (float(cul['nationalism']) - 40.0) * 0.28
        + gdp_scale * 0.35
    )
    terrorism = _clamp(terrorism, 1.0, 100.0)

    civil_unrest = (
        10.0
        + (float(pol['authoritarianism']) - 30.0) * 0.24
        + (float(pol['censorship']) - 30.0) * 0.20
        + (100.0 - float(pol['election_fairness']) - 30.0) * 0.20
        + (float(pol['internet_regulation']) - 50.0) * 0.22
        + (float(pol['ngo_regulation']) - 40.0) * 0.25
        + (float(police['police_style']) - 40.0) * 0.24
        - (float(cul['minority_autonomy']) - 40.0) * 0.22
        + (float(cul['nationalism']) - 30.0) * 0.28
        - (float(soc['social_policy']) - 50.0) * 0.12
        - (float(soc['pension_policy']) - 50.0) * 0.08
        - (float(soc['housing_policy']) - 50.0) * 0.12
        - (float(soc['healthcare_policy']) - 50.0) * 0.12
        - (float(soc['unemployment_policy']) - 50.0) * 0.06
        + (float(soc['migration_policy']) - 30.0) * 0.22
    )
    civil_unrest = _clamp(civil_unrest, 0.0, 100.0)

    social_cohesion = (
        30.0
        + float(cul['religion_influence']) * 0.25
        + (float(cul["nationalism"]) - 40.0) * 0.20
        - (100.0 - float(cul["nation_ident"]) - 60.0) * 0.20
        - float(soc['migration_policy']) * 0.22
        + float(soc['social_policy']) * 0.28
        + float(soc['education_policy']) * 0.20
    )
    social_cohesion = _clamp(social_cohesion, 1.0, 100.0)

    revolutionary_sentiments = (
        12.0
        + (float(pol['authoritarianism']) - 30.0) * 0.32
        + (float(pol['censorship']) - 20.0) * 0.28
        + (float(pol['power_struggle']) - 50.0) * 0.28
        - (float(soc['social_policy']) - 50.0) * 0.28
        + (float(cul['nationalism']) - 70.0) * 0.28
        - (float(soc['education_policy']) - 80.0) * 0.32
        - gdp_scale * 0.15
    )
    revolutionary_sentiments = _clamp(revolutionary_sentiments, 0.0, 100.0)

    stat_state.people.update(
        {
            "migration_rate": round(migration_rate, 2),
            "war_fatigue": round(war_fatigue, 2),
            "polarisation": round(polarisation, 2),
            "terrorism": round(terrorism, 2),
            "civil_unrest": round(civil_unrest, 2),
            "social_cohesion": round(social_cohesion, 2),
            "revolutionary_sentiments": round(revolutionary_sentiments, 2),
        }
    )
    return stat_state.people

def do_all(policy_state, stat_state):
    # Compute the policy-driven target on a copy so stat_state (which carries
    # accumulated event effects) is not clobbered. go_thru then drifts
    # stat_state toward this target one tick at a time.
    target = copy.deepcopy(stat_state)
    economy_policy2stats(policy_state, target)
    innerworkings_policy2stats(policy_state, target)
    humanrights_policy2stats(policy_state, target)
    security_policy2stats(policy_state, target)
    democraphics_policy2stats(policy_state, target)
    people_policy2stats(policy_state, target)
    return target

if __name__ == "__main__":
    pass