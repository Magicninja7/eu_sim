from __future__ import annotations, print_function
# print('hello world', file=sys.stderr)


import sys
import os
from pathlib import Path
from collections import deque
from threading import Lock, Thread
from time import sleep

# Add parent directory to path for relative imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chain_of_events.coe_logic import Event, Transition, EventProcessor
from chain_of_events.infra import stats, policies, types_of_stats, last_incrimentation
from pol_2_stat.logic import do_all
from pol_2_stat.increment import go_thru
from chain_of_events.coe_compiler import write_events_to_files, open_ready_events
from chain_of_events.events.polarisation import polarisat
from chain_of_events.events.terrorist_isis import terrorist_isis_1
from chain_of_events.events.terrorist_att_isis_1 import terrorist_att_isis_1
from chain_of_events.events.close_elections import cls_elections
from chain_of_events.events.pension_shortfall import pension_shortfall
from generaliser.generaliser import generalise
from flask import Flask, render_template, request, jsonify
from typing import Any
import random

policy_state = policies()
stats_state = stats()

notification_queue: deque[dict[str, Any]] = deque()
notification_lock = Lock()
notification_sequence = 0

possible_ev = []
las_increment = last_incrimentation()

game_over = False
collapsed_stats: list[str] = []


def check_game_over() -> tuple[bool, list[str]]:
    global game_over, collapsed_stats
    if game_over:
        return True, collapsed_stats
    gen = generalise(stats_state)
    fallen = [k for k, v in gen.items() if v <= 0]
    if fallen:
        game_over = True
        collapsed_stats = fallen
        return True, fallen
    return False, []


EVENTS_CLOSE_ELECTIONS = cls_elections(Event, Transition, stats_state)
EVENTS_POLARISATION = polarisat(Event, Transition, stats_state)
EVENTS_TERRORIST_ISIS_1 = terrorist_isis_1(Event, Transition, stats_state)
EVENTS_TERRORIST_ATT_ISIS_1 = terrorist_att_isis_1(Event, Transition, stats_state)
#EVENTS_PENSION_SHORTFALL = pension_shortfall(Event, Transition, stats_state)

EVENTS = [EVENTS_POLARISATION, EVENTS_TERRORIST_ISIS_1, EVENTS_TERRORIST_ATT_ISIS_1, EVENTS_CLOSE_ELECTIONS]

NAMES = {
    'POLARISATION': EVENTS_POLARISATION,
    'TERRORIST_ISIS_1': EVENTS_TERRORIST_ISIS_1,
    'TERRORIST_ATT_ISIS_1': EVENTS_TERRORIST_ATT_ISIS_1,
    'CLOSE_ELECTIONS': EVENTS_CLOSE_ELECTIONS
    #'PENSION_SHORTFALL': EVENTS_PENSION_SHORTFALL
}

CURR_OP = {f'EVENTS_{name}': 0 for name in NAMES}
NXT_EVENT = {f'EVENTS_{name}': None for name in NAMES}

curr_day = 1
dis_say_event = False
curr_month = 1
curr_year = 2026
months = {
    1: 31,
    2: 28,  # 29 days in leap year
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}
def check_leaps():
    if curr_year % 4 and not curr_year % 100:
        months[2] = 29
    elif curr_year % 4 and curr_year % 100 and curr_year % 400:
        months[2] = 29
    else:
        months[2] = 28
def handle_days(day, month, year):
    if month==12 and day == months[month]:
        year+=1
        month, day = 1, 1
    elif day > months[month]:
        month +=1
        if month ==13:
            month = 1
        day = 1
    return day, month, year



