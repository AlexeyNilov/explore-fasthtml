from fasthtml import common as fh
from typing import List, Any
import uuid
import asyncio
from service.creature import load_ft_creatures
from data.logger import set_logging


set_logging()

flex_grid = fh.Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
)
htmx_ws = fh.Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
css = fh.Style(
    """
    .row { border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px; }
    .box { border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px; }
    .col-xs-4 { border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px; }
"""
)

app = fh.FastHTML(hdrs=(fh.picolink, flex_grid, htmx_ws, css), debug=True)


name = "Sim 1.1"
is_started = False
button = "Start"


def sim():
    data = (fh.Div(*load_ft_creatures(), cls="col-xs-2", id="oak"),)
    return data


@app.get("/")
def home(session):
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    header = fh.Div(
        fh.Div(
            fh.H1(name, id="title"),
            cls="col-xs-4",
        ),
        fh.Div(
            fh.Button(
                f"{button}",
                hx_put="/start",
                hx_target="#gen-list",
                hx_swap="none",
                style="margin: 4px;",
                id="button",
            ),
            cls="col-xs-2",
        ),
        cls="row",
    )

    return (
        fh.Title("Simulation"),
        fh.Main(
            header,
            fh.Div(sim(), id="gen-list", cls="row"),
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
        await asyncio.sleep(0.1)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(background_task())


def get_title():
    return f"{name} status: {is_started}"


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
    return fh.H1(get_title(), id="title", hx_swap_oob="true"), b  # TODO use headers


fh.serve()
