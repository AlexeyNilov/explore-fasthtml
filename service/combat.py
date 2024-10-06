from dataclasses import dataclass
from typing import List

from dnd_engine.data.fastlite_dataclasses import Combats
from dnd_engine.data.fastlite_db import DB
from dnd_engine.data.fastlite_loader import load_creature
from dnd_engine.data.fastlite_loader import save_action
from dnd_engine.data.fastlite_loader import save_event
from dnd_engine.model.event import Event


TEAM_SIZE = 5

combats = DB.t.combats
combats.xtra(owner="Arena")
combats.dataclass()
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
    is_active: int = 0


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
                gladiator = get_creature(int(items[1]))
            except CreatureNotFound:
                continue

            gladiator.turn = int(items[2])
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
    c = combats.insert(
        Combats(
            name=get_combat_name(),
            owner="Arena",
            status="Not started",
            round=0,
            queue="",
        )
    )
    save_event(Event(source="Arena", msg=f"Combat created: {c}"))


def get_active_gladiator() -> Gladiator:
    sql = "SELECT id FROM creatures WHERE is_active = 1;"
    data = DB.q(sql)
    if data:
        creature_id = data[0]["id"]
        return get_creature(creature_id)
    else:
        raise CreatureNotFound


def get_skill_names(creature_id: int) -> List[str]:
    cr = load_creature(creature_id)
    return list(cr.skills.keys())


def save_skill_usage(name: str, creature_id: int):
    action = {
        "attacker_id": creature_id,
        "skill_names": name,
    }
    save_action(action)
