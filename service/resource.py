from typing import List
from fasthtml import common as fh
from dnd_engine.model.resource import Resource
import random


class NoResourcesAvailable(Exception):
    pass


class ResourceFT(Resource):
    def __ft__(self):
        return fh.Div(
            f"{self.id}",
            fh.Ul(fh.Li("Name: ", self.name), fh.Li("Value: ", self.value)),
            cls="box",
        )


water_data = {"name": "Water", "value": 200, "nature": "water"}
food_data = {"name": "Food", "value": 20, "nature": "organic"}
fruit_data = {"name": "Fruit", "value": 50, "nature": "organic"}


def get_resources() -> List[ResourceFT]:
    resources: List[ResourceFT] = list()

    for _ in range(2):
        resources.append(ResourceFT(**water_data))
        resources.append(ResourceFT(**food_data))
    return resources


RESOURCES = get_resources()


def remove_empty_resource():
    global RESOURCES
    for i, resource in enumerate(RESOURCES):
        if resource.value <= 0:
            RESOURCES.pop(i)


def get_random_resource():
    if RESOURCES:
        return random.choice(RESOURCES)
    raise NoResourcesAvailable


def create_fruit() -> int:
    fruit = ResourceFT(**fruit_data)
    RESOURCES.append(fruit)
    return fruit.value
