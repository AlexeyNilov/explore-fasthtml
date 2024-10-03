from typing import List
from fasthtml import common as fh
from dnd_engine.data.fastlite_loader import load_events
from dnd_engine.data.fastlite_db import DB, create_events_table


def delete_events():
    DB.t.events.drop()
    create_events_table()


def get_events_from_db():
    events: List[str] = []
    for e in load_events():
        events.append(f'{e["source"]}: {e["msg"]}')
    return events


def get_events():
    events = get_events_from_db()
    if not events:
        events.append("Event log")

    return fh.Div(*[fh.P(e, id="event_msg") for e in events[::-1]], id="event_list")
