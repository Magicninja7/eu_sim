
def terrorist_isis_1(Event, Transition, stats):
    EVENTS_TERRORIST_ISIS_1 = {}
    EVENTS_TERRORIST_ISIS_1['name'] = 'TERRORIST_ISIS_1'
    EVENTS_TERRORIST_ISIS_1['internet_campaign'] = Event(
        id='internet_campaign',
        prerequisites=[True],
        order_of_ops=0,
        title='ISIS begins internet propaganda campaign!',
        description="Aimed at teens, its goal to recruit new jihadists in the EU. At the moment they're succeding, with the rate of ISIS-dictated attacks by EU citizens rapidly rising!",
        effects_pol={'budget': -50},
        effects_stat={},
        transitions=[
            Transition(
                label='Open an investigation',
                condition=lambda state: True,
                target_event_id=None
            ),
            Transition(
                label="Take all the posts down, and threaten to take down websites that don't!",
                condition=lambda state: stats.security['cybersec'] > 60,
                target_event_id='EVENTS_TERRORIST_ATT_ISIS_1'
            )
        ]
    )
    return EVENTS_TERRORIST_ISIS_1


