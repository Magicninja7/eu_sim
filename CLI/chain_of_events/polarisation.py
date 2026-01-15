from coe_logic import Event, Transition, EventProcessor
from infra import stats, policies

# Create instance once
policy_state = policies()

EVENTS_POLARISARION = {}
EVENTS_POLARISARION["protests"] = Event(
    id="protests",
    description="Mass protests erupt across the country.",
    effects={"budget": -20},
    transitions=[
        Transition(
            label="Crack down on protesters",
            condition=lambda state: state.politics["authoritarianism"] >= 40,
            target_event_id="crackdown"
        ),
        Transition(
            label="Offer political concessions",
            condition=lambda state: True,
            target_event_id="concessions"
        )
    ]
)

engine = EventProcessor(EVENTS_POLARISARION, policy_state)

event = engine.trigger("protests")


print(event.description)
choices = event.available_choices(policy_state)

for i, choice in enumerate(choices):
    print(f"{i}: {choice.label}")
selection = int(input("Choose: "))

next_event_id = engine.choose(choices[selection])

print(policy_state.economy['budget'])