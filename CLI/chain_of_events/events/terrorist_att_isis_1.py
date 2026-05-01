def terrorist_att_isis_1(Event, Transition, stats):
    EVENTS_TERRORIST_ATT_ISIS_1 = {}
    EVENTS_TERRORIST_ATT_ISIS_1['name'] = 'TERRORIST_ATT_ISIS_1'
    EVENTS_TERRORIST_ATT_ISIS_1["attack"] = Event(
        id='attack',
        prerequisites=[True],
        order_of_ops=1,
        title='TERRORIST ATTACK ON PARIS',
        description="Today terrorist pledging allegiance to ISIS have attacked Paris, killing 68 people and injuring 200 more.",
        effects_pol={},
        effects_stat={
            'terrorism': 22,
            'civil_unrest': 14,
            'war_fatigue': 9,
            'social_cohesion': -12,
            'internal_security': -10,
            'freedom_of_assembly': -5,
            'legitimacy': -6,
            'diplo_reputation': -2
        },
        transitions=[
            Transition(
                label="ATTACK",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id='attack_res'
            ),
            Transition(
                label="INVESTIGATE",
                condition=lambda state: True,
                target_event_id='attack_res'
            ),
            Transition(
                label='WAIT',
                condition=lambda state: True,
                target_event_id='attack_res'
            )
        ]
    )
    EVENTS_TERRORIST_ATT_ISIS_1["attack_res"] = Event(
        id='attack_res',
        prerequisites=[True],
        order_of_ops=1,
        title='Post-attack emergency response',
        description="Emergency services restore order in affected districts, but intelligence warnings suggest elevated risk in the coming weeks.",
        effects_pol={
            'police_funding': 6,
            'surveillance': 5,
            'internet_regulation': 3
        },
        effects_stat={
            'internal_security': 6,
            'cybersec': 4,
            'terrorism': -6,
            'freedom_to_privacy': -6,
            'freedom_of_speech': -3
        },
        transitions=[
            Transition(
                label="womp womp",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None
            ),
        ]
    )
    return EVENTS_TERRORIST_ATT_ISIS_1