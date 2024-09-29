import random
from dnd_engine.data.bestiary import get_creature
from dnd_engine.model.combat import Combat
from dnd_engine.model.event import publish_deque
from dnd_engine.model.team import Team


class AsyncCombat(Combat):
    def one_round(self):
        self.form_combat_queue()
        self.next_round()


def get_new_combat() -> AsyncCombat:
    # Team Red
    wolfs = [get_creature("Wolf") for _ in range(random.randint(1, 3))]
    red = Team(name="Red", members=wolfs, events_publisher=publish_deque)

    # Team Blue
    pigs = [get_creature("Pig") for _ in range(random.randint(2, 5))]
    blue = Team(name="Blue", members=pigs, events_publisher=publish_deque)
    return AsyncCombat(name="Arena", events_publisher=publish_deque, teams=[red, blue])

# print_deque()

# print(wolf.model_dump(include={"name", "is_alive", "hp", "skills"}))
# for pig in pigs:
#     print(pig.model_dump(include={"name", "is_alive", "hp", "skills"}))
