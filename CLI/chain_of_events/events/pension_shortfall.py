

def pension_shortfall(Event, Transition, stats):
    EVENTS_PENSION_SHORTFALL = {}
    EVENTS_PENSION_SHORTFALL['name'] = 'PENSION_SHORTFALL'
    EVENTS_PENSION_SHORTFALL["pension_shortfall_start"] = Event(
        id='pension_shortfall_start',
        prerequisites=[True],
        order_of_ops=0,
        title='Pension system shortfall',
        description="Ministry of Finance has confirmed the dark scenario: public pension system deficit exceeds projections by ~4 percent of gdp next year. Demographics are worsening, contributions shrinking and recipients growing. Leaked document says the system will become insolvent within 3 years.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="start working on a reform bill",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="1.1"
            ),
            Transition(
                label="downplay issues as a temporary accounting imbalance having no translation into reality",
                condition=lambda state: True,
                target_event_id="1.2"
            ),
            Transition(
                label='blame previous government, and launch an investigation commission',
                condition=lambda state: True,
                target_event_id="1.3"
            ),
            Transition(
                label='debt debt and more debt to patch the hole',
                condition=lambda state: True,
                target_event_id="1.4"
            )
        ]
    )
    EVENTS_PENSION_SHORTFALL["1.1"] = Event(
        id='1.1',
        prerequisites=[True],
        order_of_ops=1,
        title='Bill to reform pension system',
        description="What is the main direction this bill will go?",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="retirement age increase",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="2.10"
            ),
            Transition(
                label="contribution rate increase",
                condition=lambda state: True,
                target_event_id="2.11"
            ),
            Transition(
                label="hybrid - small age increase, increase contribution, and introducing a private system alongside the public one",
                condition=lambda state: True,
                target_event_id="2.4"
            ),
            Transition(
                label='partial privatization of the system',
                condition=lambda state: True,
                target_event_id="2.12"
            )
        ]
    )
    EVENTS_PENSION_SHORTFALL["1.2"] = Event(
        id='1.2',
        prerequisites=[True],
        order_of_ops=0,
        title='Downplaying Issues',
        description="Markets are nervous, media start investigating, opposition is calling you a liar. The markets react accordingly, with a 8 percent fall over the last 2 days.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="release a part of the revised fiscal projections",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="2.20"
            ),
            Transition(
                label="wait until next fiscal year, to that time deny everything",
                condition=lambda state: True,
                target_event_id="2.21"
            ),
            Transition(
                label='attack media for spreading panic',
                condition=lambda state: True,
                target_event_id="2.22"
            )
        ]
    )
    EVENTS_PENSION_SHORTFALL["1.3"] = Event(
        id='1.3',
        prerequisites=[True],
        order_of_ops=0,
        title='Launching an Investigation Commission',
        description="You accuse the previous administration of negligence and delaying the problem. You launch a parlimentary commision; everyone but your most diehard supporters feel embarrased, at most.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="commision an independent and acturial audit of the system, and make it public",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="2.30"
            ),
            Transition(
                label="Use the commision for political theatre",
                condition=lambda state: True,
                target_event_id="2.31"
            )
        ]
    )
    EVENTS_PENSION_SHORTFALL["1.4"] = Event(
        id='1.4',
        prerequisites=[True],
        order_of_ops=0,
        title='Adding Funds via Sovereign Debt',
        description="You add funds to the pension system via issuing sovereign debt. Bonds yield rise slightly.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Issue domestic bonds",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="2.40"
            ),
            Transition(
                label="Monetise deficit through the ECB",
                condition=lambda state: True,
                target_event_id="2.41"
            )
        ]
    )
    EVENTS_PENSION_SHORTFALL["2.10"] = Event(
        id='2.10',
        prerequisites=[True],
        order_of_ops=0,
        title='Raising Retirement Age',
        description="Raise the retirment age by 3 years. Young voters approve, labour unions and older citizens go to protests",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="hold firm",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.100"
            ),
            Transition(
                label="sit to negotiations with labour unions",
                condition=lambda state: True,
                target_event_id="3.101"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.11"] = Event(
        id='2.11',
        prerequisites=[True],
        order_of_ops=0,
        title='Increasing Payroll Contributions',
        description="Payroll contributions increase by 2percent. Small and medium businesses ",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Split costs between employers and employees",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.110"
            ),
            Transition(
                label="keep burden on employers",
                condition=lambda state: True,
                target_event_id="3.111"
            ),
            Transition(
                label='implement a steep progressive tax system, burdening the richest firms more',
                condition=lambda state: True,
                target_event_id="3.112"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.12"] = Event(
        id='2.12',
        prerequisites=[True],
        order_of_ops=0,
        title='You expand the private pension funds. Markets, especially from the newly expanded sector, recover. Older voters panic, social citizens file protests.',
        description="",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="mandatory partial redirection contributions",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.120"
            ),
            Transition(
                label="voluntary opt-in",
                condition=lambda state: True,
                target_event_id="3.120"
            ),
            Transition(
                label='slow 10 year transition',
                condition=lambda state: True,
                target_event_id="3.120"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.13"] = Event(
        id='2.13',
        prerequisites=[True],
        order_of_ops=0,
        title='Combining Reforms',
        description="You combine small retirement age increase, modest contribution rise, and slight benefit formula change. Markets recover, and public stops panicking.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="good",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id=""
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.20"] = Event(
        id='2.20',
        prerequisites=[True],
        order_of_ops=0,
        title='Market Projections',
        description="You release market projections, markets and the public slightly stablise. The opposition requires full transparency, though.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="open all acturial nooks",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.200"
            ),
            Transition(
                label="ignore the demands",
                condition=lambda state: True,
                target_event_id="3.201"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.21"] = Event(
        id='2.21',
        prerequisites=[True],
        order_of_ops=0,
        title='Media Accusations',
        description='You accused the media of spreading panic and "economic sabotage", the public broadcaster spreads the narrative. All the other press, however, react strongly against.',
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Investigate journalists leading anti-governemnt articles",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.210"
            ),
            Transition(
                label="Invite opposition to talks",
                condition=lambda state: True,
                target_event_id="3.120" # TODO -> add new event line
            ),
            Transition(
                label='soften rhetoric',
                condition=lambda state: True,
                target_event_id="1.1"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.22"] = Event(
        id='2.22',
        prerequisites=[True],
        order_of_ops=0,
        title='Stalling',
        description="You refrain from taking any actions and stall. 6 months later, the deficit only worsens. Minister of finance says, a credit rating downgrade is imminient.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="emergency reforms",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.220"
            ),
            Transition(
                label="temporary rent freeze",
                condition=lambda state: True,
                target_event_id="3.221"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.30"] = Event(
        id='2.30',
        prerequisites=[True],
        order_of_ops=0,
        title='Economist Report',
        description="Economists conduct interview. Their report confirms that without reforms, pensions will have to be dropped by 25% within 10years. Street protest intensify, both elderly and left-wing voters. Some report a fire.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="Use report to justify a reform package",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.300"
            ),
            Transition(
                label='reject the "alarmist projections"',
                condition=lambda state: True,
                target_event_id="3.301"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.31"] = Event(
        id='2.31',
        prerequisites=[True],
        order_of_ops=0,
        title='Commission Hearing',
        description="Commission hearing become a spectacle - however trust only declines. ",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="pivot to a real reform",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.310"
            ),
            Transition(
                label="double down on the blame narrative",
                condition=lambda state: True,
                target_event_id="3.311"
            ),
            Transition(
                label='',
                condition=lambda state: True,
                target_event_id=""
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.32"] = Event(
        id='2.32',
        prerequisites=[True],
        order_of_ops=0,
        title='Opposition Demands',
        description="Opposition demands a shared ownership of the reform bill.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="accept co-authorship",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.320"
            ),
            Transition(
                label="collapse the talks, and accuse opposition of obstruction",
                condition=lambda state: True,
                target_event_id="3.321"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.40"] = Event(
        id='2.40',
        prerequisites=[True],
        order_of_ops=0,
        title='Banks Absorb Bonds',
        description="Banks absorb bonds, yet the crowding out effect slows down gdp projections.Banks absorb bonds, yet the crowding out effect slows down gdp projections.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="structural reform within the year",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="1.1"
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["2.41"] = Event(
        id='2.41',
        prerequisites=[True],
        order_of_ops=0,
        title='Central Bank Supports Deficit',
        description="Central bank indirectly supports deficit. Inflation rises gradually.",
        effects_pol={},
        effects_stat={},
        transitions=[
            Transition(
                label="impose price controls",
                condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
                target_event_id="3.410"
            ),
            Transition(
                label="blame global factors",
                condition=lambda state: True,
                target_event_id="3.411"
            ),
            Transition(
                label='',
                condition=lambda state: True,
                target_event_id=""
            )
        ]
    )    
    EVENTS_PENSION_SHORTFALL["3.100"] = Event(
        id='3.100',
        prerequisites=[True],
        order_of_ops=0,
        title='',
        description="Protests intensify, and turn violent. Cases of police officers being beaten up. Protesters report police violents. several fires are seen throighout the credibility",
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

