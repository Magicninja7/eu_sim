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
    'economy': ['gdp', 'hdi', 'inflation', 'unemployment', 'debt_to_gdp', 'innovation', 'big_business', 'income_inequality'],
    'inner_workings': ['legitimacy', 'state_capacity', 'corruption', 'military_pos', 'police_respect', 'rule_of_law', 'bureaucracy'],
    'diplomacy': ['diplo_reputation', 'alliance_pwr', 'soft_pwr', 'sanctions_press', 'trade_dep', 'intelligence_lvl'],
    'human_rights': ['freedom_of_speech', 'freedom_of_press', 'freedom_of_assembly', 'freedom_of_religion', 'political_rights', 'minority_rights', 'due_process', 'freedom_to_privacy'],
    'security': ['crime_rate', 'organised_crime', 'border_control', 'internal_security', 'cybersec', 'military_readiness'],
    'demographics': ['age_structure', 'population_growth', 'urbanization', 'education_lvl', 'avg_age'],
    'people': ['migration_rate', 'war_fatigue', 'polarisation', 'terrorism', 'civil_unrest', 'social_cohesion', 'revolutionary_sentiments']
}


class policies:
    def __init__(self):
        
        # economic policies
        self.economy = {
            'budget_deficit': -20, # in percentage of budget
            'minimum_wage': 2000, # in euro
            'vat': 15, # as percentage
            'public_spending': 100, # austerity - expansion
            'state_ownership': 30, # privatisation - nationalisation
            'trade': 80, # free-trade - protectionism
            'labour_regulation': 100, # flexible - protective
            'industry': 30, # laisezz-faire - state-planning
        }

        #taxes
        self.taxation = {
            'low': 30,
            'medium': 60,
            'high': 90,
        }

 
        # inside politics policy
        self.politics = {
            'authoritarianism': 10, # direct democracy - power of one
            'censorship': 90, # preventive censorship - complete freedom of speech
            'power_struggle': 50, # EP dominance - EC dominance
            'judicial_independence': 100, # politicised-courts - judicial independence
            'election_fairness': 90, # rigged - democratic
            'surveillance': 70, # total-privacy - surveillance state
            'media_ownership': 40, # completely private - fully public
            'internet_regulation': 30, # what can and cannot be posted on the internet
            'ngo_regulation': 20, # no-regulation - no-independence
        }

        # Police
        self.police = {
            'police_funding': 70, # underfunfed - para-military
            'police_style': 20, # communitative - repressive
            'prison_policy': 30, # rehabilitative - punitive
            'death_pen': 0, # delagalised - regularly excersized
        }

        # military / foreign-policy
        self.military = {
            'military_budget': 3.5, # as percent of budget
            'conscription': 30, # none - mandatory
            'force_purpose': 60, # defensive - expeditionary
            'intervention': 40, # non-interventionist - interventionist
            'sanctions_policy': 80, # aggresive - cooperative
            'alliance_status': 100, # lone - unitary block
            'foreign_aid': 90, # none - a lot
        }

        # culture 
        self.culture = {
            'religion_influence': 0, # secular - theocratic
            'nationalism': 60, # cosmopolitanism - nationalism
            'nation_ident': 40, # people - ethnicity
            'minority_autonomy': 70, # repression - free to practise
        }

        #environment
        self.environment = {
            'env_regulation': 50, # environmentalism - industry over all
            'public_transport': 80, # none - get everywhere
            'energy_mix': 60, # as percentage of total energy production
            'carbon_zero': 80, # push for carbon-zero country
        }

        # social policy
        self.social = {
            'social_policy': 80, # minimum-life - universal coverage
            'labour_policy': 80, # employer-friendly - worker-friendly
            'healthcare_policy': 90, # full-private - full-public
            'unemployment_policy': 80, # none - livable
            'pension_policy': 95, # no-money - a-lot-investment
            'education_policy': 95, # privatised - public
            'housing_policy': 30, # market-based - state-housing
            'migration_policy': 60, # closed for everyone - open borders
        }




