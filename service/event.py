from typing import List

from dnd_engine.data.fastlite_loader import load_events
from fasthtml import common as fh


def get_events_from_db() -> List[str]:
    events: List[str] = []
    for e in load_events():
        events.append(f'{e["source"]}: {e["msg"]}')
    return events


def get_events():
    events = get_events_from_db()
    return fh.Div(*[fh.P(e, id="event_msg") for e in events[::-1]], id="event_list")
