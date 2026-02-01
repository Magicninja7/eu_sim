import math
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stavanger_app.web.CLI.chain_of_events.infra import policies, stats


_NORM_STAT = stats()
policy = policies()
stat = copy.deepcopy(_NORM_STAT)


# i should be writing my TO instead of coding this mess

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def economy_policy2stats(policy_state, stat_state) -> dict:
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

    inflation = 2.0
    inflation += max(deficit_share_gdp, 0.0) * 20.0
    inflation -= max(-deficit_share_gdp, 0.0) * 8.0
    inflation += float(econ['vat']) * 0.02
    inflation += (50.0 - float(econ['trade'])) * 0.03
    inflation += (100.0 - float(env['energy_mix'])) * 0.015
    inflation += (float(econ['labour_regulation']) - 50.0) * 0.01
    inflation = _clamp(inflation, 0.0, 15.0)

    wage_factor = float(econ['minimum_wage']) / 2000.0
    unemployment = (
        4.0
        + (float(econ['labour_regulation']) - 50.0) * 0.06
        + (wage_factor - 1.0) * 2.5
        - (float(econ['public_spending']) - 50.0) * 0.04
        - (float(econ['trade']) - 50.0) * 0.025
        - (float(soc['education_policy']) - 50.0) * 0.03
        + (tax_burden - 0.35) * 6.0
    )
    unemployment = _clamp(unemployment, 0.0, 25.0)

    debt_to_gdp = (
        25.0
        + max(deficit_share_gdp, 0.0) * 260.0
        - max(-deficit_share_gdp, 0.0) * 120.0
        + (float(econ['public_spending']) - 50.0) * 0.30
        + (float(econ['state_ownership']) - 50.0) * 0.20
        - (float(econ['trade']) - 50.0) * 0.15
        - progressivity * 0.08
        - (tax_burden - 0.35) * 40.0
    )
    debt_to_gdp = _clamp(debt_to_gdp, 0.0, 100.0)

    industry_gap = abs(float(econ["industry"]) - 50.0)
    ownership_gap = abs(float(econ["state_ownership"]) - 50.0)
    innovation = (
        45.0
        + (float(soc["education_policy"]) - 50.0) * 0.30
        + (float(econ["trade"]) - 50.0) * 0.20
        + (float(env["carbon_zero"]) - 50.0) * 0.05
        + (float(econ["public_spending"]) - 50.0) * 0.05
        - industry_gap * 0.10
        - ownership_gap * 0.08
        - (float(econ["labour_regulation"]) - 50.0) * 0.07
        - (float(pol["censorship"]) - 50.0) * 0.12
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
        45.0
        - progressivity * 0.28
        - (float(soc["social_policy"]) - 50.0) * 0.20
        - (float(soc["labour_policy"]) - 50.0) * 0.15
        - (float(soc["education_policy"]) - 50.0) * 0.08
        - (wage_factor - 1.0) * 3.0
        + (float(econ["trade"]) - 50.0) * 0.06
        - (float(econ["state_ownership"]) - 50.0) * 0.10
        + unemployment * 0.35
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
        45.0
        + (float(pol["election_fairness"]) - 50.0) * 0.45
        + (float(pol["judicial_independence"]) - 50.0) * 0.35
        + (float(soc["education_policy"]) - 50.0) * 0.12
        + (float(soc["healthcare_policy"]) - 50.0) * 0.10
        + (float(soc["social_policy"]) - 50.0) * 0.08
        - (float(pol["authoritarianism"]) - 50.0) * 0.30
        - (float(pol["censorship"]) - 50.0) * 0.25
        - (float(pol["surveillance"]) - 50.0) * 0.18
        - (float(pol["power_struggle"]) - 50.0) * 0.25
        - (float(pol["ngo_regulation"]) - 50.0) * 0.12
        - abs(float(police["police_style"]) - 55.0) * 0.06
    )
    legitimacy = _clamp(legitimacy, 0.0, 100.0)

    state_capacity = (
        50.0
        + gdp_scale * 1.1
        + (float(econ["public_spending"]) - 50.0) * 0.18
        + (float(police["police_funding"]) - 50.0) * 0.18
        + (float(military["military_budget"]) - 3.0) * 3.5
        + (float(soc["education_policy"]) - 50.0) * 0.14
        + (float(soc["healthcare_policy"]) - 50.0) * 0.08
        - (float(econ["labour_regulation"]) - 50.0) * 0.08
        - (float(env["env_regulation"]) - 50.0) * 0.05
        - abs(float(pol["power_struggle"]) - 50.0) * 0.12
    )
    state_capacity = _clamp(state_capacity, 0.0, 100.0)

    tax_burden = (0.2 * tax["low"] + 0.3 * tax["medium"] + 0.5 * tax["high"]) / 100.0
    corruption = (
        58.0
        - (float(pol["judicial_independence"]) - 50.0) * 0.40
        - (float(pol["election_fairness"]) - 50.0) * 0.28
        - (float(pol["censorship"]) - 50.0) * 0.12
        - (float(pol["surveillance"]) - 50.0) * 0.14
        - (float(pol["ngo_regulation"]) - 50.0) * 0.08
        + (float(pol["power_struggle"]) - 50.0) * 0.24
        + (float(econ["state_ownership"]) - 50.0) * 0.16
        + (tax_burden - 0.35) * 32.0
        - gdp_scale * 0.6
        - (float(soc["education_policy"]) - 50.0) * 0.06
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
        60.0
        - abs(float(police["police_style"]) - 55.0) * 0.40
        - (float(police["prison_policy"]) - 50.0) * 0.22
        - (float(police["death_pen"]) - 50.0) * 0.18
        - abs(float(police["police_funding"]) - 60.0) * 0.22
        + (float(pol["judicial_independence"]) - 50.0) * 0.12
        + (float(pol["election_fairness"]) - 50.0) * 0.06
        - (float(pol["surveillance"]) - 50.0) * 0.06
    )
    police_respect = _clamp(police_respect, 0.0, 100.0)

    rule_of_law = (
        55.0
        + (float(pol["judicial_independence"]) - 50.0) * 0.45
        + (float(pol["election_fairness"]) - 50.0) * 0.22
        - abs(float(police["police_funding"]) - 60.0) * 0.25
        - (float(pol["authoritarianism"]) - 50.0) * 0.22
        - (float(pol["censorship"]) - 50.0) * 0.16
        - (float(pol["surveillance"]) - 50.0) * 0.12
        - (float(pol["power_struggle"]) - 50.0) * 0.15
        - abs(float(police["police_style"]) - 55.0) * 0.10
        - (float(police["death_pen"]) - 50.0) * 0.06
    )
    rule_of_law = _clamp(rule_of_law, 0.0, 100.0)

    bureaucracy = (
        40.0
        + (float(econ["public_spending"]) - 50.0) * 0.26
        + (float(econ["state_ownership"]) - 50.0) * 0.22
        + (float(econ["labour_regulation"]) - 50.0) * 0.20
        + (float(env["env_regulation"]) - 50.0) * 0.12
        + (tax_burden - 0.35) * 36.0
        - gdp_scale * 0.55
        - (float(pol["power_struggle"]) - 50.0) * 0.12
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
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)

    pol = policy_state.politics
    police = policy_state.police
    cult = policy_state.culture
    soc = policy_state.social

    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    freedom_of_speech = (
        45.0
        + (100.0 - float(pol["censorship"])) * 0.35
        + (100.0 - float(pol["authoritarianism"])) * 0.20
        + (100.0 - float(pol["internet_regulation"])) * 0.20
        + (100.0 - float(pol["surveillance"])) * 0.10
        + (50.0 - float(pol["media_ownership"])) * 0.10
    )
    freedom_of_speech = _clamp(freedom_of_speech, 0.0, 100.0)

    freedom_of_press = (
        40.0
        + (100.0 - float(pol["censorship"])) * 0.30
        + (100.0 - float(pol["authoritarianism"])) * 0.18
        + (100.0 - float(pol["internet_regulation"])) * 0.14
        + (100.0 - float(pol["surveillance"])) * 0.10
        + (float(pol["judicial_independence"]) - 50.0) * 0.12
        + (50.0 - float(pol["media_ownership"])) * 0.16
    )
    freedom_of_press = _clamp(freedom_of_press, 0.0, 100.0)

    freedom_of_assembly = (
        40.0
        + (100.0 - float(pol["authoritarianism"])) * 0.24
        + (100.0 - float(pol["surveillance"])) * 0.16
        + (100.0 - float(pol["ngo_regulation"])) * 0.20
        + (50.0 - float(police["police_style"])) * 0.20
        + (float(pol["election_fairness"]) - 50.0) * 0.12
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
        35.0
        + (100.0 - float(pol["surveillance"])) * 0.40
        + (100.0 - float(pol["authoritarianism"])) * 0.16
        + (100.0 - float(pol["internet_regulation"])) * 0.20
        + (50.0 - float(pol["censorship"])) * 0.08
        + (50.0 - float(police["police_style"])) * 0.12
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
        20.0
        + (float(pol['surveillance']) - 50.0) * 0.30
        + (100.0 - float(police['police_funding']) - 50.0) * 0.25
        + (float(soc['social_policy']) - 60.0) * 0.20
        + (float(soc['housing_policy']) - 60.0) * 0.15
        - (100.0 - police['police_style'] - 50.0) * 0.15
        - (100.0 - police['prison_policy'] - 50.0) * 0.15
        + gdp_scale * 0.08

    )
    crime_rate = _clamp(crime_rate, 0.0, 100.0)

    organised_crime = (
        25.0
        - float(pol['surveillance']) * 0.20
        + (100.0 - float(police['police_funding']) - 50.0) * 0.35
        + (float(soc['social_policy']) - 60.0) * 0.20
        + (float(soc['housing_policy']) - 60.0) * 0.25
        + (100.0 - police['police_style'] - 50.0) * 0.15
        + (100.0 - police['prison_policy'] - 50.0) * 0.15
        + gdp_scale * 0.50
        + (100.0 - float(eco['industry']) - 50.0) * 0.20
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
    gdp = float(stat_state.economy.get("gdp", 0) or 0)
    gdp = max(gdp, 1.0)
    gdp_scale = _clamp((math.log10(gdp) - 3.5) * 12.0, 0.0, 30.0)

    eco = policy_state.economy
    pol = policy_state.politics
    soc = policy_state.social

    age_structure = (
        30.0
        - (float(soc['labour_policy']) - 50.0) * 0.20
        - (float(soc['migration_policy']) - 50.0) * 0.25
        + gdp_scale * 0.10
        + (float(soc['education_policy']) - 50.0) * 0.15
        + (float(soc['healthcare_policy']) - 50.0) * 0.10
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
        40.0
        + float(soc['education_policy']) * 0.50
        + (float(eco['public_spending']) - 50.0) * 0.20
        + gdp_scale * 0.15
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
        30.0
        - gdp_scale * 0.15
        + (float(mil['military_budget']) - 3.0) * 15.00
        + (float(mil['conscription']) - 50.0) * 0.20
        + (float(pol['authoritarianism']) - 40.0) * 0.15
        + (float(pol['censorship']) - 60.0) * 0.20
        + (float(mil['force_purpose']) - 70.0) * 0.15
        + (float(mil['intervention']) - 60.0) * 0.15
        - (float(mil['sanctions_policy']) - 50.0) * 0.15
    )
    war_fatigue = _clamp(war_fatigue, 0.0, 100.0)

    polarisation = (
        40.0
        + (float(pol['authoritarianism']) - 30.0) * 0.30
        + (float(pol['censorship']) - 20.0) * 0.25
        + (float(pol['power_struggle']) - 50.0) * 0.20
        + (float(soc['social_policy']) - 50.0) * 0.15
        + (float(cul['nationalism']) - 70.0) * 0.20
        - (float(soc['education_policy']) - 80.0) * 0.15
        - gdp_scale * 0.10
    )
    polarisation = _clamp(polarisation, 0.0, 100.0)
    
    terrorism = (
        30.0
        - (float(eco['trade']) - 60.0) * 0.20
        + (float(pol['authoritarianism']) - 30.0) * 0.30
        + (float(pol['censorship']) - 30.0) * 0.15
        + (100.0 - float(pol['election_fairness']) - 30.0) * 0.15
        - (float(pol['internet_regulation']) - 30.0) * 0.15
        - (float(cul['minority_autonomy']) - 40.0) * 0.20
        + (float(cul['nationalism']) - 40.0) * 0.20
        + gdp_scale * 0.30
    )
    terrorism = _clamp(terrorism, 1.0, 100.0)

    civil_unrest = (
        15.0
        + (float(pol['authoritarianism']) - 30.0) * 0.20
        + (float(pol['censorship']) - 30.0) * 0.15
        + (100.0 - float(pol['election_fairness']) - 30.0) * 0.15
        + (float(pol['internet_regulation']) - 50.0) * 0.20
        + (float(pol['ngo_regulation']) - 40.0) * 0.20
        + (float(police['police_style']) - 40.0) * 0.20
        - (float(cul['minority_autonomy']) - 40.0) * 0.20
        + (float(cul['nationalism']) - 30.0) * 0.25
        - (float(soc['social_policy']) - 50.0) * 0.10
        - (float(soc['pension_policy']) - 50.0) * 0.05
        - (float(soc['housing_policy']) - 50.0) * 0.10
        - (float(soc['healthcare_policy']) - 50.0) * 0.10
        - (float(soc['unemployment_policy']) - 50.0) * 0.05
        + (float(soc['migration_policy']) - 30.0) * 0.20
    )
    civil_unrest = _clamp(civil_unrest, 0.0, 100.0)

    social_cohesion = (
        40.0
        + float(cul['religion_influence']) * 0.20
        + (float(cul["nationalism"]) - 40.0) * 0.15
        - (100.0 - float(cul["nation_ident"]) - 60.0) * 0.15
        - float(soc['migration_policy']) * 0.15
        + float(soc['social_policy']) * 0.20
        + float(soc['education_policy']) * 0.15
    )
    social_cohesion = _clamp(social_cohesion, 1.0, 100.0)

    revolutionary_sentiments = (
        20.0
        + (float(pol['authoritarianism']) - 30.0) * 0.25
        + (float(pol['censorship']) - 20.0) * 0.20
        + (float(pol['power_struggle']) - 50.0) * 0.20
        - (float(soc['social_policy']) - 50.0) * 0.20
        + (float(cul['nationalism']) - 70.0) * 0.20
        - (float(soc['education_policy']) - 80.0) * 0.25
        - gdp_scale * 0.10
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
    economy_policy2stats(policy_state, stat_state)
    innerworkings_policy2stats(policy_state, stat_state)
    humanrights_policy2stats(policy_state, stat_state)
    security_policy2stats(policy_state, stat_state)
    democraphics_policy2stats(policy_state, stat_state)
    people_policy2stats(policy_state, stat_state)
    return stat_state

if __name__ == "__main__":
    pass