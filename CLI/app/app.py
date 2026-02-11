from __future__ import annotations

import sys
from pathlib import Path
from threading import Thread
from time import sleep

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stavanger_app.web.CLI.chain_of_events.coe_logic import Event, Transition, EventProcessor
from stavanger_app.web.CLI.chain_of_events.infra import stats, policies, types_of_stats, last_incrimentation
from stavanger_app.web.CLI.pol_2_stat.logic import do_all
from stavanger_app.web.CLI.pol_2_stat.increment import go_thru
from stavanger_app.web.CLI.chain_of_events.coe_compiler import write_events_to_files, open_ready_events
from stavanger_app.web.CLI.chain_of_events.polarisation import polarisat
from stavanger_app.web.CLI.chain_of_events.terrorist_isis import terror_isis_1
import random

policy_state = policies()
stats_state = stats()

possible_ev = []
las_increment = last_incrimentation()

curr_day = 0
dis_say_event = False

EVENTS_POLARISATION = polarisat(Event, Transition, stats_state)
EVENTS_TERRORIST_ISIS_1 = terror_isis_1(Event, Transition, stats_state)

EVENTS = [EVENTS_POLARISATION, EVENTS_TERRORIST_ISIS_1]
CURR_OP = {'EVENTS_POLARISATION': 0, 'EVENTS_TERRORIST_ISIS_1': 0}
NXT_EVENT = {'EVENTS_POLARISATION': None, 'EVENTS_TERRORIST_ISIS_1': None}

NAMES = {
    'POLARISATION': EVENTS_POLARISATION,
    'TERRORIST_ISIS_1': EVENTS_TERRORIST_ISIS_1
}



from typing import Any

from flask import Flask, render_template, request, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

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
        engine = EventProcessor(NAMES[coe_name], policy_state)
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
        return render_template("index.html", curr_day=curr_day)

    @app.get("/api/day")
    def api_day():
        return jsonify({"day": curr_day})

    @app.get("/api/event")
    def api_event():
        global dis_say_event

        if dis_say_event == True:
            return jsonify({"done": True, "message": "An event has already occurred today. Wait for the next day."})

        current = ensure_current_event()

        if current is None:
            message = state.get("last_message") or "No more events available."
            return jsonify({"done": True, "message": message})
        dis_say_event = True

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
        engine = EventProcessor(NAMES[coe_name], policy_state)
        next_event_id = engine.choose(choices[decision_index])

        if next_event_id is None:
            try:
                EVENTS.remove(NAMES[coe_name])
            except ValueError:
                pass
            CURR_OP.pop(f"EVENTS_{coe_name}", None)
            NXT_EVENT.pop(f"EVENTS_{coe_name}", None)
            NAMES.pop(coe_name, None)
            state["last_message"] = f"{coe_name} sequence resolved."
        else:
            CURR_OP[f"EVENTS_{coe_name}"] = NAMES[coe_name][next_event_id].order_of_ops
            NXT_EVENT[f"EVENTS_{coe_name}"] = next_event_id
            state["last_message"] = None

        write_events_to_files(EVENTS, CURR_OP, NXT_EVENT, NAMES)

        stats_togo = do_all(policy_state, stats_state)
        stats_state, las_increment = go_thru(
            stats_state, stats_togo, las_increment, types_of_stats
        )

        state["current"] = None
        return jsonify({"ok": True})

    return app

def day_update():
    global curr_day, dis_say_event
    while True:
        curr_day += 1
        dis_say_event = False
        sleep(4)

if __name__ == "__main__":
    app = create_app()
    day_thread = Thread(target=day_update, daemon=True)
    day_thread.start()
    app.run(host="127.0.0.1", port=5000, debug=True)

