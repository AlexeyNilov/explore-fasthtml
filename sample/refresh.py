from fasthtml import common as fh

refresh = fh.Meta(http_equiv="refresh", content="10")
app = fh.FastHTML(hdrs=(fh.picolink, refresh))

count = 0


@app.get("/")
def home():
    return (
        fh.Title("Self refresh app"),
        fh.Main(
            fh.H1("Count Demo"),
            fh.P(f"Count is set to {count}", id="count"),
            fh.Button(
                "Increment",
                hx_post="/increment",
                hx_target="#count",
                hx_swap="innerHTML",
                hx_trigger="every 1s",
            ),
            cls="container",
        ),
    )


@app.post("/increment")
def increment():
    print("incrementing")
    global count
    count += 1
    return f"Count is set to {count}"


fh.serve()
