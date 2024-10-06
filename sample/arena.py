import asyncio
from typing import Any
from typing import List

from dnd_engine.data.fastlite_loader import save_action
from fasthtml import common as fh

from data.logger import set_logging
from service.combat import start_new_combat
from service.event import get_events
from ui.combat import control
from ui.combat import event_log
from ui.combat import team
from ui.common import get_header
from ui.common import html_headers


set_logging()

name = "Dungeon Arena"
version = "0.0.78"
app = fh.FastHTML(hdrs=html_headers, debug=True)


@app.get("/")
def home():
    return (
        fh.Title(f"{name}: {version}"),
        fh.Main(
            get_header(name),
            fh.Div(
                team(name="Team Red", id="team_red", reverse=True),
                team(name="Team Blue", id="team_blue"),
                id="combat_queue",
                cls="row center-xs",
            ),
            fh.Div(
                fh.Div("Control Panel", control(), cls="col-xs", id="control_panel"),
                fh.Div("Event log", event_log(), cls="col-xs", id="event_panel"),
                id="footer",
                cls="row",
            ),
            cls="container",
            hx_ext="ws",
            ws_connect="/ws",
        ),
    )


@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return fh.FileResponse(f"{fname}.{ext}")


# WS-related stuff lives bellow
client_queue: List[Any] = []


async def update_clients():
    for client in client_queue:
        try:
            await client(
                (
                    get_events(),
                    team(name="Team Red", id="team_red", reverse=True),
                    team(name="Team Blue", id="team_blue"),
                    control(),
                )
            )
        except Exception:
            client_queue.remove(client)


async def on_connect(send):
    client_queue.append(send)


async def on_disconnect(send):
    await update_clients()


@app.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def ws(msg: str, send):
    pass


async def background_task():
    while True:
        if len(client_queue) > 0:
            await update_clients()
        await asyncio.sleep(0.5)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(background_task())


@app.get("/start")
async def start():
    start_new_combat()
    await update_clients()
    return "Start"


@app.get("/use_skill")
def use_skill(name: str, creature_id: int):
    action = {"attacker_id": creature_id, "skill_classes": "Attack"}
    save_action(action)


fh.serve()
