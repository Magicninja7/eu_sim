from coe_logic import Event, Transition, EventProcessor
from infra import stats, policies
policy_state = policies()
stats = stats()


EVENTS_POLARISATION = {}
EVENTS_POLARISATION["1st_election"] = Event(
    id="1st_election",
    prerequisites=[False],
    order_of_ops=0,
    title='You are elected Commissioner!',
    description="On the 15th of January 2026 you have been elected as the new Commisioner of the EU. You pulled record-breaking number of votes, 86% of the popular vote, uniting both sides of the political spectrum.",
    effects_pol={},
    effects_stat={},
    transitions=[
        Transition(
            label="Yay",
            condition=lambda state: True, #condition=lambda state: stats.politics["authoritarianism"] >= 40,
            target_event_id="unrest"
        ),
        Transition(
            label="Time to celebrate!",
            condition=lambda state: True
            target_event_id="unrest"
        )
    ]
)  


def main():

    curr_opp = 0 # current order of operations event

    # list of id's of events based of order_of_ops
    ids = [e.id for e in EVENTS_POLARISATION.values() if getattr(e, "order_of_ops", None) == curr_opp]
    ids_not_ready = []
    for idd in ids:
        #check if prerequisites met
        x = EVENTS_POLARISATION[idd].prerequisites
        y = True
        for a in x:
            if a == False:
                y = False
                ids.remove(idd)
                ids_not_ready.append(idd)
                break

    
    # add event to txt
    '''
    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\ready.txt'
    lines_to_add = {f'POLARISATION,{i},{curr_opp}\n' for i in ids}
    with open(path, 'a+', encoding='utf-8') as f:
        f.seek(0)
        existing = set(f.readlines())
        for line in sorted(lines_to_add - existing):
            f.write(line)
    
    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\not_ready.txt'
    lines_to_add = {f'POLARISATION,{i},{curr_opp}\n' for i in ids_not_ready}
    with open(path, 'a+', encoding='utf-8') as f:
        f.seek(0)
        existing = set(f.readlines())
        for line in sorted(lines_to_add - existing):
            f.write(line)
    '''

    # trigger events
    '''
    engine = EventProcessor(EVENTS_POLARISATION, policy_state)

    event = engine.trigger("protests")

    print(event.description)
    choices = event.available_choices(policy_state)

    for i, choice in enumerate(choices):
        print(f"{i}: {choice.label}")
    selection = int(input("Choose: "))

    next_event_id = engine.choose(choices[selection])

    print(policy_state.economy['budget'])
    '''
