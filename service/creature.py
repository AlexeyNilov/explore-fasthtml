from fasthtml import common as fh
from dnd_engine.model.creature import Creature
from fastcore.all import patch
import fastlite as fl
from sqlite_minutils.db import Database
from dnd_engine.data.storage_fastlite import load_creatures
import os


@patch
def __ft__(self: Creature):
    return fh.Div(
        f"{self.id}",
        fh.Ul(
            fh.Li("Name: ", self.name),
            fh.Li("Is alive: ", self.is_alive),
            fh.Li("Health: ", self.hp),
            fh.Li("Max health: ", self.max_hp),
        ),
        cls="box",
    )


db_path = os.environ['DB_PATH']
DB: Database = fl.database(db_path)
CREATURES = load_creatures(DB)

# print(CREATURES[0].__ft__())
