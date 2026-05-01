import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stavanger_app.web.CLI.chain_of_events.coe_logic import Event, Transition, EventProcessor
from stavanger_app.web.CLI.chain_of_events.infra import stats, policies, types_of_stats, last_incrimentation
from stavanger_app.web.CLI.pol_2_stat.logic import do_all
from stavanger_app.web.CLI.pol_2_stat.increment import go_thru
from stavanger_app.web.CLI.chain_of_events.coe_compiler import game_simul
from stavanger_app.web.CLI.chain_of_events.polarisation import polarisat
from stavanger_app.web.CLI.chain_of_events.terrorist_isis import terror_isis_1
import random
import copy

policy_state=policies()
stats=stats()

possible_ev = []
las_increment = last_incrimentation()

EVENTS_POLARISATION = polarisat(Event, Transition, stats)
EVENTS_TERRORIST_ISIS_1 = terror_isis_1(Event, Transition, stats)

EVENTS = [EVENTS_POLARISATION, EVENTS_TERRORIST_ISIS_1]
CURR_OP = {'EVENTS_POLARISATION': 0, 'EVENTS_TERRORIST_ISIS_1': 0}
NXT_EVENT = {'EVENTS_POLARISATION': None, 'EVENTS_TERRORIST_ISIS_1': None}

NAMES = {
    'POLARISATION': EVENTS_POLARISATION,
    'TERRORIST_ISIS_1': EVENTS_TERRORIST_ISIS_1
}




while True:
    game_simul(EVENTS, CURR_OP, NXT_EVENT, NAMES, possible_ev, policy_state, stats, EventProcessor)
    stats_togo = do_all(policy_state, stats)
    stats, las_increment = go_thru(stats, stats_togo, las_increment, types_of_stats)