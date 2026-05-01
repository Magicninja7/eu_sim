
def polarisat(Event, Transition, stats):
    EVENTS_POLARISATION = {}
    EVENTS_POLARISATION['name'] = 'POLARISATION'
    EVENTS_POLARISATION["1st_election"] = Event(
        id='1st_election',
        prerequisites=[True],
        order_of_ops=0,
        title='You are elected Commissioner!',
        description="On the 15th of January 2026 you have been elected as the new Commisioner of the EU. You pulled record-breaking number of votes, 86% of the popular vote, uniting both sides of the political spectrum.",
        effects_pol={},
        effects_stat={
            'legitimacy': 8,
            'social_cohesion': 6,
            'polarisation': -5,
            'civil_unrest': -2,
            'diplo_reputation': 2
        },
        transitions=[
            Transition(
                label="Yay",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="popularity_plummets"
            ),
            Transition(
                label="Time to celebrate!",
                condition=lambda state: True,
                target_event_id="popularity_plummets"
            )
        ]
    )  
    EVENTS_POLARISATION["popularity_plummets"] = Event(
        id='popularity_plummets',
        prerequisites=[True],
        order_of_ops=1,
        title='Popularity among left/left-leaning voters plummets!',
        description="Your decisions have created a division between them, and your more conservative followers. This also results in a rapid decline of you popularity, to measly 54%.",
        effects_pol={
            'internet_regulation': 2
        },
        effects_stat={
            'legitimacy': -12,
            'social_cohesion': -15,
            'polarisation': 16,
            'civil_unrest': 10,
            'freedom_of_assembly': -3
        },
        transitions=[
            Transition(
                label="Find common ground and appease them",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="talks"
            ),
            Transition(
                label="Hold my ground, no concessions",
                condition=lambda state: stats.human_rights['freedom_of_assembly'] < 80,
                target_event_id="division"
            )
        ]
    )   
    EVENTS_POLARISATION["talks"] = Event(
        id='talks',
        prerequisites=[True],
        order_of_ops=2,
        title='Talks with the opposition are drawing out!',
        description="The opposition has proven innefective after over 1month of talks. They are demanding more and more radical decisions from us. We must do somthing!",
        effects_pol={
            'power_struggle': 4
        },
        effects_stat={
            'state_capacity': -5,
            'bureaucracy': 5,
            'civil_unrest': 4,
            'polarisation': 7,
            'social_cohesion': -6
        },
        transitions=[
            Transition(
                label="Continue talks until a mutually benefical decision is reached",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="talks"
            ),
            Transition(
                label="Cave to the opposition",
                condition=lambda state: True,
                target_event_id="talks"
            ),
            Transition(
                label="Ditch the talks",
                condition=lambda state:True,
                target_event_id="division"
            )
        ]
    )  
    EVENTS_POLARISATION["division"] = Event(
        id='division',
        prerequisites=[lambda: stats.human_rights['freedom_of_assembly'] > 70],
        order_of_ops=2,
        title='The opposition rallies people against you!',
        description="The people came to the streets to protest your recent actions!",
        effects_pol={
            'police_style': 4,
            'surveillance': 3
        },
        effects_stat={
            'civil_unrest': 16,
            'polarisation': 15,
            'social_cohesion': -12,
            'freedom_of_assembly': -6,
            'legitimacy': -10,
            'internal_security': -3
        },
        transitions=[
            Transition(
                label="Find common ground with the other side & appease",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="talks"
            ),
            Transition(
                label="Hold the ground, no concessions",
                condition=lambda state: True,
                target_event_id=None
            )
        ]
    )  
    return EVENTS_POLARISATION

