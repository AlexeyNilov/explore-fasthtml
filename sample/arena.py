from fasthtml import common as fh
from typing import List, Any
import asyncio
from service.event import delete_events, get_events
from data.logger import set_logging
from ui.common import html_headers, get_header
from ui.combat import get_team, event_log
from service.combat import start_new_combat


set_logging()

name = "Dungeon Arena"
version = "0.0.36"
app = fh.FastHTML(hdrs=html_headers, debug=True)


@app.get("/")
def home():
    return (
        fh.Title(f"{name}: {version}"),
        fh.Main(
            get_header(name),
            fh.Div(
                get_team(name="Team Red", id="team_red", reverse=True),
                get_team(name="Team Blue", id="team_blue"),
                id="combat_queue",
                cls="row center-xs",
            ),
            fh.Div(
                fh.Div("Control Panel", cls="col-xs-8"),
                event_log(),
                id="footer",
                cls="row"),
            cls="container",
            hx_ext="ws",
            ws_connect="/ws",
        ),
    )


@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return fh.FileResponse(f'{fname}.{ext}')


# WS-related stuff lives bellow
client_queue: List[Any] = []


async def update_clients():
    for client in client_queue:
        try:
            await client((get_events(), get_team(name="Team Red", id="team_red", reverse=True),
                          get_team(name="Team Blue", id="team_blue")))
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
    delete_events()
    start_new_combat()
    await update_clients()
    return "Start"


fh.serve()
