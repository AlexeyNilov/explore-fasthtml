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
        g = get_active_gladiator()
        info = fh.P(f"{g.name}_{g.id} HP: {g.hp} Max_HP: {g.max_hp}")
    except CreatureNotFound:
        pass
    return fh.Div(info, cls="col-xs", id="info_block")


def skill_buttons():
    skill_names = []
    try:
        g = get_active_gladiator()
        skill_names = get_skill_names(g.id)
    except CreatureNotFound:
        pass

    buttons = list()
    for skill_name in skill_names:
        buttons.append(
            fh.Button(
                skill_name,
                hx_get=f"/use_skill?name={skill_name}&creature_id={g.id}",
                hx_swap="none",
                style="margin: 2px; background-color: green; padding: 4px;",
                id=f"button_skill_{skill_name}",
                cls="skill_button",
            )
        )

    return fh.Div(*buttons, cls="col-xs-6", id="skill_buttons_block")


def control():
    return fh.Div(creature_info(), skill_buttons(), cls="row", id="control_block")
