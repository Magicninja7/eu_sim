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
        effects_stat={},
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
        title='fuck you',
        description="fuck you v2",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="womp womp",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None
            ),
        ]
    )
    return EVENTS_TERRORIST_ATT_ISIS_1