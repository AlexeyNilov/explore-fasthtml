from fasthtml import common as fh
from dataclasses import dataclass

from dnd_engine.data.fastlite_db import DB


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

    def __ft__(self):
        return fh.Div(
            f"{self.name}",
            fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
            fh.Img(src=f"img/{self.name.lower()}.png", width="80"),
            cls="box",
        )


def get_combat_queue(name: str):
    return combats[name].queue


def get_creature(id: int) -> Gladiator:
    return Gladiator(**creatures[id])


empty_space = fh.Div("Empty", cls="box")


def get_team(name: str, id: str, reverse: bool = False) -> list:
    team = [empty_space for _ in range(TEAM_SIZE)]
    queue = get_combat_queue(name="Arena")
    q = queue.split(";")
    creatures = list()
    for team_id_pair in q:
        items = team_id_pair.split(":")
        if items[0] == name:
            creatures.append(get_creature(items[1]))

    for i, c in enumerate(creatures):
        team[i] = c.__ft__()

    if reverse:
        t = fh.Div(*team[::-1], cls="row center-xs")
    else:
        t = fh.Div(*team, cls="row center-xs")
    return fh.Div(
        fh.H2(name),
        t,
        cls="col-xs",
        id=id
    )
