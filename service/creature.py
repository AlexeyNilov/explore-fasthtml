from fasthtml import common as fh
from dnd_engine.model.creature import Creature
from dnd_engine.model.skill_tech import SkillRecord


class CreatureFT(Creature):
    def __ft__(self):
        return fh.Div(
            f"{self.id}",
            fh.Ul(
                fh.Li("Name: ", self.name),
                fh.Li("Is alive: ", self.is_alive),
                fh.Li("Health: ", self.hp),
            ),
            style="border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px;",
            cls="box",
        )


oak_data = {
    "name": "The first oak",
    "hp": 400,
    "max_hp": 500,
    "skill_book": [SkillRecord(name="eat", skill_class="Consume")],
    "compatible_with": ["water"],
    "nature": "organic",
}

oak = CreatureFT(**oak_data)
