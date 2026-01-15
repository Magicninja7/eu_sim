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


class Event:
    def __init__(self, id, description, effects, transitions):
        self.id = id
        self.description = description
        self.effects = effects
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
        for k, v in event.effects.items():
            category = next((cat for cat, items in types_of_policies.items() if k in items), None)
            
            if category and hasattr(self.state, category):
                category_dict = getattr(self.state, category) 
                if k in category_dict:
                    category_dict[k] += v
                    if category_dict[k] > 100:
                        category_dict[k] = 100
        return event

    def choose(self, transition):
        return transition.target_event_id
