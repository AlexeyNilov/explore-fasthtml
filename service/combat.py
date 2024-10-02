from dataclasses import dataclass

from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import save_event
from dnd_engine.model.event import Event


TEAM_SIZE = 5

combats = DB.t.combats
combats.xtra(owner="Arena")
Combat = combats.dataclass()
creatures = DB.t.creatures


@dataclass
class Gladiator:
    id: int
    name: str
    hp: int
    max_hp: int
    is_alive: int


combat_counter = 0


def get_combat_name():
    return f"Arena_{combat_counter}"


def get_combat_queue():
    return combats[get_combat_name()].queue


def get_creature(id: int) -> Gladiator:
    return Gladiator(**creatures[id])


def get_team_creatures(name: str):
    try:
        queue = get_combat_queue()
    except Exception:
        return []

    q = queue.split(";")
    creatures = list()
    for team_id_pair in q:
        items = team_id_pair.split(":")
        if items[0] == name:
            creatures.append(get_creature(items[1]))
    return creatures


def delete_combats(owner: str = "Arena"):
    sql = f"SELECT name FROM combats WHERE owner = '{owner}';"
    data = DB.q(sql)
    for item in data:
        combats.delete(item["name"])


def start_new_combat():
    delete_combats()
    global combat_counter
    combat_counter += 1
    c = combats.insert(Combat(
        name=get_combat_name(),
        owner="Arena",
        status="Not started",
        round=0,
        queue=""
    ))
    save_event(Event(source="Arena", msg=f"Combat created: {c}"))
    print("combat saved")


def start_next_round():
    c = combats[get_combat_name()]
    c.round += 1
    combats.upsert(c)
    save_event(Event(source="Arena", msg=f"Round {c.round} started"))
