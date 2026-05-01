

def check_prerequisites(NAMES):

    def checking(tmp_rdy, tmp_nt_rdy, existing):
        for param in existing:
            name_dict, name_event, _ = param.split(',')
            x = NAMES[name_dict][name_event].prerequisites
            tmp_rdy.append(param)
            for a in x:
                result = a() if callable(a) else a
                if result == False:
                    tmp_rdy.remove(param)
                    tmp_nt_rdy.append(param)
                    break
        return tmp_rdy, tmp_nt_rdy


    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\ready.txt'
    path_nt = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\not_ready.txt'
    ready = []
    not_ready = []


    with open(path, '+a', encoding='utf-8') as f:
        f.seek(0)
        existing = f.readlines()
        a, b = checking([], [], existing)
        
    ready = ready+a
    not_ready = not_ready+b
    

    with open(path_nt, '+a', encoding='utf-8') as f:
        f.seek(0)
        existing = f.readlines()
        a, b = checking([], [], existing)
    ready = ready + a
    not_ready = not_ready + b

    with open(path, 'w') as f:
        for para in ready:
            f.write(para)
    with open(path_nt, 'w') as f:
        for para in not_ready:
            f.write(para)

def write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES):
    import random
    def write_to_files(ids, not_ids):
        # add event to txt
        path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\ready.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for line in ids:
                f.write(line)
        
        path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\not_ready.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for line in not_ids:
                f.write(line)

    ids = []
    not_ids = []
    for event in EVENTS:
        key = next(k for k, v in NAMES.items() if v is event) # k is the event name, ex POLARISATION
        #find what order of op
        curr_opp = CURR_OP[f'EVENTS_{key}']
        
        if NXT_EVENT[f'EVENTS_{key}'] == None:
            temp_ids = [e.id for e in event.values() if getattr(e, "order_of_ops", None) == curr_opp]
        else:
            temp_ids = [NXT_EVENT[f'EVENTS_{key}']]

        temp_not_ids = []

        for idd in temp_ids:
            #check if prerequisites met
            x = event[idd].prerequisites
            for a in x:
                result = a() if callable(a) else a
                if result == False:
                    temp_ids.remove(idd)
                    temp_not_ids.append(idd)
                    break

        ids = ids + [f'{event['name']},{i},{curr_opp}\n' for i in temp_ids]
        not_ids = not_ids + [f'{event['name']},{i},{curr_opp}\n' for i in temp_not_ids]

    random.shuffle(ids)
    random.shuffle(not_ids)
    write_to_files(set(ids), set(not_ids))

def open_ready_events(CURR_OP):
    temp_possible = []
    path = 'C:\\Users\\jtpta\\OneDrive\\Pulpit\\personal\\stavanger_app\\web\\CLI\\chain_of_events\\ready.txt'
    with open(path, 'r') as f:
        f.seek(0)
        existing = f.readlines()

        for stuff in existing:
            coe_name, event_name, ev_order_of_ops = stuff.split(',')


            CURR_OP[f'EVENTS_{coe_name}'] = int(ev_order_of_ops.strip('\n'))
            temp_possible.append([coe_name, event_name])

    return temp_possible
      
def game_simul(EVENTS, CURR_OP, NXT_EVENT, NAMES, possible_ev, policy_state, stats_state, EventProcessor):
    import random
    write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES)

    possible_ev = open_ready_events(CURR_OP)
    if possible_ev == []:
        print('Bye Bye miss american pie')
        quit()


    coe_name, event_name = possible_ev.pop(random.randint(0, len(possible_ev)-1))

    engine = EventProcessor(NAMES[coe_name], policy_state, stats_state)

    event = engine.trigger(event_name)

    print('\n' + event.description)
    choices = event.available_choices(policy_state)

    for i, choice in enumerate(choices):
        print(f"{i}: {choice.label}")
    selection = int(input("Choose: \n"))

    next_event_id = engine.choose(choices[selection])

    if next_event_id == None:
        EVENTS.remove(NAMES[coe_name])       
        del CURR_OP[f'EVENTS_{coe_name}']
        del NXT_EVENT[f'EVENTS_{coe_name}']
        del NAMES[coe_name]

    else:        
        CURR_OP[f'EVENTS_{coe_name}'] = NAMES[coe_name][next_event_id].order_of_ops
        NXT_EVENT[f'EVENTS_{coe_name}'] = next_event_id
    write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES)



if __name__ == "__main__":
    pass

# implement chain-switching functionality