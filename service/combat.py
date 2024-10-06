from dataclasses import dataclass
from typing import List

from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import save_event
from dnd_engine.model.event import Event


TEAM_SIZE = 5

combats = DB.t.combats
combats.xtra(owner="Arena")
Combat = combats.dataclass()
creatures = DB.t.creatures
actions = DB.t.actions


class CreatureNotFound(Exception):
    pass


class CombatNotFound(Exception):
    pass


@dataclass
class Gladiator:
    id: int
    name: str
    hp: int
    max_hp: int
    is_alive: int
    turn: int = 0
    is_attacker: bool = False
    is_target: bool = False


combat_counter = 0


def get_combat_name() -> str:
    return f"Arena_{combat_counter}"


def get_combat_queue() -> str:
    try:
        return combats[get_combat_name()].queue
    except Exception:
        raise CombatNotFound


def get_creature(id: int) -> Gladiator:
    try:
        return Gladiator(**creatures[id])
    except Exception:
        raise CreatureNotFound


def get_gladiators_from_queue(queue: str, team_name: str) -> List[Gladiator]:
    q = queue.split(";")
    gladiators = list()
    for team_id_pair in q:
        items = team_id_pair.split(":")
        if items[0] == team_name:
            try:
                gladiator = get_creature(items[1])
            except CreatureNotFound:
                continue

            gladiator.turn = items[2]
            # if gladiator.id == action["attacker_id"]:
            #     gladiator.is_attacker = True
            # if gladiator.id == action["target_id"]:
            #     gladiator.is_target = True
            # print(gladiator)
            gladiators.append(gladiator)
    return gladiators


def get_team_creatures(name: str) -> list:
    if not combats() or not creatures():
        return []
    try:
        queue = get_combat_queue()
    except CombatNotFound:
        return []

    return get_gladiators_from_queue(queue, name)


def start_new_combat():
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
