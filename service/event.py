from typing import List
from fasthtml import common as fh
from dnd_engine.data.storage_fastlite import load_events
from dnd_engine.model.event import get_deque

EVENTS = list()


def get_events_from_db():
    events: List[str] = []
    for e in load_events():
        events.append(f'{e["source"]}: {e["msg"]}')
    return events


def get_events_1():
    events = get_events_from_db()
    if not events:
        events.append("Event log")

    return fh.Div(*[fh.P(e, id="event_msg") for e in events[::-1]], id="event_list")


def get_events():
    global EVENTS
    EVENTS += get_deque()
    if not EVENTS:
        EVENTS.append("Event log")

    return fh.Div(*[fh.P(e, id="event_msg") for e in EVENTS[::-1]], id="event_list")


def event_log():
    return fh.Div(
        get_events(),
        cls="col-xs",
        id="event_block",
        style="height: 200px; overflow-y: scroll;",
    )
