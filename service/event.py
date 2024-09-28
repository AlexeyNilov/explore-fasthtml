from typing import List
from dnd_engine.data.storage_fastlite import load_events


def get_events_from_db():
    events: List[str] = []
    for e in load_events():
        events.append(f'{e["creature_id"]}: {e["msg"]}')
    return events