class stats:
    def __init__(self):
        # economy
        self.economy = {
            'gdp': 10000000, # in mln
            'hdi': 91, # HDi*100
            'inflation': 2, # percentage of inflation
            'unemployment': 6, # 0-100 %
            'debt_to_gdp': 0, # 0: none, 100: equal to gdp
            'innovation': 50, # stagnation - best
            'big_business': 12, # number of companies in top100 
            'income_inequality': 40, # gini coefficient, from 0 to 100
        }

        # stats/effects on country
        # workings of the state
        self.inner_workings = {
            'legitimacy': 100, # repressive-dictatorship - democracy
            'state_capacity': 90, # failed state - ability to enforce will of the governemnt
            'corruption': 5, # clear institutions - kleptocracy
            'military_pos': 100, # politicised - independent
            'police_respect': 80, # fear - respected
            'rule_of_law': 90, # arbitrary-verdicts - laws-respected
            'bureaucracy': 70, # no-administrative-overload-(effective bureaucracy) - administrative-overload
        }

        # diplomacy
        self.diplomacy = {
            'diplo_reputation': 90, # forgetable - important player
            'alliance_pwr': 100, # isolated - united
            'soft_pwr': 80, # no-cultural-exports - known-everywhere
            'sanctions_press': 0, # no-noticable-effect - crippled
            'trade_dep': 60, # autarky - can't-survive-w/imports/exports
            'intelligence_lvl': 85, # no-good-agency - can-do-anything
        }

        # human rights
        self.human_rights = {
            'freedom_of_speech': 90, # nothing - everything
            'freedom_of_press': 90, # only-approved - anything
            'freedom_of_assembly': 70, # only pro-gov - anything
            'freedom_of_religion': 90, # banned-religions - all-religions
            'political_rights': 100, # no-democracy - citizens-democracy
            'minority_rights': 90, # holocaust-v2 - equality
            'due_process': 99, # lawlessness - correct judicial process
            'freedom_to_privacy': 60, # spy-state - right-to-privacy
        }

        #security
        self.security = {
            'crime_rate': 50, # no crimes - lawlessness
            'organised_crime': 50, # non-existent - run the country
            'border_control': 80, # common-illegal-crossings - no-leaks
            'internal_security': 80, # no-defense - flawless-sec
            'cybersec': 80, # no-cybersec-defense - full-sec
            'military_readiness': 80, # symbolic - full_readiness
        }



        # demographics
        self.demographics = {
            'age_structure': 55, # avrg age
            'population_growth': 1.4, # average children per woman
            'urbanization': 75, # as percentage of people living in urban areas
            'education_lvl': 45, # as ercentage of bachalor-educated people
            'avg_age': 81.5, # as average age
        }

        # people & political stability
        self.people = {
            'migration_rate': 2.0, # net migration rate per 1000 people
            'war_fatigue': 0, # no-war 0 high fatigue
            'polarisation': 50, # variety-of-views - unitary-views
            'terrorism': 50, # no-risk - inevetable
            'civil_unrest': 10, # calm - riots
            'social_cohesion': 70, # divided-society - unified-society
            'revolutionary_sentiments': 1, # calm - storm the bastille!
        }

class last_incrimentation:
    def __init__(self):
        # economy
        self.economy = {
            'gdp': 0, # in mln
            'hdi': 0, # HDi*100
            'inflation': 0, # percentage of inflation
            'unemployment': 0, # 0-100 %
            'debt_to_gdp': 0, # 0: none, 100: equal to gdp
            'innovation': 0, # stagnation - best
            'big_business': 0, # number of companies in top100 
            'income_inequality': 0, # gini coefficient, from 0 to 100
        }

        # stats/effects on country
        # workings of the state
        self.inner_workings = {
            'legitimacy': 0, # repressive-dictatorship - democracy
            'state_capacity': 0, # failed state - ability to enforce will of the governemnt
            'corruption': 0, # clear institutions - kleptocracy
            'military_pos': 0, # politicised - independent
            'police_respect': 0, # fear - respected
            'rule_of_law': 0, # arbitrary-verdicts - laws-respected
            'bureaucracy': 0, # no-administrative-overload-(effective bureaucracy) - administrative-overload
        }

        # diplomacy
        self.diplomacy = {
            'diplo_reputation': 0, # forgetable - important player
            'alliance_pwr': 0, # isolated - united
            'soft_pwr': 0, # no-cultural-exports - known-everywhere
            'sanctions_press': 0, # no-noticable-effect - crippled
            'trade_dep': 0, # autarky - can't-survive-w/imports/exports
            'intelligence_lvl': 0, # no-good-agency - can-do-anything
        }

        # human rights
        self.human_rights = {
            'freedom_of_speech': 0, # nothing - everything
            'freedom_of_press': 0, # only-approved - anything
            'freedom_of_assembly': 0, # only pro-gov - anything
            'freedom_of_religion': 0, # banned-religions - all-religions
            'political_rights': 0, # no-democracy - citizens-democracy
            'minority_rights': 0, # holocaust-v2 - equality
            'due_process': 0, # lawlessness - correct judicial process
            'freedom_to_privacy': 0, # spy-state - right-to-privacy
        }

        #security
        self.security = {
            'crime_rate': 0, # no crimes - lawlessness
            'organised_crime': 0, # non-existent - run the country
            'border_control': 0, # common-illegal-crossings - no-leaks
            'internal_security': 0, # no-defense - flawless-sec
            'cybersec': 0, # no-cybersec-defense - full-sec
            'military_readiness': 0, # symbolic - full_readiness
        }



        # demographics
        self.demographics = {
            'age_structure': 0,
            'population_growth': 0,
            'urbanization': 0,
            'education_lvl': 0,
            'avg_age': 0,
        }

        # people & political stability
        self.people = {
            'migration_rate': 0,
            'war_fatigue': 0,
            'polarisation': 0,
            'terrorism': 0,
            'civil_unrest': 0,
            'social_cohesion': 0,
            'revolutionary_sentiments': 0,
        }