def create_app() -> Flask:
    # Specify template and static folders (one level up from app.py)
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    state: dict[str, Any] = {
        "current": None,
        "last_message": None,
    }

    def select_next_event() -> dict[str, Any] | None:
        write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES)

        possible = open_ready_events(CURR_OP)
        if not possible:
            return None

        coe_name, event_name = random.choice(possible)
        engine = EventProcessor(NAMES[coe_name], policy_state, stats_state)
        event = engine.trigger(event_name)
        choices = event.available_choices(policy_state)

        return {
            "coe_name": coe_name,
            "event_name": event_name,
            "event": event,
            "choices": choices,
        }

    def ensure_current_event() -> dict[str, Any] | None:
        if state["current"] is None:
            state["current"] = select_next_event()
        return state["current"]

    @app.get("/")
    def index():
        ensure_current_event()
        return render_template(
            "index.html",
            curr_date=f'{curr_day}/{curr_month}/{curr_year}',
            gdp=stats_state.economy['gdp'],
            tax_h=policy_state.taxation['high'],
        )

    @app.get("/api/notifications")
    def api_notifications():
        return jsonify({"notifications": drain_notifications()})

    @app.post("/api/notifications")
    def api_push_notification():
        payload = request.get_json(silent=True) or {}
        description = payload.get("description")
        classification = payload.get("classification")

        if not description or not classification:
            return jsonify({"error": "description and classification are required."}), 400

        notification = send_notification(
            description=str(description),
            classification=str(classification),
            date=str(payload.get("date")) if payload.get("date") else None,
            timestamp=str(payload.get("timestamp")) if payload.get("timestamp") else None,
            title=str(payload.get("title")) if payload.get("title") else None,
        )
        return jsonify({"ok": True, "notification": notification}), 201

    @app.get("/api/status")
    def api_status():
        global stats_state
        gdp = stats_state.economy['gdp']
        tax_l, tax_m, tax_h = policy_state.taxation['low'], policy_state.taxation['medium'], policy_state.taxation['high']
        gen = generalise(stats_state)
        is_over, collapsed = check_game_over()
        return jsonify({
            "date": f'{curr_day}/{curr_month}/{curr_year}',
            "day": curr_day,
            "gdp": gdp,
            "tax_l": tax_l,
            "tax_m": tax_m,
            "tax_h": tax_h,
            "stats": gen,
            "game_over": is_over,
            "collapsed": collapsed,
        })

    @app.get("/api/event")
    def api_event():
        global dis_say_event

        is_over, collapsed = check_game_over()
        if is_over:
            return jsonify({"done": True, "message": "Game over.", "game_over": True, "collapsed": collapsed})

        current = ensure_current_event()

        if current is None:
            message = state.get("last_message") or "No more events available."
            return jsonify({"done": True, "message": message})
    

        event = current["event"]
        decisions = [
            {"id": idx, "label": choice.label}
            for idx, choice in enumerate(current["choices"])
        ]


        return jsonify(
            {
                "done": False,
                "description": event.description,
                "decisions": decisions,
            }
        )

    @app.post("/api/choose")
    def api_choose():
        global stats_state, las_increment

        is_over, collapsed = check_game_over()
        if is_over:
            return jsonify({"done": True, "message": "Game over.", "game_over": True, "collapsed": collapsed})

        payload = request.get_json(silent=True) or {}
        decision_id = payload.get("decisionId")

        current = ensure_current_event()
        if current is None:
            return jsonify({"done": True, "message": "No active event to choose."}), 400

        try:
            decision_index = int(decision_id)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid decisionId."}), 400

        choices = current["choices"]
        if decision_index < 0 or decision_index >= len(choices):
            return jsonify({"error": "Decision index out of range."}), 400

        coe_name = current["coe_name"]
        engine = EventProcessor(NAMES[coe_name], policy_state, stats_state)
        next_event_id = engine.choose(choices[decision_index])

        def del_chain(deleted_event):
            try:
                EVENTS.remove(NAMES[deleted_event])
            except ValueError:
                pass
            CURR_OP.pop(f"EVENTS_{deleted_event}", None)
            NXT_EVENT.pop(f"EVENTS_{deleted_event}", None)
            NAMES.pop(deleted_event, None)

        if next_event_id is None:
            del_chain(coe_name)
            state["last_message"] = f"{coe_name} sequence resolved."
        elif next_event_id[:7] == 'EVENTS_':
            
            # If next_event_id is another chain
            new_coe_name = next_event_id.replace("EVENTS_", "", 1)
            print(f'next event id: {next_event_id}')
            print(f'next event id: {new_coe_name}')
            if new_coe_name in NAMES:
                CURR_OP[f"EVENTS_{new_coe_name}"] = 1
                event_temp = NAMES[new_coe_name]
                next_event_id = [e.id for e in event_temp.values() if getattr(e, "order_of_ops", None) == 1][0]
                NXT_EVENT[f"EVENTS_{new_coe_name}"] = next_event_id
                state["last_message"] = f"Switched to chain {new_coe_name}"
            del_chain(coe_name)
  
        else:
            CURR_OP[f"EVENTS_{coe_name}"] = NAMES[coe_name][next_event_id].order_of_ops
            NXT_EVENT[f"EVENTS_{coe_name}"] = next_event_id
            state["last_message"] = None

        write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES)

        stats_togo = do_all(policy_state, stats_state)
        stats_state, las_increment = go_thru(
            stats_state, stats_togo, las_increment, types_of_stats
        )

        is_over, collapsed = check_game_over()
        if is_over:
            return jsonify({"ok": True, "done": True, "message": "Game over.", "game_over": True, "collapsed": collapsed})

        state["current"] = None
        next_current = ensure_current_event()
        if next_current is None:
            return jsonify({"ok": True, "done": True, "message": state.get("last_message") or "No more events available."})
        event = next_current["event"]
        decisions = [{"id": idx, "label": choice.label} for idx, choice in enumerate(next_current["choices"])]
        return jsonify({"ok": True, "done": False, "description": event.description, "decisions": decisions})

    return app

def day_update():
    global curr_day, curr_month, curr_year, dis_say_event, stats_state, las_increment
    while True:
        sleep(2)
        if check_game_over()[0]:
            continue
        curr_day += 1
        curr_day, curr_month, curr_year = handle_days(curr_day, curr_month, curr_year)

        stats_togo = do_all(policy_state, stats_state)
        stats_state, las_increment = go_thru(
            stats_state, stats_togo, las_increment, types_of_stats
        )
        

if __name__ == "__main__":
    app = create_app()

    day_thread = Thread(target=day_update, daemon=True)
    day_thread.start()

    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)

