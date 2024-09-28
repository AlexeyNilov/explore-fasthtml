from fasthtml import common as fh
from typing import List, Any
import asyncio
from service.event import event_log, get_events
from data.logger import set_logging
from ui.common import html_headers, get_header
from service.gladiator import get_red_team, get_blue_team


set_logging()

name = "Dungeon Arena"
app = fh.FastHTML(hdrs=html_headers, debug=True)


@app.get("/")
def home():
    return (
        fh.Title(name),
        fh.Main(
            get_header(name),
            fh.Div(
                fh.Div(
                    fh.H2("Team Red"),
                    fh.Div(*get_red_team(), cls="row center-xs"),
                    cls="col-xs",
                    id="team_read"
                ),
                fh.Div(
                    fh.H2("Team Blue"),
                    fh.Div(*get_blue_team(), cls="row center-xs"),
                    cls="col-xs",
                    id="team_blue"
                ),
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
            await client(get_events())
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


fh.serve()
