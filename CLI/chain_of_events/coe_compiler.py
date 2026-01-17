from coe_logic import Event, Transition, EventProcessor
from infra import stats, policies
policy_state=policies()
stats=stats()

from polarisation import EVENTS_POLARISATION
from terrorist_isis import EVENTS_TERRORIST_ISIS_1

def main():
    curr_opp = 0 # current order of operations event

    # list of id's of events based of order_of_ops
    pol_ids = [e.id for e in EVENTS_POLARISATION.values() if getattr(e, "order_of_ops", None) == curr_opp]
    pol_ids_not_ready = []
    for idd in pol_ids:
        #check if prerequisites met
        x = EVENTS_POLARISATION[idd].prerequisites
        y = True
        for a in x:
            if a == False:
                y = False
                pol_ids.remove(idd)
                pol_ids_not_ready.append(idd)
                break

    ter_ids = [e.id for e in EVENTS_TERRORIST_ISIS_1.values() if getattr(e, "order_of_ops", None) == curr_opp]
    ter_ids_not_ready = []
    for idd in ter_ids:
        #check if prerequisites met
        x = EVENTS_TERRORIST_ISIS_1[idd].prerequisites
        y = True
        for a in x:
            if a == False:
                y = False
                ter_ids.remove(idd)
                ter_ids_not_ready.append(idd)
                break

    
    # add event to txt
    lines_to_add = {f'POLARISATION,{i},{curr_opp}\n' for i in pol_ids}.union({f'TERRORIST_ISIS,{i},{curr_opp}\n' for i in ter_ids})
    not_lines_to_add = {f'POLARISATION,{i},{curr_opp}\n' for i in pol_ids_not_ready}.union({f'TERRORIST_ISIS,{i},{curr_opp}\n' for i in ter_ids_not_ready})
    write_to_files(lines_to_add, not_lines_to_add)


def write_to_files(ids, not_ids):
    # add event to txt
    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\ready.txt'
    with open(path, 'a+', encoding='utf-8') as f:
        f.seek(0)
        existing = set(f.readlines())
        for line in sorted(ids - existing):
            f.write(line)
    
    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\not_ready.txt'
    with open(path, 'a+', encoding='utf-8') as f:
        f.seek(0)
        existing = set(f.readlines())
        for line in sorted(not_ids - existing):
            f.write(line)


main()