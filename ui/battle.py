from fasthtml import common as fh
from fastcore.all import patch

from dnd_engine.model.creature import Creature
from service.combat import red, blue


TEAM_SIZE = 5


@patch
def __ft__(self: Creature):
    return fh.Div(
        f"{self.name}",
        fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
        fh.Img(src=f"img/{self.name.lower()}.png", width="80"),
        cls="box",
    )


empty_space = fh.Div("Empty", cls="box")


def get_red_team() -> list:
    team = [empty_space for _ in range(TEAM_SIZE)]
    for i, c in enumerate(red.members):
        team[i] = c.__ft__()

    return fh.Div(
        fh.H2("Team Red"),
        fh.Div(*team[::-1], cls="row center-xs"),
        cls="col-xs",
        id="team_read"
    )


def get_blue_team() -> list:
    team = [empty_space for _ in range(TEAM_SIZE)]
    for i, c in enumerate(blue.members):
        team[i] = c.__ft__()
    return fh.Div(
        fh.H2("Team Blue"),
        fh.Div(*team, cls="row center-xs"),
        cls="col-xs",
        id="team_blue"
    )
