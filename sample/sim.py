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
style = "{ border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px; }"
css = fh.Style(
    f"""
    .row {style}
    .box {style}
    .col-xs-3 {style}
    .col-xs-4 {style}
    .col-xs {style}
"""
)

app = fh.FastHTML(hdrs=(fh.picolink, flex_grid, htmx_ws, css), debug=True)


name = "Sim"
is_started = False
count = 0
events = ["Empty"]


def sim():
    return fh.Div(*load_ft_creatures(), cls="col-xs-4", id="sim-list")


def get_events():
    global count
    global events

    if is_started:
        count += 1
        events.append(f"New event {count}")

    return fh.Div(*[fh.P(e) for e in events[::-1]], id="event-list", style="margin: 1px; padding: 1px;")


def event_log():
    return fh.Div(
        get_events(),
        cls="col-xs",
        id="event-block",
        style="height: 200px; overflow-y: scroll;"
    )


@app.get("/get_title")
def get_title():
    status = "stopped" if is_started else "started"
    return f"{name}: {status}"


def get_start_button():
    return "Stop" if is_started else "Start"


@app.get("/")
def home(session):
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    header = fh.Div(
        fh.Div(
            fh.H1(
                get_title(),
                id="title",
                hx_trigger="sim_start from:body",
                hx_get="/get_title",
                hw_swap="afterbegin",
                style="margin: 6px;",
                hx_target="event"
            ),
            cls="col-xs-3",
        ),
        fh.Div(
            fh.Button(
                get_start_button(),
                hx_get="/start",
                hx_target="#button",
                hx_swap="innerHTML",
                style="margin: 6px;",
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
            fh.Div(sim(), event_log(), id="gen-list", cls="row"),
            cls="container",
            hx_ext="ws",
            ws_connect="/ws",
        ),
    )


player_queue: List[Any] = []


async def update_players():
    for player in player_queue:
        try:
            await player((sim(), get_events()))
        except Exception:
            player_queue.remove(player)


async def on_connect(send):
    player_queue.append(send)


async def on_disconnect(send):
    await update_players()


@app.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def ws(msg: str, send):
    pass


async def background_task():
    while True:
        if len(player_queue) > 0:
            await update_players()
        await asyncio.sleep(0.5)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(background_task())


@app.get("/start")
async def start():
    global is_started
    is_started = not is_started
    await update_players()
    return get_start_button(), fh.HtmxResponseHeaders(trigger="sim_start")


fh.serve()
