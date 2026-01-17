types_of_policies = {
    'economy': ['budget', 'minimum_wage', 'vat', 'public_spending', 'state_ownership', 'trade', 'labour_regulation', 'industry'],
    'taxation': ['low', 'medium', 'high'],
    'politics': ['authoritarianism', 'censorship', 'power_struggle', 'judicial_independence', 'election_fairness', 'surveillance', 'media_ownership', 'internet_regulation', 'ngo_regulation'],
    'police': ['police_funding', 'police_style', 'prison_policy', 'death_pen'],
    'military': ['military_budget', 'conscription', 'force_purpose', 'intervention', 'sanctions_policy', 'alliance_status', 'foreign_aid'],
    'culture': ['religion_influence', 'nationalism', 'nation_ident', 'minority_autonomy'],
    'environment': ['env_regulation', 'public_transport', 'energy_mix', 'carbon_zero'],
    'social': ['social_policy', 'labour_policy', 'healthcare_policy', 'unemployment_policy', 'pension_policy', 'education_policy', 'housing_policy', 'migration_policy']
}
types_of_stats = {
    'inner_workings': ['legitimacy', 'state_capacity', 'corruption', 'military_pos', 'police_respect', 'rule_of_law', 'bureaucracy'],
    'people': ['war_fatigue', 'polarisation', 'terrorism', 'civil_unrest', 'social_cohesion', 'revolutionary_sentiments'],      
    'economy': ['hdi', 'inflation', 'unemployment', 'debt_to_gdp', 'innovation', 'big_business', 'income_inequality'],
    'security': ['crime_rate', 'organised_crime', 'border_control', 'internal_security', 'cybersec', 'military_readiness'],
    'human_rights': ['freedom_of_speech', 'freedom_of_press', 'freedom_of_assembly', 'freedom_of_religion', 'political_rights', 'minority_rights', 'due_process', 'freedom_to_privacy'],
    'demographics': ['age_structure', 'population_growth', 'urbanization', 'education_lvl', 'avg_age'],
    'diplomacy': ['diplo_reputation', 'alliance_pwr', 'soft_pwr', 'sanctions_press', 'trade_dep', 'intelligence_lvl']
}



class Event:
    def __init__(self, id, prerequisites, order_of_ops, title, description, effects_pol, effects_stat, transitions):
        self.id = id
        self.prerequisites = prerequisites
        self.order_of_ops = order_of_ops
        self.title = title
        self.description = description
        self.effects_pol = effects_pol
        self.effects_stat = effects_stat
        self.transitions = transitions

    def available_choices(self, state):
        return [
            t for t in self.transitions
            if t.is_available(state)
        ]

class Transition:
    def __init__(self, label, condition, target_event_id):

        self.label = label
        self.condition = condition
        self.target_event_id = target_event_id

    def is_available(self, state):
        return self.condition(state)


class EventProcessor:
    def __init__(self, events, state):
        self.events = events
        self.state = state
        self.current_event_id = None

    def trigger(self, event_id):
        event = self.events[event_id]
        self.current_event_id = event_id
        for k, v in event.effects_pol.items():
            category = next((cat for cat, items in types_of_policies.items() if k in items), None)
            
            if category and hasattr(self.state, category):
                category_dict = getattr(self.state, category) 
                if k in category_dict:
                    category_dict[k] += v

        for k, v in event.effects_stat.items():
            category = next((cat for cat, items in types_of_stats.items() if k in items), None)
            
            if category and hasattr(self.state, category):
                category_dict = getattr(self.state, category) 
                if k in category_dict:
                    category_dict[k] += v
        return event

    def choose(self, transition):
        return transition.target_event_id
