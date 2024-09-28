from fasthtml import common as fh
from typing import List, Any
import uuid
import asyncio
from service.event import event_log, get_events
from data.logger import set_logging
from service.headers import headers


set_logging()
app = fh.FastHTML(hdrs=headers, debug=True)
player_queue: List[Any] = []


@app.get("/")
def home(session):
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    header = fh.Div(
        fh.Div(
            fh.H1("Dungeon Arena", id="title", style="margin: 6px;"), cls="col-xs-3"
        ),
        cls="row",
    )

    return (
        fh.Title("Dungeon Arena"),
        fh.Main(
            header,
            fh.Div(event_log(), id="main_body", cls="row"),
            cls="container",
            hx_ext="ws",
            ws_connect="/ws",
        ),
    )


async def update_players():
    for player in player_queue:
        try:
            await player(get_events())
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


fh.serve()
