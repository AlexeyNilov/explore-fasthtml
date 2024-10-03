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
    .active_box {{ border: 3px solid green; border-radius: 5px; margin: 2px; padding: 2px; width: 110px; }}
    .col-xs-3 {{ {style} }}
    .col-xs-4 {{ {style} }}
    .col-xs-5 {{ {style} }}
    .col-xs-8 {{ {style} }}
    .col-xs {{ {style} }}
    #event_list p {{ margin: 1px; padding: 1px;}}
    progress::-webkit-progress-value {{ background-color: red !important; }}
"""
)
html_headers = (fh.picolink, flex_grid, htmx_ws, css)


def get_header(name: str):
    return fh.Div(
        fh.Div(
            fh.H1(name, id="title", style="margin: 6px;")
        ),
        fh.Div(
            fh.Button(
                "Start",
                hx_get="/start",
                hx_swap="none",
                style="margin: 6px;",
                id="button_start",
            )
        ),
        fh.Div(
            fh.Button(
                "Next",
                hx_get="/next",
                hx_swap="none",
                style="margin: 6px;",
                id="button_next",
            )
        ),
        cls="row",
    )
