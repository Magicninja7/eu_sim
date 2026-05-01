def cls_elections(Event, Transition, stats):
    EVENTS_CLOSE_ELECTIONS = {}
    EVENTS_CLOSE_ELECTIONS['name'] = 'name'
    EVENTS_CLOSE_ELECTIONS["event_id"] = Event(
        id='',
        prerequisites=[True],
        order_of_ops=0,
        title='',
        description="",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=""
            ),
            Transition(
                label="",
                condition=lambda state: True,
                target_event_id=""
            ),
            Transition(
                label='',
                condition=lambda state: True,
                target_event_id=""
            )
        ]
    )