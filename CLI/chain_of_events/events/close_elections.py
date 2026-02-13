def cls_elections(Event, Transition, stats):
    EVENTS_CLOSE_ELECTIONS = {}
    EVENTS_CLOSE_ELECTIONS['name'] = 'CLOSE_ELECTIONS'
    EVENTS_CLOSE_ELECTIONS["big_election_win_fraud"] = Event(
        id='big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=0,
        title='You won the elections!',
        description="You lead the ____, a ruling party that just won a shocking landslide victory, completely in contrast to the exit polls.The opposition bloc claims widespread electoral fraud. International observers are divided, the country is polarised, and TV networks are running 24/h coverage.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Create and independent audit",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="audit_big_election_win_fraud"
            ),
            Transition(
                label="Dismiss claims as lies",
                condition=lambda state: True,
                target_event_id="claims_lies_big_election_win_fraud"
            ),
            Transition(
                label='Order removal of "harmful disinformation"',
                condition=lambda state: True,
                target_event_id="removal_disinformation_big_election_win_fraud"
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["audit_big_election_win_fraud"] = Event(
        id='audit_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=1,
        title='Audit details',
        description="You announce the audit, public demands transparency. Who will conduct it?",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="A parliamentary committee",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="parliamentary_committee_big_election_win_fraud"
            ),
            Transition(
                label="An executive review commission",
                condition=lambda state: True,
                target_event_id="exe_review_big_election_win_fraud"
            ),
            Transition(
                label='A judicial oversight panel',
                condition=lambda state: True,
                target_event_id="courts_audit_big_election_win_fraud"
            )
        ]
    )   
    EVENTS_CLOSE_ELECTIONS["claims_lies_big_election_win_fraud"] = Event(
        id='claims_lies_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=1,
        title='Opposition rallies',
        description='You call the allegations a "desperate hail mary, in light of a loss". The opposition escalates rhetoric, news network begin investigative coverage. Protests start.',
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Increase anti-opposition rhetoric",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="propaganda_esc_big_election_win_fraud"
            ),
            Transition(
                label="Seek a back-channel compromise",
                condition=lambda state: True,
                target_event_id="negotiation_attmpt_big_election_win_fraud"
            ),
            Transition(
                label='Lower tone and call for unity during these instable times',
                condition=lambda state: True,
                target_event_id=None #todo -> mb back to 1.1
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["removal_disinformation_big_election_win_fraud"] = Event(
        id='removal_disinformation_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=1,
        title='Unexpected opposition to disinformation removal',
        description='Content alleging fraud is removed from major platforms under "national stability" provisions. Soon the ECHR opens a preliminary hearing review...',
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Reverse the censorship",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="censorship_rev_big_election_win_fraud"
            ),
            Transition(
                label="Maintain censorship, increase pro-stability rhetoric",
                condition=lambda state: True,
                target_event_id="censorship_mant_big_election_win_fraud"
            )
        ]
    ) 
    EVENTS_CLOSE_ELECTIONS["parliamentary_committee_big_election_win_fraud"] = Event(
        id='parliamentary_committee_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Pushback against parliamentary-run audit',
        description="Houston there is a problem, you control the parliment. The opposition and press realise that; court complaints were filed and protests mobilised.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Transfer audit to judiciary",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="courts_audit_big_election_win_fraud"
            ),
            Transition(
                label="Defend parliamentary neutrality",
                condition=lambda state: True,
                target_event_id=None #todo
            ),
            Transition(
                label='fast-track investigation and results before situation escalates',
                condition=lambda state: True,
                target_event_id=None
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["exe_review_big_election_win_fraud`"] = Event(
        id='exe_review_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Unstability, alleged authoritarianism!',
        description="Even you allies are uncomfortable, you are summoned infront of the ECHR to give explenations. Choose your defence strategy.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Reassign audit to courts",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="courts_audit_big_election_win_fraud"
            ),
            Transition(
                label='Stand firm with it being "Fully constitutional and within spirit of the law"',
                condition=lambda state: True,
                target_event_id=None # todo
            ),
            Transition(
                label='Announce compromise - parliamentary comission with foreign-led obserbers',
                condition=lambda state: True,
                target_event_id=None # todo
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["courts_audit_big_election_win_fraud"] = Event(
        id='courts_audit_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Court audit begins',
        description="Courts begin review, situation on the streets begin to calm. TVs update situation hourly, investigative programs release. Emotions and distrust remain high",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="respect full independence",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None #todo
            ),
            Transition(
                label="Quietly control the judges",
                condition=lambda state: True,
                target_event_id=None #todo
            ),
            Transition(
                label='Fuel propaganda during waiting period',
                condition=lambda state: True,
                target_event_id="propaganda_esc_big_election_win_fraud"
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["propaganda_esc_big_election_win_fraud"] = Event(
        id='propaganda_esc_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Taking critique becuase of increased rhetoric',
        description="Trust in the opposition trops drastically among your supporters. However independent press accuses you of disinformational campaigns. Foreign media begin reporting concerns.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label='Investigate the media! look for "bias" and foreign agent involvment',
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None #todo
            ),
            Transition(
                label="Open a debate on public television",
                condition=lambda state: True,
                target_event_id=None #todo
            ),
            Transition(
                label='De-escalate narrative',
                condition=lambda state: True,
                target_event_id=None #todo
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["negotiation_attmpt_big_election_win_fraud"] = Event(
        id='negotiation_attmpt_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Negotiations talking point',
        description="You open talks with the opposition, what is your goal in this?",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Joint public statement recognising original results",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None #todo
            ),
            Transition(
                label="Power-sharing concessions for backing down on election fraud allegations",
                condition=lambda state: True,
                target_event_id=None #todo
            ),
            Transition(
                label='Excersice delaying tactics, hoping for public losing their interest',
                condition=lambda state: True,
                target_event_id=None #todo
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["censorship_rev_big_election_win_fraud"] = Event(
        id='censorship_rev_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Results of previous restrictions',
        description="You frop the restrictions, ECHR shelves the case. However, you lose credibility in eyes of your most radical supporters, and opposition insists on fraud.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Oops",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None #todo
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["censorship_mant_big_election_win_fraud"] = Event(
        id='censorship_mant_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='Consequences of disinformation',
        description="The ECHR case continues, maintainment of censorship seen negatively. Protests continue and trust in you plummets",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="hmmmmmm",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="echr_ruling_big_election_win_fraud"
            )
        ]
    )
    EVENTS_CLOSE_ELECTIONS["echr_ruling_big_election_win_fraud"] = Event(
        id='echr_ruling_big_election_win_fraud',
        prerequisites=[True],
        order_of_ops=2,
        title='ECHR ruling',
        description="The ECHR has ruled against you, forcing to conduct a judicial audit and temporarily removing you from power, until the audit is over. Cheering erupts from the opposition, as you allies back away from you.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Comply with ruling",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=None #todo
            ),
            Transition(
                label="coup d'etat plot?",
                condition=lambda state: True,
                target_event_id=None #todo
            )
        ]
    )
    return EVENTS_CLOSE_ELECTIONS