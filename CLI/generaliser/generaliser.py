types_of_stats = {
    'economy': ['gdp', 'hdi', 'inflation', 'unemployment', 'debt_to_gdp', 'innovation', 'big_business', 'income_inequality'],
    'inner_workings': ['legitimacy', 'state_capacity', 'corruption', 'military_pos', 'police_respect', 'rule_of_law', 'bureaucracy'],
    'diplomacy': ['diplo_reputation', 'alliance_pwr', 'soft_pwr', 'sanctions_press', 'trade_dep', 'intelligence_lvl'],
    'human_rights': ['freedom_of_speech', 'freedom_of_press', 'freedom_of_assembly', 'freedom_of_religion', 'political_rights', 'minority_rights', 'due_process', 'freedom_to_privacy'],
    'security': ['crime_rate', 'organised_crime', 'border_control', 'internal_security', 'cybersec', 'military_readiness'],
    'demographics': ['age_structure', 'population_growth', 'urbanization', 'education_lvl', 'avg_age'],
    'people': ['migration_rate', 'war_fatigue', 'polarisation', 'terrorism', 'civil_unrest', 'social_cohesion', 'revolutionary_sentiments']
}
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stavanger_app.web.CLI.chain_of_events.infra import stats
import math


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def generalise(stat_state) -> dict:
    econ = stat_state.economy
    inner = stat_state.inner_workings
    diplo = stat_state.diplomacy
    sec = stat_state.security
    dem = stat_state.demographics
    ppl = stat_state.people

    # normalize disparate raw stats into 0-100 ranges for realistic aggregation
    def _norm_gdp(gdp_raw: float) -> float:
        # GDP in millions in this dataset; use log scaling to map wide ranges into 0-100
        return _clamp((math.log10(max(gdp_raw, 1.0)) - 3.0) * 20.0, 0.0, 100.0)

    def _norm_proportion(x: float) -> float:
        # already 0-100 style values
        return _clamp(x, 0.0, 100.0)

    def _norm_inverse(x: float, max_val: float = 100.0) -> float:
        # higher raw value is worse (e.g., unemployment), return 0-100 goodness
        return _clamp((1.0 - (x / max_val)) * 100.0, 0.0, 100.0)

    # build normalized view used by aggregations
    necon = {
        'gdp': _norm_gdp(econ.get('gdp', 0)),
        'hdi': _norm_proportion(econ.get('hdi', 0)),
        'inflation': _norm_inverse(econ.get('inflation', 0), max_val=50.0),
        'unemployment': _norm_inverse(econ.get('unemployment', 0), max_val=100.0),
        'debt_to_gdp': _norm_inverse(econ.get('debt_to_gdp', 0), max_val=200.0),
        'innovation': _norm_proportion(econ.get('innovation', 0)),
        'big_business': _clamp(econ.get('big_business', 0) * 1.0, 0.0, 100.0),
        'income_inequality': _norm_inverse(econ.get('income_inequality', 0), max_val=100.0),
    }

    ndem = {
        'age_structure': _norm_proportion(dem.get('age_structure', 0)),
        'population_growth': _clamp((dem.get('population_growth', 0) / 3.0) * 100.0, 0.0, 100.0),
        'urbanization': _norm_proportion(dem.get('urbanization', 0)),
        'education_lvl': _norm_proportion(dem.get('education_lvl', 0)),
        'avg_age': _clamp((1.0 - ((dem.get('avg_age', 0) - 15.0) / 70.0)) * 100.0, 0.0, 100.0),
    }

    nppl = {
        'migration_rate': _clamp((ppl.get('migration_rate', 0) / 10.0) * 100.0, 0.0, 100.0),
        'war_fatigue': _norm_inverse(ppl.get('war_fatigue', 0), max_val=100.0),
        'polarisation': _norm_inverse(ppl.get('polarisation', 0), max_val=100.0),
        'terrorism': _norm_inverse(ppl.get('terrorism', 0), max_val=100.0),
        'civil_unrest': _norm_inverse(ppl.get('civil_unrest', 0), max_val=100.0),
        'social_cohesion': _norm_proportion(ppl.get('social_cohesion', 0)),
        'revolutionary_sentiments': _norm_inverse(ppl.get('revolutionary_sentiments', 0), max_val=100.0),
    }


    economics = (
        5.0
        + (necon['gdp'] * 0.40)
        + (necon['hdi'] * 0.12)
        + (necon['innovation'] * 0.15)
        + (necon['big_business'] * 0.03)
        + (necon['income_inequality'] * 0.12)
        + (necon['inflation'] * 0.10)
        + (necon['unemployment'] * 0.12)
        - ((100.0 - necon['debt_to_gdp']) * 0.08)
    )
    economics = _clamp(economics, 0.0, 100.0)

    inner_workings = (
        5.0
        + (inner['legitimacy'] * 0.22)
        + (inner['state_capacity'] * 0.22)
        - (inner['corruption'] * 0.55)
        + (inner['military_pos'] * 0.08)
        + (inner['police_respect'] * 0.12)
        + (inner['rule_of_law'] * 0.25)
        + (inner['bureaucracy'] * 0.08)
    )
    inner_workings = _clamp(inner_workings, 0.0, 100.0)

    diplomacy = (
        5.0
        + (diplo['diplo_reputation'] * 0.32)
        + (diplo['alliance_pwr'] * 0.28)
        + (diplo['soft_pwr'] * 0.22)
        - (diplo['sanctions_press'] * 0.25)
        - (diplo['trade_dep'] * 0.15)
        + (diplo['intelligence_lvl'] * 0.08)
    )
    diplomacy = _clamp(diplomacy, 0.0, 100.0)

    security = (
        5.0
        - (sec['crime_rate'] * 0.45)
        - (sec['organised_crime'] * 0.40)
        + (sec['border_control'] * 0.22)
        + (sec['internal_security'] * 0.32)
        + (sec['cybersec'] * 0.28)
        + (sec['military_readiness'] * 0.33)
    )
    security = _clamp(security, 0.0, 100.0)


    demographics = (
        5.0
        + (ndem['age_structure'] * 0.18)
        + (ndem['population_growth'] * 0.22)
        + (ndem['urbanization'] * 0.16)
        + (ndem['education_lvl'] * 0.27)
        + (ndem['avg_age'] * 0.17)
    )
    demographics = _clamp(demographics, 0.0, 100.0)

    people = (
        20.0
        + (nppl['migration_rate'] * 0.08)
        + (nppl['social_cohesion'] * 0.28)
        - (nppl['war_fatigue'] * 0.10)
        - (nppl['polarisation'] * 0.18)
        - (nppl['terrorism'] * 0.16)
        - (nppl['civil_unrest'] * 0.16)
        - (nppl['revolutionary_sentiments'] * 0.14)
    )
    people = _clamp(people, 10.0, 100.0)
    # human rights aggregation (use raw 0-100 style values)
    human = stat_state.human_rights
    hr = (
        5.0
        + (_clamp(human.get('freedom_of_speech', 0), 0.0, 100.0) * 0.16)
        + (_clamp(human.get('freedom_of_press', 0), 0.0, 100.0) * 0.14)
        + (_clamp(human.get('freedom_of_assembly', 0), 0.0, 100.0) * 0.14)
        + (_clamp(human.get('freedom_of_religion', 0), 0.0, 100.0) * 0.14)
        + (_clamp(human.get('political_rights', 0), 0.0, 100.0) * 0.24)
        + (_clamp(human.get('minority_rights', 0), 0.0, 100.0) * 0.08)
        + (_clamp(human.get('due_process', 0), 0.0, 100.0) * 0.10)
        + (_clamp(human.get('freedom_to_privacy', 0), 0.0, 100.0) * 0.10)
    )
    hr = _clamp(hr, 0.0, 100.0)

    return {
        'economics': economics,
        'inner_workings': inner_workings,
        'diplomacy': diplomacy,
        'security': security,
        'demographics': demographics,
        'people': people
        , 'human_rights': hr
    }


if __name__ == '__main__':
    # run standalone for quick inspection
    out = generalise(stats())
    for k, v in out.items():
        print(f"{k}: {v:.2f}")