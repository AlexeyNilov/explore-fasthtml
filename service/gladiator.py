from fasthtml import common as fh
from dnd_engine.model.creature import Creature
from fastcore.all import patch
# from dnd_engine.data.storage_fastlite import load_creatures
from dnd_engine.data.bestiary import get_creature


@patch
def __ft__(self: Creature):
    return fh.Div(
        f"{self.name}",
        fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
        fh.Img(src=f"img/{self.name.lower()}.png", width="80"),
        cls="box",
    )


# load_ft_creatures = load_creatures
empty_space = fh.Div("Empty", cls="box")


def get_red_team() -> list:
    team = [empty_space for _ in range(4)]
    g = get_creature("Wolf")
    team.append(g.__ft__())
    return team


def get_blue_team() -> list:
    team = [empty_space for _ in range(4)]
    g = get_creature("Pig")
    team.insert(0, g.__ft__())
    return team
