from fasthtml import common as fh
from fastcore.all import patch
from service.combat import TEAM_SIZE, Gladiator, get_team_creatures
from service.event import get_events


@patch
def __ft__(self: Gladiator):
    return fh.Div(
        f"{self.name}",
        fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
        fh.Img(src=f"img/{self.name.lower()}.png", width="80"),
        cls="box",
    )


empty_space = fh.Div("Empty", cls="box")


def get_team(name: str, id: str, reverse: bool = False) -> list:
    team = [empty_space for _ in range(TEAM_SIZE)]

    for i, c in enumerate(get_team_creatures(name)):
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


def event_log():
    return fh.Div(
        get_events(),
        cls="col-xs",
        id="event_block",
        style="height: 200px; overflow-y: scroll;",
    )
