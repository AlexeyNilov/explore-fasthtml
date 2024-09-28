from fasthtml import common as fh
from dnd_engine.model.creature import Creature
from fastcore.all import patch
from dnd_engine.data.storage_fastlite import load_creatures


@patch
def __ft__(self: Creature):
    return fh.Div(
        f"{self.id}",
        fh.Progress(value=f"{self.hp}", max=f"{self.max_hp}"),
        fh.Ul(
            fh.Li("Name: ", self.name),
            fh.Li("Is alive: ", self.is_alive),
            fh.Li("Health: ", self.hp),
            fh.Li("Max health: ", self.max_hp),
        ),
        cls="box",
    )


load_ft_creatures = load_creatures
