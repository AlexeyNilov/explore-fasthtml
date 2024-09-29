import asyncio
from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import print_deque
from dnd_engine.model.event import publish_deque
from dnd_engine.model.team import Team


class AsyncCombat(Combat):
    async def battle(self):
        if self.is_completed:
            return

        while not self.is_the_end():
            self.form_combat_queue()
            self.fight()
            print_deque()
            await asyncio.sleep(0.5)


def get_new_combat() -> AsyncCombat:
    # Team Red
    wolf = get_creature("Wolf")
    red = Team(name="Red", members=[wolf], events_publisher=publish_deque)

    # Team Blue
    pigs = [get_creature("Pig") for _ in range(2)]
    blue = Team(name="Blue", members=pigs, events_publisher=publish_deque)
    return AsyncCombat(name="Arena", events_publisher=publish_deque, teams=[red, blue])

# print_deque()

# print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
# for pig in pigs:
#     print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
