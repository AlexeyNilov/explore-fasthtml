from fasthtml import common as fh
from typing import List, Any
import uuid
import asyncio
from service.resource import (
    get_random_resource,
    remove_empty_resource,
    RESOURCES,
    create_fruit,
)
from service.creature import oak
from data.logger import set_logging


set_logging()
gridlink = fh.Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css",
)
htmx_ws = fh.Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
app = fh.FastHTML(hdrs=(fh.picolink, gridlink, htmx_ws), debug=True)


is_started = False
button = "Start"


def sim():
    data = (
        fh.Div(*RESOURCES, cls="row col-xs-12", id="resources"),
        fh.Div(oak, cls="row col-xs-12", id="oak"),
    )
    return data


@app.get("/")
def home(session):
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    return (
        fh.Title("Simulation"),
        fh.Main(
            fh.H1("Sim demo", id="title"),
            fh.Button(
                f"{button}",
                hx_put="/start",
                hx_target="#gen-list",
                hx_swap="none",
                style="margin: 8px;",
                id="button",
            ),
            fh.Div(sim(), id="gen-list"),
            cls="container",
            hx_ext="ws",
            ws_connect="/main",
        ),
    )


player_queue: List[Any] = []


async def update_players():
    for i, player in enumerate(player_queue):
        try:
            await player(sim())
        except Exception:
            player_queue.pop(i)


async def on_connect(send):
    player_queue.append(send)


async def on_disconnect(send):
    await update_players()


@app.ws("/main", conn=on_connect, disconn=on_disconnect)
async def ws(msg: str, send):
    pass


async def background_task():
    while True:
        if len(player_queue) > 0:
            await update_players()
        await asyncio.sleep(1)


async def simulation():
    while True:
        if is_started and oak.is_alive:

            oak.hp -= 1  # Live sucks!

            if RESOURCES:
                oak.apply(skill=oak.skills["eat"], to=get_random_resource())
                if oak.hp == oak.max_hp:
                    oak.hp -= create_fruit()

                remove_empty_resource()

        await asyncio.sleep(0.3)


background_task_coroutine = asyncio.create_task(background_task())
simulation_coroutine = asyncio.create_task(simulation())


def get_title():
    return f"Sim demo status: {is_started}"


def switch_button():
    global button
    if button == "Start":
        button = "Stop"
    else:
        button = "Start"


@app.put("/start")
async def start():
    global is_started
    is_started = not is_started
    switch_button()
    b = fh.Button(
        f"{button}",
        hx_put="/start",
        hx_target="#gen-list",
        hx_swap="none",
        style="margin: 8px;",
        id="button",
        hx_swap_oob="true",
    )
    await update_players()
    return fh.H1(get_title(), id="title", hx_swap_oob="true"), b


fh.serve()
