from fastcore.all import patch
from fasthtml import common as fh

from service.combat import CreatureNotFound
from service.combat import get_active_gladiator
from service.combat import get_skill_names
from service.combat import get_team_creatures
from service.combat import Gladiator
from service.combat import TEAM_SIZE
from service.event import get_events


@patch
def __ft__(self: Gladiator):
    if self.is_active:
        box_type = "active_box"
    else:
        box_type = "box"
    return fh.Div(
        f"{self.name}_{self.id} {self.turn}",
        fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
        fh.Img(src=f"img/{self.name.lower()}.png", width="80"),
        cls=f"{box_type}",
    )


empty_space = fh.Div("Empty", cls="box")


def team(name: str, id: str, reverse: bool = False) -> list:
    team = [empty_space for _ in range(TEAM_SIZE)]

    for i, c in enumerate(get_team_creatures(name)):
        team[i] = c.__ft__()

    if reverse:
        t = fh.Div(*team[::-1], cls="row center-xs")
    else:
        t = fh.Div(*team, cls="row center-xs")
    return fh.Div(fh.H2(name), t, cls="col-xs", id=id)


def event_log():
    return fh.Div(
        get_events(),
        cls="col-xs",
        id="event_block",
        style="height: 200px; overflow-y: scroll;",
    )


def creature_info():
    info = None
    try:
        info = get_active_gladiator()
    except CreatureNotFound:
        pass
    return fh.Div("Info block", info, cls="col-xs", id="info_block")


def skill_buttons():
    skill_names = []
    try:
        skill_names = get_skill_names()
    except CreatureNotFound:
        pass

    buttons = list()
    for skill_name in skill_names:
        buttons.append(skill_name)

    return fh.Div("Control buttons", buttons, cls="col-xs", id="skill_buttons_block")


def control():
    return fh.Div(creature_info(), skill_buttons(), cls="row", id="control_block")
