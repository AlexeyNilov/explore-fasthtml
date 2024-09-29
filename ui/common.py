from fasthtml import common as fh


flex_grid = fh.Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
)
htmx_ws = fh.Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
style = "border: 1px solid black; border-radius: 5px; margin: 2px; padding: 2px;"
css = fh.Style(
    f"""
    .row {{ {style} }}
    .box {{ {style} width: 110px; }}
    .col-xs-3 {{ {style} }}
    .col-xs-4 {{ {style} }}
    .col-xs-5 {{ {style} }}
    .col-xs-6 {{ {style} }}
    .col-xs {{ {style} }}
    #event_list p {{ margin: 1px; padding: 1px;}}
    progress::-webkit-progress-value {{ background-color: red !important; }}
"""
)
html_headers = (fh.picolink, flex_grid, htmx_ws, css)


def get_header(name: str):
    return fh.Div(
        fh.Div(
            fh.H1(name, id="title", style="margin: 6px;"), cls="col-xs-3"
        ),
        fh.Div(
            fh.Button(
                "Start",
                hx_get="/start",
                style="margin: 6px;",
                id="button",
            ),
            cls="col-xs-2",
        ),
        cls="row",
    )
